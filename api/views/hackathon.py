"""
    General api calls on a hackathon
"""

from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .. import models
from .decorators import require_POST_JSON


@require_POST_JSON
def subscribe(request):
    subscriber = models.Subscriber.objects.create(
        email=request.JSON['email'],
        hackathon=models.Hackathon.objects.current())

    try:
        subscriber.full_clean()
    except ValidationError as e:
        return JsonResponse({
            'error': str(e)
        })

    subscriber.save()

    return JsonResponse({})
