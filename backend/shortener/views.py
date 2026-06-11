import json
from urllib.parse import urlparse

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Link
from .helpers import unique_code

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
    short_url = f"{request.scheme}://{request.get_host()}/{link.code}"
    return JsonResponse(
        {"code": link.code, "short_url": short_url, "long_url": link.long_url},
        status=201,
    )

@require_GET
def resolve(request, code):
    # 302 (not 301) so repeat visits don't get cached
    link = get_object_or_404(Link, code=code)
    return HttpResponse(status=302, headers={"Location": link.long_url})
