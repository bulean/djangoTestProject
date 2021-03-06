var accounts = [];
var accountFrom = undefined;
var accountsTo = undefined;


function transformServerAccountModel(pAccount) {
    return {
        id: pAccount.pk,
        first_name: pAccount.fields.first_name,
        last_name: pAccount.fields.last_name,
        inn: pAccount.fields.inn,
        balance: pAccount.fields.balance
    };
}

function getStrByUserModel(pAccount) {
    return "id = " + pAccount.id + " " + pAccount.first_name + " " + pAccount.last_name + " " + "(инн = " + pAccount.inn + ")" + " (баланс = " + pAccount.balance + ")";
}

function getAllAccounts() {
    $.ajax({
        url: 'getAccounts',
        dataType: "json",
        success: function (data, textStatus) {

            accounts = [];

            $.each(data, function (key, value) {

                var tmpAccount = transformServerAccountModel(value);

                accounts[tmpAccount.id] = tmpAccount;

                $('#selectAccountsList').append($('<option>', {
                    value: tmpAccount.id,
                    text: getStrByUserModel(tmpAccount)
                }));

                // заполним autocomplete списком
                fill_select_list_accounts(accounts);

            });


        },
        error: function () {
            printResult("Не удалось получить список аккаунтов");
        }
    });
}

function printResult(text) {
    $("#result").text(text);

    setTimeout(function () {
        $('#result').text("");
    }, 4000);
}

function clearForm() {
    getAllAccounts();
    $("#resSearch").text('');
    $("#from").text();
    $("#inn").val("");
    $("#accountsList").val("");
    $("#sum").val("");
    accountFrom = undefined;
    accountsTo = undefined;
}

function fill_select_list_accounts(pAccounts) {

    var availableTags = [];

    for (key in pAccounts) {
        availableTags.push({
            label: getStrByUserModel(pAccounts[key]),
            value: key
        });
    }

    $("#accountsList").autocomplete({
        source: availableTags,
        select: function (event, ui) {
            event.preventDefault();
            $(this).val(getStrByUserModel(accounts[ui.item.value]));
            accountFrom = Number(ui.item.value);
        }
    });
}

$(function () {

    // после загрузки страницы подготовим список аккаунтов
    getAllAccounts();

    $("#clearForm").click(function () {
        clearForm()
    });

    $("#inn").bind("change keyup input click", function () {

            if (this.value.match(/[^0-9]/g)) {
                this.value = this.value.replace(/[^0-9]/g, '');
            }
        }
    );

    $("#sum").bind("change keyup input click", function () {

            if (this.value.match(/[^0-9]/g)) {
                this.value = this.value.replace(/[^0-9]/g, '');
            }
        }
    );

    // перевод со счета на счета
    $("#moveMoneyBtn").click(function () {

        var sum = $("#sum").val();

        // проверим что указана сумма и отлично от нуля
        if (sum == undefined || sum <= 0) {
            printResult("Укажите сумму перевода!");
            return;
        }

        // проверим что указан счет для списания
        if (accountFrom == undefined) {
            printResult("Укажите счет для списания!")
            return;
        }

        // проверим что указан счет куда переводить
        if (accountsTo == undefined) {
            printResult("Укажите счет куда переводить!")
            return;
        }

        // проверим что счет с  которого переводим не числится среди тех куда переводим
        if ($.inArray(accountFrom, accountsTo) != -1) {
            printResult("Нельзя переводить со счета на тот же счет!");
            return;
        }


        if (accounts[accountFrom].balance < sum) {
            printResult("На выбранном счету не достаточно средств!");
            return;
        }

        var dataSend = {};

        dataSend.accountFrom = accountFrom;
        dataSend.accountsTo = accountsTo;
        dataSend.sum = sum;

        $.ajax({
            url: 'moveMoney',
            dataType: "json",
            data: JSON.stringify(dataSend),
            method: 'POST',
            success: function (data, textStatus) {


                if (data.result != 1) {
                    printResult("Не удалось осуществить перевод")
                    return;
                }

                printResult("Перевод осуществлен");
                clearForm();
            },
            error: function () {
                printResult("Не удалось осуществить перевод")
            }
        });
    });

    // поиск аккаунтов по инн
    $("#search").click(function () {

        printResult("");

        elem = $("#inn");

        inn = elem.val();

        // проверим что инн указан
        if (inn == undefined || inn == "") {
            printResult("Укажите ИНН!");
            elem.focus();

            return;
        }

        const textErr = "Не удалось найти счет по указанному инн";

        $.ajax({
            url: 'getAccountsByInn/' + inn,
            dataType: "json",
            success: function (data) {

                // проверим что что-то нашлось
                if (data.length == 0) {

                    printResult(textErr)
                    return;
                }

                accountsTo = [];

                $("#resSearch").text('');

                $.each(data, function (key, value) {
                    $("#resSearch").append($('<li>').append(getStrByUserModel(transformServerAccountModel(value))));
                    accountsTo.push(Number(value.pk));
                });
            },
            error: function () {
                printResult(textErr)
            }
        });
    });

});




