from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from pprint import pprint
import json

#
# @csrf_exempt
# @require_GET
# def test(request):
#
#     test_obj = Test(some_str='rawr')
#     test_obj.save()
#
#     return JsonResponse({
#
#     })
#
#
# @csrf_exempt
# @require_POST
# def save(request):
#     data = json.loads(request.POST['data'])
#
#     pprint(data)
#
#     return JsonResponse({
#
#     })
