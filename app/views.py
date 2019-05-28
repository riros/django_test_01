from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework_json_api.django_filters import DjangoFilterBackend
from rest_framework_json_api.filters import OrderingFilter, QueryParameterValidationFilter
from rest_framework_json_api.pagination import JsonApiPageNumberPagination
from rest_framework_json_api.views import ModelViewSet

from rest_framework_json_api.exceptions import exceptions

from app.models import *
from rest_framework.decorators import action

from app.serializers import (
    EUserSerializer, CashTransactionSerializer
)


class EUserViewSet(ModelViewSet):
    queryset = EUser.objects.all().order_by('id')
    serializer_class = EUserSerializer

    filter_backends = (
        QueryParameterValidationFilter, OrderingFilter,
        DjangoFilterBackend, SearchFilter
    )
    ordering_fields = ('username',)

    rels = ('exact', 'iexact',
            'contains', 'icontains',
            'gt', 'gte', 'lt', 'lte',
            'in', 'regex', 'isnull',)
    filterset_fields = {
        'id': ('exact', "in"),
        'username': rels,
        'email': rels,
    }
    search_fields = ('username',)

    @action(detail=True, name="Transfer Money")
    def transfer_money(self, request: Request, pk=None):
        if len(request.query_params) == 0:
            return Response({
                "result": "ok", "pk": pk,
                "description": "Позволяет переводить деньги для другого пользователя,"
                               " или для ползователей с одинковым ИНН",
                "syntax": r"/?amount=[0-9\\.]+&to_user=[a-z0-9-]*&tin=[a-z0-9-]*"
            })
        else:
            eu = EUser.objects.get(id=pk)
            qp = request.query_params
            if qp.get('amount'):
                if qp.get('to_user') and EUser.objects.filter(id=qp.get('to_user')).exists():

                    if eu.make_transfer(qp.get('amount'), user=EUser.objects.get(id=qp.get('to_user'))):

                        return Response({
                            "result": "ok", "pk": pk,
                        })
                    else:
                        exceptions.ErrorDetail("Unable transfer money...")

                elif qp.get('tid'):
                    if eu.make_transfer(qp.get('amount'), inn=qp.get('tid')):
                        return Response({
                            "result": "ok", "pk": pk,
                        })
                    else:
                        exceptions.ErrorDetail("Unable transfer money...")

                else:

                    raise exceptions.ValidationError("Не указан ни to_user, ни tid")
            else:
                raise exceptions.ValidationError("Не указано значение amount")


class CashTransactionViewSet(ModelViewSet):
    queryset = CashTransaciton.objects.all().order_by('tid')
    serializer_class = CashTransactionSerializer

    prefetch_for_includes = {
        '__all__': [],
        'src': ['src__id'],
        'dst': ['src__id']

    }

    filter_backends = (
        QueryParameterValidationFilter, OrderingFilter,
        DjangoFilterBackend, SearchFilter
    )
    ordering_fields = ('tid', 'val', 'src', 'dst')

    rels = ('exact', 'iexact',
            'contains', 'icontains',
            'gt', 'gte', 'lt', 'lte',
            'in', 'regex', 'isnull',)
    filterset_fields = {
        'tid': ('exact', "in"),
        'val': rels,
        'src': ('exact', 'in'),
        'dst': ('exact', 'in'),
        'active': ('exact',),
    }
    search_fields = ('tid', 'active')
    allowed_methods = ['GET', 'HEAD', 'OPTIONS']


class NoPagination(JsonApiPageNumberPagination):
    page_size = None
