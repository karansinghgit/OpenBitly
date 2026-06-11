import json
from urllib.parse import urlparse

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Click, Link
from .helpers import is_valid_alias, unique_code


def _serialize(link, request, click_count=0):
    return {
        "code": link.code,
        "short_url": f"{request.scheme}://{request.get_host()}/{link.code}",
        "long_url": link.long_url,
        "click_count": click_count,
    }

@csrf_exempt
@require_POST
def shorten(request):
    data = json.loads(request.body or "{}")
    url = data.get("url")
    if not url:
        return JsonResponse({"error": "url is required"}, status=400)

    # Reject URLs that point back at our own host, otherwise the short link
    # would just redirect to this service (or to itself) and create a loop.
    if urlparse(url).hostname == request.get_host().split(":")[0]:
        return JsonResponse(
            {"error": "URL cannot point back at this service"}, status=400
        )

    # Optional custom alias; fall back to a random code when none is given.
    alias = (data.get("alias") or "").strip()
    if alias:
        if not is_valid_alias(alias):
            return JsonResponse(
                {"error": "alias may only contain letters, numbers, hyphens and "
                          "underscores (max 10 characters)"},
                status=400,
            )
        if Link.objects.filter(code=alias).exists():
            return JsonResponse({"error": "alias is already taken"}, status=409)
        code = alias
    else:
        code = unique_code()

    link = Link.objects.create(code=code, long_url=url)
    return JsonResponse(_serialize(link, request), status=201)


@require_GET
def links(request):
    # Scoped to the codes the caller created (kept in their browser's
    # localStorage). There are no accounts, so the browser is the only thing
    # that knows which links are "mine"; the DB stays the source of truth.
    codes = [c for c in request.GET.get("codes", "").split(",") if c]
    if not codes:
        return JsonResponse({"links": []})

    qs = Link.objects.filter(code__in=codes).annotate(click_count=Count("clicks"))
    by_code = {link.code: link for link in qs}
    # Preserve the order the browser sent (newest first).
    ordered = [by_code[c] for c in codes if c in by_code]
    return JsonResponse(
        {"links": [_serialize(link, request, link.click_count) for link in ordered]}
    )

@require_GET
def resolve(request, code):
    # 302 (not 301) so repeat visits don't get cached
    link = get_object_or_404(Link, code=code)

    # Record the visit synchronously, before redirecting. This is fine at
    # current traffic, but if the redirect path ever becomes hot this insert
    # should be pushed onto a queue (e.g. Celery/SQS) so it stays off the
    # request's critical path.
    Click.objects.create(
        link=link,
        referer=request.META.get("HTTP_REFERER", ""),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )

    return HttpResponse(status=302, headers={"Location": link.long_url})
