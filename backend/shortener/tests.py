import json

from django.test import TestCase

from .helpers import BASE_62_SET, generate_code, unique_code
from .models import Click, Link


class Base62Tests(TestCase):
    def test_generate_code_has_requested_length(self):
        self.assertEqual(len(generate_code()), 7)
        self.assertEqual(len(generate_code(10)), 10)

    def test_generate_code_uses_only_base62_chars(self):
        code = generate_code(50)
        self.assertTrue(all(c in BASE_62_SET for c in code))

    def test_unique_code_avoids_existing_codes(self):
        # Pre-create every code but one, so unique_code must find the gap.
        Link.objects.create(code="aaa", long_url="https://a.com")
        self.assertNotEqual(unique_code(), "aaa")


class ShortenApiTests(TestCase):
    def post(self, body):
        return self.client.post(
            "/api/shorten", data=json.dumps(body), content_type="application/json"
        )

    def test_shorten_creates_link(self):
        res = self.post({"url": "https://example.com/page"})
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertEqual(data["long_url"], "https://example.com/page")
        self.assertEqual(data["click_count"], 0)
        self.assertTrue(Link.objects.filter(code=data["code"]).exists())

    def test_shorten_requires_url(self):
        res = self.post({})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(Link.objects.exists())

    def test_shorten_rejects_self_host(self):
        res = self.post({"url": "http://testserver/abc"})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(Link.objects.exists())


class LinksApiTests(TestCase):
    def test_links_lists_newest_first_with_click_counts(self):
        old = Link.objects.create(code="old", long_url="https://a.com")
        new = Link.objects.create(code="new", long_url="https://b.com")
        Click.objects.create(link=old)
        Click.objects.create(link=old)

        res = self.client.get("/api/links")
        self.assertEqual(res.status_code, 200)
        links = res.json()["links"]

        self.assertEqual([l["code"] for l in links], ["new", "old"])
        counts = {l["code"]: l["click_count"] for l in links}
        self.assertEqual(counts, {"new": 0, "old": 2})


class ResolveTests(TestCase):
    def test_resolve_redirects_and_records_click(self):
        link = Link.objects.create(code="xyz", long_url="https://example.com")
        res = self.client.get(
            "/xyz", HTTP_REFERER="https://ref.com", HTTP_USER_AGENT="pytest-agent"
        )
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.headers["Location"], "https://example.com")

        click = Click.objects.get(link=link)
        self.assertEqual(click.referer, "https://ref.com")
        self.assertEqual(click.user_agent, "pytest-agent")

    def test_resolve_unknown_code_returns_404(self):
        self.assertEqual(self.client.get("/nope").status_code, 404)
