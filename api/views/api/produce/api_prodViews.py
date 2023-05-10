import json

from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder

def EquipList(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT FACT_NBR AS FACT_NBR, FACT_NME AS FACT_NME FROM mis1tb006 ORDER BY FACT_NME ASC")
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"factnbr": all[0], "factnme": all[1]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")

def EmpList(request):
    with connection.cursor() as cursor:
        cursor.execute(
                       " SELECT A.EMP_NBR, A.EMP_NME FROM pis1tb001 A "
                        )
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"empnbr": all[0], "empnme": all[1]})
        return HttpResponse(json.dumps(result_list, ensure_ascii=False, cls=DjangoJSONEncoder), content_type="application/json")



# 생산결과 저장
def apiProdItemSaveViews(request):

    body_data = request.body

    body_text = body_data.decode('utf-8')
    body_json = json.loads(body_text)


    prodqty = body_json.get('prodqty')
    prodbqty = body_json.get('prodbqty')
    prodgqty = body_json.get('prodgqty')
    prodemp = body_json.get('empnbr')
    factnbr = body_json.get('factnbr')

    with connection.cursor() as cursor:
        cursor.execute(
                           " INSERT INTO pop_prod "
                           " ( "
                           "     JOB_DATE "
                           "     ,JOB_SEQ "
                           "     ,PROD_QTY "
                           "     ,BAD_QTY "
                           "     ,GOOD_QTY "
                           "     ,PROD_EMP "
                           "     ,PROD_FACT "
                           " ) "
                           " VALUES "
                           " ( "
                           "     (SELECT DATE_FORMAT(NOW(), '%Y%m%d') AS JOB_DATE) "
                           "     ,(SELECT IFNULL(MAX(A.JOB_SEQ) + 1, 1) AS JOB_SEQ FROM pop_prod A WHERE job_date = (SELECT DATE_FORMAT(NOW(), '%Y%m%d') AS JOB_DATE)) "
                           "     ,'" + prodqty + "' "
                           "     ,'" + prodbqty + "' "
                           "     ,'" + prodgqty + "' "
                           "     ,'" + prodemp + "' "
                           "     ,'" + factnbr + "' "
                           " ) "
                       )
        connection.commit()
