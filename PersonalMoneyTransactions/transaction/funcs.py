from django.shortcuts import render
from .models import ProfitableTransaction, ExpenditureTransaction
from django.db.models import Sum, F


def func2(request, maxdeltadays, sumpro, sumexp):
    pk = 3

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset = ExpenditureTransaction.objects.values('name').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                      averpr=Sum(F('quantity') * F('price')) / Sum('quantity'),
                                                                      totalquant=Sum('quantity'), meter=F('meter__name'),
                                                                      categories=F('category__name')
                                                                         ).order_by()

    for item in queryset:
        item['consumptionrate'] = item['totalquant'] / maxdeltadays
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speedmonthexp'] = float(item['speedexp']) * 30.4375

    overall_speedexp = round(sumexp / maxdeltadays, 2)
    overall_speedmonthexp = round(float(overall_speedexp) * 30.4375, 2)

    context = {'queryset': queryset, 'sumexp': sumexp, 'overall_speedmonthexp': overall_speedmonthexp,
               'overall_speedexp': overall_speedexp, 'multidash2': multidash2, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)


def func3(request, maxdeltadays, sumpro, sumexp):
    pk = 4

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset = ExpenditureTransaction.objects.values('category').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                          categories=F('category__name')).order_by()
    for item in queryset:
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speedmonthexp'] = float(item['speedexp']) * 30.4375

    overall_speedexp = round(sumexp / maxdeltadays, 2)
    overall_speedmonthexp = round(float(overall_speedexp) * 30.4375, 2)

    context = {'queryset': queryset, 'sumexp': sumexp, 'overall_speedmonthexp': overall_speedmonthexp,
               'overall_speedexp': overall_speedexp, 'multidash2': multidash2, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)


def func4(request, maxdeltadays, sumpro, sumexp):
    pk = 5

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset = ProfitableTransaction.objects.values('name').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speedmonthpro'] = float(item['speedpro']) * 30.4375

    overall_speedpro = round(sumpro / maxdeltadays, 2)
    overall_speedmonthpro = round(float(overall_speedpro) * 30.4375, 2)

    context = {'queryset': queryset, 'sumpro': sumpro, 'overall_speedmonthpro': overall_speedmonthpro,
               'overall_speedpro': overall_speedpro, 'multidash2': multidash2, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)



def func5(request, maxdeltadays, sumpro, sumexp):
    pk = 6

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset = ProfitableTransaction.objects.values('incometype').annotate(totalpro=Sum(F('amount')),
                                                                           incometypes=F('incometype__name')).order_by()
    for item in queryset:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speedmonthpro'] = float(item['speedpro']) * 30.4375

    overall_speedpro = round(sumpro / maxdeltadays, 2)
    overall_speedmonthpro = round(float(overall_speedpro) * 30.4375, 2)

    context = {'queryset': queryset, 'sumpro': sumpro, 'overall_speedmonthpro': overall_speedmonthpro,
               'overall_speedpro': overall_speedpro, 'multidash2': multidash2, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)


def func6(request, maxdeltadays, sumpro, sumexp):
    pk = 7

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset1 = ProfitableTransaction.objects.values('name').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset1:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speedmonthpro'] = float(item['speedpro']) * 30.4375

    queryset2 = ExpenditureTransaction.objects.values('name').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                      averpr=Sum(F('quantity') * F('price')) / Sum('quantity'),
                                                                      totalquant=Sum('quantity'), meter=F('meter__name'),
                                                                      categories=F('category__name')
                                                                         ).order_by()

    for item in queryset2:
        item['consumptionrate'] = item['totalquant'] / maxdeltadays
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speedmonthexp'] = float(item['speedexp']) * 30.4375

    overall_speedpro = round(sumpro / maxdeltadays, 2)
    overall_speedexp = round(sumexp / maxdeltadays, 2)

    overall_speedmonthpro = round(float(overall_speedpro) * 30.4375, 2)
    overall_speedmonthexp = round(float(overall_speedexp) * 30.4375, 2)

    context = {'queryset1': queryset1, 'queryset2': queryset2, 'overall_speedpro': overall_speedpro,
               'overall_speedexp': overall_speedexp, 'overall_speedmonthpro': overall_speedmonthpro,
               'overall_speedmonthexp': overall_speedmonthexp, 'sumpro': sumpro, 'sumexp': sumexp,
               'multidash2': multidash2, 'pk': pk}

    return render(request, 'transaction/specialcalculation.html', context)


def func7(request, maxdeltadays, sumpro, sumexp):
    pk = 8

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset1 = ProfitableTransaction.objects.values('incometype').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset1:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speedmonthpro'] = float(item['speedpro']) * 30.4375

    queryset2 = ExpenditureTransaction.objects.values('category').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                          categories=F('category__name')).order_by()
    for item in queryset2:
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speedmonthexp'] = float(item['speedexp']) * 30.4375

    overall_speedpro = round(sumpro / maxdeltadays, 2)
    overall_speedexp = round(sumexp / maxdeltadays, 2)

    overall_speedmonthpro = round(float(overall_speedpro) * 30.4375, 2)
    overall_speedmonthexp = round(float(overall_speedexp) * 30.4375, 2)

    context = {'queryset1': queryset1, 'queryset2': queryset2, 'overall_speedpro': overall_speedpro,
               'overall_speedexp': overall_speedexp, 'overall_speedmonthpro': overall_speedmonthpro,
               'overall_speedmonthexp': overall_speedmonthexp, 'sumpro': sumpro, 'sumexp': sumexp,
               'multidash2': multidash2, 'pk': pk}

    return render(request, 'transaction/specialcalculation.html', context)


def func8(request, maxdeltadays, sumpro, sumexp):
    pk = 9

    # Эта переменная для пунктира
    multidash2 = '- ' * 30

    queryset1 = ProfitableTransaction.objects.values('name').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset1:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speedmonthpro'] = float(item['speedpro']) * 30.4375

    queryset2 = ExpenditureTransaction.objects.values('name').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                      averpr=Sum(F('quantity') * F('price')) / Sum('quantity'),
                                                                      totalquant=Sum('quantity'), meter=F('meter__name'),
                                                                      categories=F('category__name')
                                                                         ).order_by()


    for item in queryset2:
        item['consumptionrate'] = item['totalquant'] / maxdeltadays
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speedmonthexp'] = float(item['speedexp']) * 30.4375

    queryset3 = ProfitableTransaction.objects.values('incometype').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset3:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speedmonthpro'] = float(item['speedpro']) * 30.4375

    queryset4 = ExpenditureTransaction.objects.values('category').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                          categories=F('category__name')).order_by()
    for item in queryset4:
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speedmonthexp'] = float(item['speedexp']) * 30.4375

    overall_speedpro = round(sumpro / maxdeltadays, 2)
    overall_speedexp = round(sumexp / maxdeltadays, 2)

    overall_speedmonthpro = round(float(overall_speedpro) * 30.4375, 2)
    overall_speedmonthexp = round(float(overall_speedexp) * 30.4375, 2)

    context = {'queryset1': queryset1, 'queryset2': queryset2, 'queryset3': queryset3, 'queryset4': queryset4,
               'overall_speedpro': overall_speedpro, 'overall_speedexp': overall_speedexp,
               'overall_speedmonthpro': overall_speedmonthpro, 'overall_speedmonthexp': overall_speedmonthexp,
               'sumpro': sumpro, 'sumexp': sumexp, 'multidash2': multidash2, 'pk': pk}

    return render(request, 'transaction/specialcalculation.html', context)



funcs = ['', '', func2, func3, func4, func5, func6, func7, func8]

