from django.utils.translation import ugettext_lazy as _

# from rest_framework_json_api import serializers

from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from base.models import EUser
from apps.cash.models import CashTransaciton


class EUserSerializer(serializers.HyperlinkedModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, user_inst):
        return user_inst.balance

    class Meta:
        model = EUser
        fields = ('url',
                  'id',
                  "tin",
                  "balance",
                  'updated_at',
                  'created_at',
                  "email",
                  "username",
                  "is_active",
                  "is_staff")


class CashTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashTransaciton
        fields = '__all__'

    @staticmethod
    def _check(v_data):
        if v_data['src'] and EUser.objects.get(id=v_data['src'].id).balance < v_data["val"]:
            raise serializers.ValidationError(_(f"Not enough user ({v_data.src.get_full_name()}) money"))

        if not v_data['src'] and not v_data['dst']:
            raise serializers.ValidationError(_(f"no src and no dst. Empty."))

    def create(self, v_data):
        self._check(v_data)
        return super(CashTransactionSerializer, self).create(v_data)

    def update(self, inst: EUser, v_data):
        self._check(v_data)

        return super(CashTransactionSerializer, self).update(inst, v_data)
