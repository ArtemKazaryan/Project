from django.shortcuts import render
from .models import ProfitableTransaction, ExpenditureTransaction
from django.db.models import Sum, F
from django.utils.safestring import mark_safe


def func2(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 3
    queryset = ExpenditureTransaction.objects.values('name').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                      averpr=Sum(F('quantity') * F('price')) / Sum('quantity'),
                                                                      totalquant=Sum('quantity'), meter=F('meter__name'),
                                                                      categories=F('category__name')
                                                                         ).order_by()

    for item in queryset:
        item['consumptionrate'] = item['totalquant'] / maxdeltadays
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speed30exp'] = item['speedexp'] * 30

    context = {'queryset': queryset, 'multidash': multidash, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)


def func3(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 4
    queryset = ExpenditureTransaction.objects.values('category').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                          categories=F('category__name')).order_by()
    for item in queryset:
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speed30exp'] = item['speedexp'] * 30

    context = {'queryset': queryset, 'multidash': multidash, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)


def func4(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 5
    queryset = ProfitableTransaction.objects.values('name').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speed30pro'] = item['speedpro'] * 30

    context = {'queryset': queryset, 'multidash': multidash, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)



def func5(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 6
    queryset = ProfitableTransaction.objects.values('incometype').annotate(totalpro=Sum(F('amount')),
                                                                           incometypes=F('incometype__name')).order_by()
    for item in queryset:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speed30pro'] = item['speedpro'] * 30

    context = {'queryset': queryset, 'multidash': multidash, 'pk': pk}
    return render(request, 'transaction/specialcalculation.html', context)


def func6(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 7
    queryset1 = ProfitableTransaction.objects.values('name').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset1:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speed30pro'] = item['speedpro'] * 30

    queryset2 = ExpenditureTransaction.objects.values('name').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                      averpr=Sum(F('quantity') * F('price')) / Sum('quantity'),
                                                                      totalquant=Sum('quantity'), meter=F('meter__name'),
                                                                      categories=F('category__name')
                                                                         ).order_by()

    for item in queryset2:
        item['consumptionrate'] = item['totalquant'] / maxdeltadays
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speed30exp'] = item['speedexp'] * 30

    context = {'queryset1': queryset1, 'queryset2': queryset2, 'multidash': multidash, 'pk': pk}

    return render(request, 'transaction/specialcalculation.html', context)


def func7(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 8
    queryset1 = ProfitableTransaction.objects.values('incometype').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset1:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speed30pro'] = item['speedpro'] * 30

    queryset2 = ExpenditureTransaction.objects.values('category').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                          categories=F('category__name')).order_by()
    for item in queryset2:
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speed30exp'] = item['speedexp'] * 30

    context = {'queryset1': queryset1, 'queryset2': queryset2, 'multidash': multidash, 'pk': pk}

    return render(request, 'transaction/specialcalculation.html', context)


def func8(request, maxdeltadays, sumpro, sumexp, multidash):
    pk = 9
    queryset1 = ProfitableTransaction.objects.values('name').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset1:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speed30pro'] = item['speedpro'] * 30

    queryset2 = ExpenditureTransaction.objects.values('name').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                      averpr=Sum(F('quantity') * F('price')) / Sum('quantity'),
                                                                      totalquant=Sum('quantity'), meter=F('meter__name'),
                                                                      categories=F('category__name')
                                                                         ).order_by()

    for item in queryset2:
        item['consumptionrate'] = item['totalquant'] / maxdeltadays
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speed30exp'] = item['speedexp'] * 30

    queryset3 = ProfitableTransaction.objects.values('incometype').annotate(totalpro=Sum(F('amount')),
                                                                     incometypes=F('incometype__name')).order_by()
    for item in queryset3:
        item['speedpro'] = item['totalpro'] / maxdeltadays
        item['percentpro'] = round(100 * item['totalpro'] / sumpro, 3)
        item['speed30pro'] = item['speedpro'] * 30

    queryset4 = ExpenditureTransaction.objects.values('category').annotate(totalexp=Sum(F('quantity') * F('price')),
                                                                          categories=F('category__name')).order_by()
    for item in queryset4:
        item['speedexp'] = item['totalexp'] / maxdeltadays
        item['percentexp'] = round(100 * item['totalexp'] / sumexp, 3)
        item['speed30exp'] = item['speedexp'] * 30

    context = {'queryset1': queryset1, 'queryset2': queryset2, 'queryset3': queryset3, 'queryset4': queryset4,
               'multidash': multidash, 'pk': pk}

    return render(request, 'transaction/specialcalculation.html', context)



funcs = ['', '', func2, func3, func4, func5, func6, func7, func8]




