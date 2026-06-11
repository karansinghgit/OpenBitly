import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Link
from .helpers import unique_code

@csrf_exempt
@require_POST
def shorten(request):
    data = json.loads(request.body or "{}")
    url = data.get("url")
    if not url:
        return JsonResponse({"error": "url is required"}, status=400)

    link = Link.objects.create(code=unique_code(), long_url=url)
    short_url = f"{request.scheme}://{request.get_host()}/{link.code}"
    return JsonResponse(
        {"code": link.code, "short_url": short_url, "long_url": link.long_url},
        status=201,
    )
