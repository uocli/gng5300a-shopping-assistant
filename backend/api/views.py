from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def query_view(request):

    return JsonResponse({"message": "Hello, world!"})
