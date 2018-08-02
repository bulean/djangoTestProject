from _decimal import Decimal

from django.test import TestCase

# Create your tests here.
from django.test.utils import setup_test_environment

from accounts.models import Account
from accounts.services import AccountService


class AccountServiceTests(TestCase):

    def setUp(self):
        Account.objects.create(pk=1, first_name="lion1", last_name="roar1", inn=1231, balance=100)
        Account.objects.create(pk=2, first_name="lion2", last_name="roar2", inn=1232, balance=50)
        Account.objects.create(pk=3, first_name="lion3", last_name="roar3", inn=1233, balance=0)
        Account.objects.create(pk=4, first_name="lion4", last_name="roar4", inn=1234, balance=10)

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
        account = Account.objects.get(pk=1)
        AccountService().decrease_balance_on_account(account, 10)
        self.assertEquals(account.balance, 90)
        AccountService().decrease_balance_on_account(account, 0)
        self.assertEquals(account.balance, 90)
        AccountService().decrease_balance_on_account(account, 0.01)
        self.assertEquals(account.balance, Decimal(89.99).quantize(Decimal("1.00")))

    def test_move_money(self):

        account1 = Account.objects.get(pk=1)
        account2 = Account.objects.get(pk=2)
        account3 = Account.objects.get(pk=3)
        account4 = Account.objects.get(pk=4)

        result = AccountService().move_money(account1.id, [account2.id, account3.id, account4.id], 1)

        # перечитаем объекты
        account1 = Account.objects.get(pk=1)
        account2 = Account.objects.get(pk=2)
        account3 = Account.objects.get(pk=3)
        account4 = Account.objects.get(pk=4)

        self.assertEquals(result > 0, True)

        print("account1.balance =" + str(account1.balance))

        self.assertEquals(account1.balance, Decimal(99.01).quantize(Decimal("1.00")))
        self.assertEquals(account2.balance, Decimal(50.33).quantize(Decimal("1.00")))
        self.assertEquals(account3.balance, Decimal(0.33).quantize(Decimal("1.00")))
        self.assertEquals(account4.balance, Decimal(10.33).quantize(Decimal("1.00")))

        # проверим на пустой список
        result = AccountService().move_money(account1.id, [], 1)
        self.assertEquals(result, -1)

        # счет с которого переводим не может быть среди тех на который переводим
        result = AccountService().move_money(account1.id, [account1.id], 1)
        self.assertEquals(result, -2)

        # положительная сумма перевода
        result = AccountService().move_money(account1.id, [account2.balance], 0)
        self.assertEquals(result, -3)

        # счет с которого списываем не существует
        result = AccountService().move_money(0, [account2.balance], 1)
        self.assertEquals(result, -4)

        # на счете достаточно средств
        result = AccountService().move_money(account1.id, [account2.id], 999)
        self.assertEquals(result, -5)

        # все получатели существуют
        result = AccountService().move_money(account1.id, [0], 1)
        self.assertEquals(result, -6)


