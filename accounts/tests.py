from _decimal import Decimal

from django.test import TestCase

# Create your tests here.
from django.test.utils import setup_test_environment

from accounts.models import Account
from accounts.services import AccountService


class AccountServiceTests(TestCase):

    def setUp(self):
      Account.objects.create(first_name="lion", last_name="roar", inn=1234567, balance=100)

    def test_check_balance_on_account(self):
        # test_account = Account.objects.get(inn=1234567)
        # если сумма на счете больше или равна сумме которую мы должны переводим - True, иначе False
        self.assertEquals(AccountService().check_balance(100, 90), True)
        self.assertEquals(AccountService().check_balance(90, 100), False)
        self.assertEquals(AccountService().check_balance(0, 0), True)

    def test_get_sum_to_each_account(self):
        self.assertEquals(AccountService().get_sum_to_each_account(100, 10), 10)
        self.assertEquals(AccountService().get_sum_to_each_account(10, 4), 2.5)
        self.assertEquals(AccountService().get_sum_to_each_account(1, 4), 0.25)
        self.assertEquals(AccountService().get_sum_to_each_account(1, 3), 0.33)

    def test_decrease_balance_on_account(self):
        account = Account.objects.get(inn__exact=1234567)
        account.balance = 100
        AccountService().decrease_balance_on_account(account, 10)
        self.assertEquals(account.balance, 90)
        AccountService().decrease_balance_on_account(account, 0)
        self.assertEquals(account.balance, 90)
        AccountService().decrease_balance_on_account(account, 0.01)
        self.assertEquals(account.balance, Decimal(89.99).quantize(Decimal("1.00")))

    #todo
    def test_move_money(self):
        self.assertEquals(True,False)



