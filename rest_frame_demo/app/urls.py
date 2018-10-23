# -*- coding:utf-8 -*-


from django.conf.urls import url, include
from rest_framework import routers
from app import views



# 注册视图
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'pwd', views.GroupViewSet)



# 二级路由
urlpatterns = [
    url(r'apb/',include(router.urls)),
    url(r'1/',include(router.urls)),
    url(r'auth/$', views.GetUserData.as_view()),            # 登陆认证
    url(r'order/$', views.OrderView.as_view())               # 订单
]