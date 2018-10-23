# -*- coding: utf-8 -*-
__author__ = 'YongCong Wu'
# @Time    : 2018/10/23 15:05
# @Email   :  : 1922878025@qq.com
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from app import models


class FirstAuthtication(BasicAuthentication):
    def authenticate(self, request):
        pass

    def authenticate_header(self, request):
        pass


class Authtication(BasicAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest framework内部将整个两个字段赋值给request，以供后续操作使用。
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass
