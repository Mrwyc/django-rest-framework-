from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from app.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions
from django.http import JsonResponse
from app import models
import hashlib
import time

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# 生成md5
def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# 请求Token认证
class GetUserData(APIView):
    """
    用于用户登陆认证
    """
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
        try:
            user = request._request.POST.get('username')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为当前登陆用户创建Token
            token = md5(user)
            models.UserToken.objects.update_or_create(user=obj, defaults={'token':token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        return JsonResponse(ret)



# 测试数据
ORDER_DICT = {
    1: {
        'name': '书包',
        'sku': 1002,
        'price': 500
    },
    2: {
        'name': '键盘',
        'sku': 1052,
        'price': 258
    }
}

class OrderView(APIView):
    """
    用于订单    rest framework
    """
    # 通过authentication_classes添加用户认证
    def get(self, request, *args, **kwargs):
        """
        用户登陆成功，才可以查看订单数据
        """
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

# 用户中心
class UserInfoView(APIView):
    """
    用于订单    rest framework
    """
    # 通过authentication_classes添加用户认证
    def get(self, request, *args, **kwargs):
        return HttpResponse('用户信息')