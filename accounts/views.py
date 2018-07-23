import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.shortcuts import render_to_response
from django.views.decorators.http import require_http_methods

from accounts.services import AccountService

# объект сервис
accountService = AccountService()

def index(request):
    return render_to_response('index.html')

@require_http_methods(["GET"])
def get_all_accounts(request):
    data = serializers.serialize('json', accountService.get_all_accounts())
    return HttpResponse(data, content_type="application/json")

@require_http_methods(["GET"])
def get_accounts_by_inn(request, inn):
    print('accounts by inn')
    data = serializers.serialize('json', accountService.get_accounts_by_inn(inn))
    return HttpResponse(data, content_type="application/json")

@require_http_methods(["POST"])
def move_money(request):
    json_data = json.loads(request.body)
    idAccountFrom = json_data["accountFrom"]
    listAccountTo = json_data["accountsTo"]
    sum = float(json_data["sum"])

    return JsonResponse({'result': accountService.move_money(idAccountFrom, listAccountTo, sum)})
