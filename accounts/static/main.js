var accountFrom = undefined;
var accountsTo = undefined;


function getStrByUserModel(value) {
    return value.fields.first_name + " " + value.fields.last_name + " " + "(инн = " + value.fields.inn + ")" + " (баланс = " + value.fields.balance + ")";
}

function getAllAccounts() {
    $.ajax({
        url: 'getAccounts',             // указываем URL и
        dataType: "json",                     // тип загружаемых данных
        success: function (data, textStatus) { // вешаем свой обработчик на функцию success

            console.log(data);

            $.each(data, function (key, value) {
                $('#selectAccountsList').append($('<option>', {
                    value: value.pk,
                    text: getStrByUserModel(value)
                }));
            });
        }
    });
};

function printResult(text) {
    $("#result").text(text);
}


function clearForm() {
    getAllAccounts();
    $("#resSearch").text('');
    $("#from").text();
    accountFrom = undefined;
    accountsTo = undefined;
}

$(function () {

    // после загрузки страницы подготовимсписок аккаунтов
    getAllAccounts();

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

        var dataSend = {};

        dataSend.accountFrom = accountFrom;
        dataSend.accountsTo = accountsTo;
        dataSend.sum = sum;

        console.log(dataSend);

        $.ajax({
            url: 'moveMoney',
            dataType: "json",
            data: JSON.stringify(dataSend),
            method: 'POST',
            success: function (data, textStatus) {
                printResult("Перевод осуществлен");
                clearForm();
                console.log(data);
            },
            error: function () {
                printResult("Не удалось осуществить перевод")
            }
        });
    });


    // выбор аккаунта из списка
    $("#selectAccountsList").click(function () {

        console.log("click select on accountsList");

        accountFrom = $("#selectAccountsList option:selected").val();
        console.log("accountFrom = " + accountFrom);
        $("#from").text($("#selectAccountsList option:selected").text());
    });


    // поиск аккаунтов по инн
    $("#search").click(function () {


        console.log("click search by inn");

        elem = $("#inn");

        inn = elem.val();

        console.log("inn = " + inn);

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
                    $("#resSearch").append($('<li>').append(getStrByUserModel(value)));
                    accountsTo.push(value.pk);
                });

                console.log("accountsTo = " + accountsTo);
            },
            error: function () {
                printResult(textErr)
            }
        });
    });

});




