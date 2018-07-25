from django.db import transaction, DatabaseError
from django.db.models import F

from .models import Account


class AccountService():

    # возвращаем список всех аккаунтов
    def get_all_accounts(self):
        return Account.objects.all()

    # получение спискапо инн
    def get_accounts_by_inn(self, inn):
        return Account.objects.filter(inn__exact=inn)

    # перевод средств со счета на счета - одна транзакция
    @transaction.atomic
    def move_money(self, idFrom, listIdsTo, amount):

        print('call move money')
        print('idFrom = ' + str(idFrom))
        print('listIdsTo = ' + str(listIdsTo))
        print('amount = ' + str(amount))

        # достанем аккаунт с которого нужно списать
        try:
            accountFrom = Account.objects.get(pk=idFrom)
        except Account.DoesNotExist:
            return -2

        print(accountFrom)

        # to do если такого пользователя нет

        if self.check_balance(accountFrom.balance, amount):
            sum_to_move = amount / len(listIdsTo)
            accountFrom.balance = accountFrom.balance - amount
        else:
            return 0

        print('balance check')

        try:
            with transaction.atomic():
                accountFrom.save()
                Account.objects.filter(id__in=listIdsTo).update(balance=F('balance') + sum_to_move)
                return 1
        except DatabaseError:
            return -1

    # проверка баланса на счету
    def check_balance(self, accountBalance, checkSum):

        print("in check balance")

        if checkSum > accountBalance:
            return False

        return True

    # проверка что id с которого переводим нету в списках на кого переводим
    def check_id_not_in_list(self):
        return False
