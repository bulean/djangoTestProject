from decimal import Decimal

from django.db import transaction, DatabaseError
from django.db.models import F

from .models import Account

import logging

logger = logging.getLogger("account_service")


class AccountService():

    # возвращаем список всех аккаунтов
    def get_all_accounts(self):
        return Account.objects.all()

    # получение списка по инн
    def get_accounts_by_inn(self, inn):
        return Account.objects.filter(inn__exact=inn)

    # перевод средств со счета на счета - одна транзакция
    @transaction.atomic
    def move_money(self, idFrom, listIdsTo, amount):

        logger.debug("call move_money:" + "idFrom = " + str(idFrom) + ";" + "listIdsTo = " + str(
            listIdsTo) + ";" + "amount =" + str(amount))

        # проверим что есть список аккаунтов куда переводить не пуст
        lengthList = len(listIdsTo)
        if lengthList == 0:
            return -1

        # проверим что сумма положительная
        if amount <= 0:
            return -2

        # достанем аккаунт с которого нужно списать
        try:
            accountFrom = Account.objects.get(pk=idFrom)
        except Account.DoesNotExist:
            return -2

        if self.check_balance(accountFrom.balance, amount):
            sum_to_move = self.get_sum_to_each_account(amount, lengthList)
            self.decrease_balance_on_account(accountFrom, sum_to_move * lengthList)
        else:
            return 0

        try:
            with transaction.atomic():
                accountFrom.save()
                Account.objects.filter(id__in=listIdsTo).update(balance=F('balance') + sum_to_move)
                return 1
        except DatabaseError:
            logger.error("error on move money")
            return -1

    # проверка баланса на счету
    def check_balance(self, accountBalance, checkSum):
        if checkSum > accountBalance:
            return False

        return True

    # проверка что id с которого переводим нету в списках на кого переводим
    def check_id_not_in_list(self):
        return False

    # возвращаем сумму для каждого аккаунта, проверка деления на 0 делается перед вызовом
    def get_sum_to_each_account(self, sumToMove, cntAccounts):
        # округляем до 2-х знаком после ,
        return round(sumToMove / cntAccounts, 2)

    def decrease_balance_on_account(self, account, addSum):
        print("addSum = " + str(addSum))
        print("account.balance = " + str(account.balance))
        account.balance = Decimal(account.balance - Decimal(addSum)).quantize(Decimal("1.00"))
