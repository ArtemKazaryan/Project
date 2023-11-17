# Импортируем функции рендеринга, перенапрвления и получения объекта модели из пакета функций быстрого доступа
from django.shortcuts import render, redirect, get_object_or_404

# Импортируем стандартные формы создания пользователя и его аутентификации из подпакета forms пакета auth
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Импортируем стандартную модель пользователя из подпакета models пакета auth
from django.contrib.auth.models import User

# Импортируем функции создания пользователя и его аутентификации из пакета auth
from django.contrib.auth import login, logout, authenticate

# Импортируем функцию отслеживания ошибки целостности при взаимодействии с БД
from django.db import IntegrityError

# Импортируем формы отображения для ввода данных в наши модели из файла forms.py
from .forms import ProfitableTransactionForm, ExpenditureTransactionForm

# Импортируем наши модели, взаимодействующие с базой данных из файла models.py
from .models import ProfitableTransaction, ExpenditureTransaction, Meter

# Импортируем стандартную функцию-декоратор, отслеживающую выполнения требования входа пользователя в систему
from django.contrib.auth.decorators import login_required

# Импортируем стандартные арифметические функции для работы с моделью при вычислениях на основе данных из БД
from django.db.models import Min, Sum, F, Avg

# Импортируем функцию даты из стандартного пакета datetime и функцию округления до меньшего целого
# из стандартного пакета math
from datetime import date
from math import floor

# Импортируем список наших функций из файла funcs.py
from .funcs import funcs


def home(request):
    return render(request, 'transaction/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'transaction/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('recorded')
            except IntegrityError:
                return render(request, 'transaction/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Пользователь с таким именем уже существует!'})

        else:
            return render(request, 'transaction/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали!'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'transaction/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'transaction/loginuser.html',
                          {'form': AuthenticationForm(),
                           'error': 'Неверные данные входа!'})
        else:
            login(request, user)
            return redirect('recorded')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def recordedtransactions(request):
    protransactions = ProfitableTransaction.objects.all().order_by('-date')
    exptransactions = ExpenditureTransaction.objects.all().order_by('-date')

    # Получение списков из queryset'ов
    valuespro_list = protransactions.values()
    valuesexp_list = exptransactions.values()

    # Задаём переменные общих размеров доходов и расходов, а также счётчики транзакций
    sumpro = 0
    sumexp = 0
    countpro = 0
    countexp = 0

    # Итерируемся по спискам
    for item in valuespro_list:
        valuepro = item['amount']
        sumpro += valuepro
        countpro += 1

    for item in valuesexp_list:
        valueexp = round(item['quantity'] * item['price'], 2)
        sumexp += valueexp
        countexp += 1

    # Вычисляем баланс нашей учётной базы
    total_balance = sumpro - sumexp

    # Получаем минимальную дату из БД по доходам
    oldest_date_pro = ProfitableTransaction.objects.aggregate(Min('date'))['date__min']
    if not oldest_date_pro:
        return 0
    # Разница между текущей датой и самой старой датой
    delta_date_pro = (date.today() - oldest_date_pro).days + 1

    # Получаем минимальную дату из БД по расходам
    oldest_date_exp = ExpenditureTransaction.objects.aggregate(Min('date'))['date__min']
    if not oldest_date_exp:
        return 0
    # Разница между текущей датой и самой старой датой
    delta_date_exp = (date.today() - oldest_date_exp).days + 1

    # Находим общий срок ведения учёта
    delta_days = [delta_date_pro, delta_date_exp]
    max_delta_days = max(delta_days)

    # Находим самую первую дату учёта
    if delta_date_pro >= delta_date_exp:
        oldest_of_oldest_dates = oldest_date_pro
    else:
        oldest_of_oldest_dates = oldest_date_exp

    # Вычисляем скорости доходов и затрат
    total_revenue_rate = round(sumpro / max_delta_days, 2)
    total_expense_rate = round(sumexp / max_delta_days, 2)
    term = floor(total_balance / total_expense_rate)

    # Вычисляем оставшиеся дни
    days_left = f'{term}'

    # Вычисляем скорость прибыли
    margin_total_rate = total_revenue_rate - total_expense_rate

    # Получаем текущую дату
    today = date.today()

    # Эта переменная для пунктира
    multidash1 = '- ' * 80
    multidash2 = '- ' * 100

    notempty = True

    if request.method == 'POST':
        try:

            from datetime import datetime
            start_date = request.POST.get('filtering-start')  # Получение значения даты из запроса
            start_date = datetime.strptime(start_date, '%Y-%m-%d')  # Преобразование строки в объект datetime
            startday = start_date.day  # Получение дня
            startmonth = start_date.month  # Получение месяца
            startyear = start_date.year  # Получение года
            finish_date = request.POST.get('filtering-finish')  # Получение значения даты из запроса
            finish_date = datetime.strptime(finish_date, '%Y-%m-%d')  # Преобразование строки в объект datetime
            finishday = finish_date.day  # Получение дня
            finishmonth = finish_date.month  # Получение месяца
            finishyear = finish_date.year  # Получение года

            protransactions = ProfitableTransaction.objects.filter(date__range=[f"{startyear}-{startmonth}-{startday}",
                                                                                f"{finishyear}-{finishmonth}-{finishday}"
                                                                                ]).order_by('-date')

            exptransactions = ExpenditureTransaction.objects.filter(date__range=[f"{startyear}-{startmonth}-{startday}",
                                                                                 f"{finishyear}-{finishmonth}-{finishday}"
                                                                                 ]).order_by('-date')
            countfiltpro = protransactions.count
            countfiltexp = exptransactions.count
            if not countfiltpro:
                countfiltpro = 0
            if not countfiltexp:
                countfiltexp = 0

            # Формируем контекст вывода на страницу
            context = {'protransactions': protransactions, 'exptransactions': exptransactions,
                       'countfiltpro': countfiltpro, 'countfiltexp': countfiltexp, 'notempty': notempty,
                       'startday': startday, 'startmonth': startmonth, 'startyear': startyear,
                       'finishday': finishday, 'finishmonth': finishmonth, 'finishyear': finishyear,
                       'sumpro': sumpro, 'sumexp': sumexp, 'countpro': countpro, 'countexp': countexp,
                       'total_revenue_rate': total_revenue_rate, 'total_expense_rate': total_expense_rate,
                       'total_balance': total_balance, 'margin_total_rate': margin_total_rate,
                       'today': today, 'max_delta_days': max_delta_days, 'days_left': days_left,
                       'oldest_of_oldest_dates': oldest_of_oldest_dates, 'multidash1': multidash1,
                       'multidash2': multidash2}
            return render(request, 'transaction/recordedtransactions.html', context)

        except ValueError:
            notempty = False
            countfiltpro = protransactions.count
            countfiltexp = exptransactions.count
            if not countfiltpro:
                countfiltpro = 0
            if not countfiltexp:
                countfiltexp = 0
            # Формируем контекст вывода на страницу
            context = {'protransactions': protransactions, 'exptransactions': exptransactions,
                       'countfiltpro': countfiltpro, 'countfiltexp': countfiltexp, 'notempty': notempty,
                       'sumpro': sumpro, 'sumexp': sumexp, 'countpro': countpro, 'countexp': countexp,
                       'total_revenue_rate': total_revenue_rate, 'total_expense_rate': total_expense_rate,
                       'total_balance': total_balance, 'margin_total_rate': margin_total_rate,
                       'today': today, 'max_delta_days': max_delta_days, 'days_left': days_left,
                       'oldest_of_oldest_dates': oldest_of_oldest_dates, 'multidash1': multidash1,
                       'multidash2': multidash2}
            return render(request, 'transaction/recordedtransactions.html', context)

    else:
        notempty = False
        countfiltpro = protransactions.count
        countfiltexp = exptransactions.count
        if not countfiltpro:
            countfiltpro = 0
        if not countfiltexp:
            countfiltexp = 0
        # Формируем контекст вывода на страницу
        context = {'protransactions': protransactions, 'exptransactions': exptransactions,
                   'countfiltpro': countfiltpro, 'countfiltexp': countfiltexp, 'notempty': notempty,
                   'sumpro': sumpro, 'sumexp': sumexp, 'countpro': countpro, 'countexp': countexp,
                   'total_revenue_rate': total_revenue_rate, 'total_expense_rate': total_expense_rate,
                   'total_balance': total_balance, 'margin_total_rate': margin_total_rate,
                   'today': today, 'max_delta_days': max_delta_days, 'days_left': days_left,
                   'oldest_of_oldest_dates': oldest_of_oldest_dates, 'multidash1': multidash1,
                       'multidash2': multidash2}
        return render(request, 'transaction/recordedtransactions.html', context)



@login_required
def transactions_special_cost_calculations(request):
    custom_range = range(0, 4)
    funcnames = ['3. Средняя цена, общее количество, общий расход и скорость расхода на все товары / услуги',
                 '4. Расчёт общего расхода, скорости расхода и доли от общих расходов по категориям товаров / услуг',
                 '5. Расчёт общего дохода, скорости дохода и доли от общих доходов по типам поступлений в процентах',
                 '6. Расчёт общего дохода, скорости дохода и доли от общих доходов по поступлениям в процентах']

    return render(request, 'transaction/special_cost_calculations.html', {'custom_range': custom_range,
                                                                          'funcnames': funcnames})


@login_required
def specialcostcalculation1(request):
    # Эта переменная для пунктира
    multidash = '- ' * 117
    if request.method == 'POST':
        input_name_value = request.POST.get('calculation1input')

        exptransactions = ExpenditureTransaction.objects.all()

        # Получаем минимальную дату из БД по доходам
        oldest_date_pro = ProfitableTransaction.objects.aggregate(Min('date'))['date__min']
        if not oldest_date_pro:
            return 0
        # Разница между текущей датой и самой старой датой
        delta_date_pro = (date.today() - oldest_date_pro).days + 1

        # Получаем минимальную дату из БД по расходам
        oldest_date_exp = ExpenditureTransaction.objects.aggregate(Min('date'))['date__min']
        if not oldest_date_exp:
            return 0
        # Разница между текущей датой и самой старой датой
        delta_date_exp = (date.today() - oldest_date_exp).days + 1

        # Находим общий срок ведения учёта
        delta_days = [delta_date_pro, delta_date_exp]
        max_delta_days = max(delta_days)

        # Получение списков из queryset'ов
        valuesexp_list = exptransactions.values()

        sumpricequantity = 0
        sumquantity = 0
        for item in valuesexp_list:
            if item['name'].lower() == input_name_value.lower():
                value = round(item['quantity'] * item['price'], 2)
                sumpricequantity += value
                value = item['quantity']
                sumquantity += value
        input_name_value = request.POST.get('calculation1input').capitalize()
        speedexp = round(sumpricequantity / max_delta_days, 2)
        consumptionrate = round(sumquantity / max_delta_days, 2)
        averageprice = round(sumpricequantity / sumquantity, 2)
        pk = 1
        context = {'averageprice': averageprice, 'input_name_value': input_name_value, 'speedexp': speedexp,
                   'consumptionrate': consumptionrate, 'pk': pk,
                   'sumpricequantity': sumpricequantity, 'sumquantity': sumquantity, 'multidash': multidash}
        return render(request, 'transaction/specialcalculation1.html', context)
    else:
        return render(request, 'transaction/specialcalculation1.html')

@login_required
def specialcostcalculation2(request):
    # Эта переменная для пунктира
    multidash = '- ' * 117
    if request.method == 'POST':
        input_name = request.POST.get('calculation2input')

        protransactions = ProfitableTransaction.objects.all()

        # Получаем минимальную дату из БД по доходам
        oldest_date_pro = ProfitableTransaction.objects.aggregate(Min('date'))['date__min']
        if not oldest_date_pro:
            return 0
        # Разница между текущей датой и самой старой датой
        delta_date_pro = (date.today() - oldest_date_pro).days + 1

        # Получаем минимальную дату из БД по расходам
        oldest_date_exp = ExpenditureTransaction.objects.aggregate(Min('date'))['date__min']
        if not oldest_date_exp:
            return 0
        # Разница между текущей датой и самой старой датой
        delta_date_exp = (date.today() - oldest_date_exp).days + 1

        # Находим общий срок ведения учёта
        delta_days = [delta_date_pro, delta_date_exp]
        max_delta_days = max(delta_days)

        # Получение списков из queryset'ов
        valuespro_list = protransactions.values()

        sumamount = 0
        for item in valuespro_list:
            if item['name'] == input_name:
                value = round(item['amount'], 2)
                sumamount += value
        input_name = request.POST.get('calculation2input')
        speedpro = round(sumamount / max_delta_days, 2)
        pk = 2
        context = {'input_name': input_name, 'speedpro': speedpro, 'pk': pk,
                   'sumamount': sumamount, 'multidash': multidash}
        return render(request, 'transaction/specialcalculation2.html', context)
    else:
        return render(request, 'transaction/specialcalculation2.html')

@login_required
def specialcostcalculation(request, pk):
    pk = str(int(pk) + 1)

    multidash = '- ' * 117
    # Получаем минимальную дату из БД по доходам
    oldest_date_pro = ProfitableTransaction.objects.aggregate(Min('date'))['date__min']
    if not oldest_date_pro:
        return 0
    # Разница между текущей датой и самой старой датой
    delta_date_pro = (date.today() - oldest_date_pro).days + 1

    # Получаем минимальную дату из БД по расходам
    oldest_date_exp = ExpenditureTransaction.objects.aggregate(Min('date'))['date__min']
    if not oldest_date_exp:
        return 0
    # Разница между текущей датой и самой старой датой
    delta_date_exp = (date.today() - oldest_date_exp).days + 1

    # Находим общий срок ведения учёта
    delta_days = [delta_date_pro, delta_date_exp]
    maxdeltadays = max(delta_days)

    # для func4 и func5
    protransactions = ProfitableTransaction.objects.all()
    valuespro_list = protransactions.values()
    sumpro = 0
    for item in valuespro_list:
        value = round(item['amount'], 2)
        sumpro += value

    # для func3
    exptransactions = ExpenditureTransaction.objects.all()
    valuesexp_list = exptransactions.values()
    sumexp = 0
    for item in valuesexp_list:
        value = round(item['quantity'] * item['price'], 2)
        sumexp += value

    return funcs[int(pk)](request, maxdeltadays, sumpro, sumexp, multidash)



@login_required
def createprotransaction(request):
    if request.method == 'GET':
        return render(request, 'transaction/createprotransaction.html', {'form': ProfitableTransactionForm()})
    else:
        try:
            form = ProfitableTransactionForm(request.POST)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/createprotransaction.html', {'form': ProfitableTransactionForm(),
                                                                             'error': 'Неверные данные!'})


@login_required
def createexptransaction(request):
    if request.method == 'GET':
        return render(request, 'transaction/createexptransaction.html', {'form': ExpenditureTransactionForm()})
    else:
        try:
            form = ExpenditureTransactionForm(request.POST)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/createexptransaction.html', {'form': ExpenditureTransactionForm(),
                                                                             'error': 'Неверные данные!'})


@login_required
def viewprotransaction(request, protransaction_pk):
    protransaction = get_object_or_404(ProfitableTransaction, pk=protransaction_pk)
    form = ProfitableTransactionForm(instance=protransaction)
    if request.method == 'GET':
        return render(request, 'transaction/viewprotransaction.html', {'protransaction': protransaction,
                                                                       'form': form})
    else:
        try:
            form = ProfitableTransactionForm(request.POST, instance=protransaction)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/viewprotransaction.html', {'protransaction': protransaction,
                                                                           'form': form})


@login_required
def viewexptransaction(request, exptransaction_pk):
    exptransaction = get_object_or_404(ExpenditureTransaction, pk=exptransaction_pk)
    form = ExpenditureTransactionForm(instance=exptransaction)
    if request.method == 'GET':
        return render(request, 'transaction/viewexptransaction.html', {'exptransaction': exptransaction,
                                                                       'form': form})
    else:
        try:
            form = ExpenditureTransactionForm(request.POST, instance=exptransaction)
            form.save()
            return redirect('recorded')
        except ValueError:
            return render(request, 'transaction/viewexptransaction.html', {'exptransaction': exptransaction,
                                                                           'form': form})


@login_required
def deleteprotransaction(request, protransaction_pk):
    protransaction = get_object_or_404(ProfitableTransaction, pk=protransaction_pk)
    if request.method == 'POST':
        protransaction.delete()
        return redirect('recorded')


@login_required
def deleteexptransaction(request, exptransaction_pk):
    exptransaction = get_object_or_404(ExpenditureTransaction, pk=exptransaction_pk)
    if request.method == 'POST':
        exptransaction.delete()
        return redirect('recorded')
