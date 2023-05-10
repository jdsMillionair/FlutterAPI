import json

from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder



def monthlysalesViews(request):
    with connection.cursor() as cursor:
        cursor.execute(
                        " SELECT "
                        "         LEFT (A.SADATE, 6) AS SADATE "
                        "         ,A.SAITEM "
                        "         ,B.ITNAME "
                        "         ,FORMAT(CAST(SUM(A.SAAMTS) AS signed integer),0) AS SAAMTS "
                        " FROM ossalep A "
                        " LEFT OUTER JOIN ositemp B "
                        " ON A.SAITEM = B.ITITEM "
                        " WHERE A.SADATE LIKE '%2023%' "
                        " GROUP BY A.SAITEM "
        )
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"salesdt": all[0], "salesitemnbr": all[1], "salesitemnme": all[2], "salesamount": all[3]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")


def monthlysalessumViews(request):
    with connection.cursor() as cursor:
        cursor.execute(
                        " SELECT "
                        "         CONCAT(SUBSTR(A.SADATE, 1,4), '-', SUBSTR(A.SADATE, 5,2)) AS SADATE "
                        "         ,FORMAT(CAST(SUM(A.SAAMTS) AS signed integer),0) AS SAAMTS "
                        " FROM ossalep A "
                        " LEFT OUTER JOIN ositemp B "
                        " ON A.SAITEM = B.ITITEM "
                        " GROUP BY LEFT (A.SADATE, 6) "

        )
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"salesdt": all[0], "salessum": all[1]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")