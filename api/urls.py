from django.urls import path
from api.views.api.account import api_loginViews
from api.views.api.base import api_empViews
from api.views.api.sales import api_salesViews
from api.views.api.produce import api_prodViews
from api.views.api.state import api_stateViews


urlpatterns = [

    path('api_state/', api_stateViews.StateList, name="api_state"), #상태체크

    path('api_csrftoken/', api_loginViews.apicsrf, name="api_csrftoken"),
    path('api_login/', api_loginViews.apiloginViews, name="api_login"),
    path('api_login_save/', api_loginViews.apiloginSaveViews, name="api_login_save"),
    path('api_login_attand_save/', api_loginViews.apiAttendInOutSaveViews, name="api_login_attand_save"), #출퇴근시간저장


    # API 직원관리
    path('api_empmng/', api_empViews.emplistViews, name="api_empmng"),  # 직원 정보
    path('api_empworkinoutlist/', api_empViews.empworkinoutViews, name="api_empworkinoutlist"),  # 직원 출근 현황

    # API 월별매출관리(현황)
    path('api_monthlysalesmng/', api_salesViews.monthlysalesViews, name="api_monthlysalesmng"),  # 월별로 아이템별 현황
    path('api_monthlysalessummng/', api_salesViews.monthlysalessumViews, name="api_monthlysalessummng"),  # 월별로 아이템별 현황


    # API 생산관리(현황)
    path('api_equip_list/', api_prodViews.EquipList, name="api_equip_list"),
    path('api_emp_list/', api_prodViews.EmpList, name="api_emp_list"),
    path('api_prod_mng_save/', api_prodViews.apiProdItemSaveViews, name="api_prod_mng_save"),


    # path('login/', loginViews.loginViews, name="login"),
    #
    # path('empworkinoutlist/', baseempViews.empworkinoutViews, name="empworkinoutlist"),

]
