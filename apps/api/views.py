from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.exceptions import APIException as MyException

from rest_framework.decorators import action

from base.models import EUser
from apps.cash.models import CashTransaciton

from apps.api.serializers import (
    EUserSerializer, CashTransactionSerializer
)

from rest_framework import routers, serializers, viewsets, generics


class LargeResultSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SmallResultSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class NoPagination(PageNumberPagination):
    page_size = None


class EUserViewSet(viewsets.ModelViewSet):
    # class EUserViewSet(generics.ListAPIView):
    queryset = EUser.objects.all()
    serializer_class = EUserSerializer

    pagination_class = SmallResultSetPagination
    # filter_backends = (
    #     QueryParameterValidationFilter, OrderingFilter,
    #     DjangoFilterBackend, SearchFilter
    # )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ('username',)

    rels = ('exact', 'iexact',
            'contains', 'icontains',
            'gt', 'gte', 'lt', 'lte',
            'in', 'regex', 'isnull',)
    filterset_fields = {
        'id': ('exact', "in"),
        'username': ('icontains',),
        'email': rels,
    }
    search_fields = ('username',)

    @action(detail=True, name="Transfer Money")
    def transfer_money(self, request: Request, pk=None):
        if len(request.query_params) == 0:
            return Response({
                "pk": pk,
                "description": "Позволяет переводить деньги для другого пользователя,"
                               " или для ползователей с одинковым ИНН",
                "syntax": r"?amount=[0-9\\.]+&to_user=[a-z0-9-]*&tin=[a-z0-9-]*"
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
                        MyException("Unable transfer money...")

                elif qp.get('tin'):
                    if eu.make_transfer(qp.get('amount'), tin=qp.get('tin')):
                        return Response({
                            "result": "ok", "pk": pk,
                        })
                    else:
                        MyException("Unable transfer money...")

                else:

                    raise MyException("Не указан ни to_user, ни tin")
            else:
                raise MyException("Не указано значение amount")

    @action(detail=True, name='Add cash')
    def add_money(self, request: Request, pk=None):

        if len(request.query_params) == 0:
            return Response({
                "pk": pk,
                "description": "Добавить денег",
                "syntax": r"?amount=[0-9\\.]+&tin=[a-z0-9-]*"
            })
        else:
            eu = EUser.objects.get(id=pk)
            qp = request.query_params
            if qp.get('amount'):
                eu.make_receipt(qp.get('amount'))
                return Response({
                    "result": "ok", "pk": pk,
                })
            else:
                raise MyException("Не указано значение amount")


class CashTransactionViewSet(viewsets.ModelViewSet):
    queryset = CashTransaciton.objects.all().order_by('tid')
    serializer_class = CashTransactionSerializer

    prefetch_for_includes = {
        '__all__': [],
        'src': ['src__id'],
        'dst': ['src__id']

    }

    # filter_backends = (
    #     QueryParameterValidationFilter, OrderingFilter,
    #     DjangoFilterBackend, SearchFilter
    # )
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
