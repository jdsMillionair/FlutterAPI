import json

from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.middleware.csrf import get_token


#-*- coding: utf-8 -*-
#!/bin/env python

# 로그인 정보
def apiloginViews(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT EMP_NBR, EMP_PASS FROM pis1tb001 ")
        results = cursor.fetchall()

        result_list = []
        for all in results:
            result_list.append({"empid": all[0], "emppw": all[1]})

        # return JsonResponse(result_list, safe=False)
        return HttpResponse(json.dumps(result_list, ensure_ascii=False), content_type="application/json")




def apicsrf(request):
    csrf_token = get_token(request)
    response = JsonResponse({'csrf_token': csrf_token})
    response['X-CSRFToken'] = csrf_token
    return response



# 회원가입(?)
def apiloginSaveViews(request):

    body_data = request.body

    body_text = body_data.decode('utf-8')
    body_json = json.loads(body_text)

    id = body_json.get('id')
    pw = body_json.get('pw')

    with connection.cursor() as cursor:
        cursor.execute(
                           "INSERT INTO pis1tb001 "
                           "("
                           "    EMP_NBR "
                           "    ,EMP_NME "
                           "    ,EMP_PASS "
                           "    ,EMP_DEPT "
                           "    ,CRE_DT "
                           "    ,CRE_USER "
                           ") "
                           "VALUES"
                           "("
                           "    '" + id + "'"
                           "    ,'TEST' "
                           "    ,'" + pw + "'"
                           "    ,'101'"
                           "    ,NOW() "
                           "    ,'" + id + "'"
                           ")"
                       )
        connection.commit()


# 근태(출퇴근)
def apiAttendInOutSaveViews(request):

    body_data = request.body

    body_text = body_data.decode('utf-8')
    body_json = json.loads(body_text)

    empid = body_json.get('id') #이거 대신 session을 가져와서 하기

    with connection.cursor() as cursor:
        cursor.execute(
                           "INSERT INTO pis1tb002 "
                           "("
                           "    SEQ "
                           "    ,EMP_NBR "
                           "    ,EMP_IN_OUT "
                           "    ,EMP_DEPT "
                           "    ,EMP_GBN "
                           "    ,EMP_IN_OUT "
                           "    ,EMP_IN_DTE "
                           ") "
                           "VALUES"
                           "("
                           "    ,(SELECT IFNULL(MAX(A.SEQ) + 1, 1) AS SEQ FROM pis1tb002 A WHERE A.EMP_IN_OUT = (SELECT DATE_FORMAT(NOW(), '%Y%m%d'))) "
                           "    '" + empid + "'"
                           "    ,(SELECT DATE_FORMAT(NOW(), '%Y%m%d')) "
                           "    ,(SELECT EMP_DEPT FROM pis1tb001 WHERE EMP_NBR = '" + empid + "') "
                           "    ,(SELECT EMP_GBN FROM pis1tb001 WHERE EMP_NBR = '" + empid + "')"
                           "    ,'1'"
                           "    ,NOW() "
                           ")"
                       )
        connection.commit()


