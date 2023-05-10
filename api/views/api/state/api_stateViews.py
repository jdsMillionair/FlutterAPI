import json

from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder

def StateList(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS COUNT ")
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"statecount": all[0]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")