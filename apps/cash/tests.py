from django.test import TestCase, tag

from apps.api.factories import EUserFactory
from base.models import EUser
from apps.cash.models import CashTransaciton


class CashTransactionTestCase(TestCase):
    def setUp(self):
        self.user_src: EUser = EUserFactory(username="testsrc", tin="0")
        self.user_dst1: EUser = EUserFactory(username="testdst1", tin="1")
        self.user_dst2: EUser = EUserFactory(username="testdst2", tin="1")

    @tag("Финансовые операции")
    def test_cash_transfers(self):
        self.cash_credit = CashTransaciton.objects.create(
            val=125,
            dst=self.user_src
        )

        self.cash_debt = CashTransaciton.objects.create(
            val=1,
            src=self.user_src
        )

        self.assertIsInstance(self.cash_credit, CashTransaciton)
        self.assertIsInstance(self.cash_debt, CashTransaciton)

        self.assertEqual(True, self.user_src.make_transfer(1, self.user_dst1))

        self.assertEqual(True, self.user_src.make_transfer(19.99, tin="1"))

        self.assertEqual(103.02, self.user_src.balance)
        self.assertEqual(10.99, self.user_dst1.balance)
        self.assertEqual(9.99, self.user_dst2.balance)
