import json

from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder



def emplistViews(request):
    with connection.cursor() as cursor:
        cursor.execute(
                       " SELECT "
                       "       A.EMP_NBR "
                       "      ,A.EMP_NME "
                       "      ,A.EMP_DEPT "
                       "      ,B.RESNAM AS DEPT_NM "
                       " FROM pis1tb001 A "
                       " LEFT OUTER JOIN osrefcp B "
                       " ON B.RECODE = 'DPT' "
                       " AND A.EMP_DEPT = B.RESKEY "
        )
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"empnbr": all[0], "empnme": all[1], "empdept": all[2], "empdeptnm": all[3]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")

def empworkinoutViews(request):
    with connection.cursor() as cursor:
        cursor.execute(
                       " SELECT "
                       "         A.EMP_NBR "
                       "         ,B.EMP_NME "
                       "         ,A.EMP_IN_OUT "
                       "         ,C.RESNAM "
                       "         ,A.EMP_IN_DTE "
                       "         ,IFNULL(A.EMP_OUT_DTE,'') AS EMP_OUT_DTE "
                       " FROM pis1tb002 A "
                       " LEFT OUTER JOIN pis1tb001 B "
                       " ON A.EMP_NBR = B.EMP_NBR "
                       " LEFT OUTER JOIN osrefcp C "
                       " ON C.RECODE = 'WIO' "
                       " AND A.EMP_IN_OUT = C.RESKEY "
        )
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"empnbr": all[0], "empnme": all[1], "empinout": all[2], "empinoutnm": all[3], "indte": all[4], "outdte": all[5]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")