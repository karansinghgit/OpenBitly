import json

from django.test import TestCase

from .helpers import BASE_62_SET, generate_code, is_valid_alias, unique_code
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


class AliasValidationTests(TestCase):
    def test_accepts_url_safe_aliases(self):
        self.assertTrue(is_valid_alias("my-link_1"))

    def test_rejects_bad_characters_and_length(self):
        self.assertFalse(is_valid_alias("has space"))
        self.assertFalse(is_valid_alias("way-too-long-alias"))
        self.assertFalse(is_valid_alias(""))

    def test_rejects_reserved_names(self):
        self.assertFalse(is_valid_alias("admin"))


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

    def test_shorten_uses_custom_alias(self):
        res = self.post({"url": "https://example.com", "alias": "promo"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["code"], "promo")

    def test_shorten_rejects_invalid_alias(self):
        res = self.post({"url": "https://example.com", "alias": "bad alias"})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(Link.objects.exists())

    def test_shorten_rejects_taken_alias(self):
        Link.objects.create(code="promo", long_url="https://a.com")
        res = self.post({"url": "https://example.com", "alias": "promo"})
        self.assertEqual(res.status_code, 409)
        self.assertEqual(Link.objects.filter(code="promo").count(), 1)


class LinksApiTests(TestCase):
    def test_links_returns_requested_codes_in_order_with_counts(self):
        old = Link.objects.create(code="old", long_url="https://a.com")
        Link.objects.create(code="new", long_url="https://b.com")
        Click.objects.create(link=old)
        Click.objects.create(link=old)

        # The browser sends its codes (newest first) from localStorage.
        res = self.client.get("/api/links?codes=new,old")
        self.assertEqual(res.status_code, 200)
        links = res.json()["links"]

        self.assertEqual([l["code"] for l in links], ["new", "old"])
        counts = {l["code"]: l["click_count"] for l in links}
        self.assertEqual(counts, {"new": 0, "old": 2})

    def test_links_is_scoped_to_requested_codes(self):
        Link.objects.create(code="mine", long_url="https://a.com")
        Link.objects.create(code="theirs", long_url="https://b.com")

        res = self.client.get("/api/links?codes=mine")
        self.assertEqual([l["code"] for l in res.json()["links"]], ["mine"])

    def test_links_empty_without_codes(self):
        Link.objects.create(code="x", long_url="https://a.com")
        res = self.client.get("/api/links")
        self.assertEqual(res.json()["links"], [])


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
