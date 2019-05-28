from django.utils.translation import ugettext_lazy as _

from rest_framework_json_api import serializers

from app.models import EUser, CashTransaciton


class EUserSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    def get_balance(self, user_inst):
        a = 1
        return user_inst.balance

    class Meta:
        model = EUser
        fields = ('url',
                  'id',
                  "inn",
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

    def create(self, v_data):
        if v_data['src'] and EUser.objects.get(id=v_data['src'].id).balance < v_data["val"]:
            raise serializers.ValidationError(_(f"Not enough user ({v_data.src.get_full_name()}) money"))

        if not v_data['src'] and not v_data['dst']:
            raise serializers.ValidationError(_(f"no src and no dst. Empty."))

        return super(CashTransactionSerializer, self).create(v_data)

    def update(self, v_data):
        if v_data['src'] and EUser.objects.get(id=v_data['src'].id).balance < v_data["val"]:
            raise serializers.ValidationError(_(f"Not enough user ({v_data.src.get_full_name()}) money"))

        if not v_data['src'] and not v_data['dst']:
            raise serializers.ValidationError(_(f"no src and no dst. Empty."))

        return super(CashTransactionSerializer, self).update(v_data)
