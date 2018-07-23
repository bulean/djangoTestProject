from .models import Account


class AccountService():

    # возвращаем список всех аккаунтов
    def get_all_accounts(self):
        return Account.objects.all()

    # получение спискапо инн
    def get_accounts_by_inn(self, inn):
        return Account.objects.filter(inn__exact=inn)

    # перевод средств со счета на счета
    def move_money(self, idFrom, listIdsTo, amount):

        if self.check_balance(idFrom, amount):
            sum_to_move = amount/len(listIdsTo)

            return 1
        else:
            return 0

    # проверка баланса на счету
    def check_balance(self, idAccount, checkSum):

        currentSum = Account.objects.get(id=idAccount).balance

        if checkSum > currentSum:
            return False

        return True

    # проверка что id с которого переводим нету в списках на кого переводим
    def check_id_not_in_list(self):
        return False

