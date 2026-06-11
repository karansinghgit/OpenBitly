import json
from urllib.parse import urlparse

from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Click, Link
from .helpers import unique_code


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

    link = Link.objects.create(code=unique_code(), long_url=url)
    return JsonResponse(_serialize(link, request), status=201)


@require_GET
def links(request):
    qs = (
        Link.objects.annotate(click_count=Count("clicks"))
        .order_by("-created_at")
    )
    return JsonResponse(
        {"links": [_serialize(link, request, link.click_count) for link in qs]}
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
