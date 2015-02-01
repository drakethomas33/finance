import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from moneyed import Money
from project.finance.models import Account, Month, Category


def index(request):
    return render_to_response(
        'index.html', {}, RequestContext(request))


def account_totals(request):
    if request.GET.get('accounts'):
        print request.GET['accounts'].split(',')
        accounts = Account.objects.filter(name__in=request.GET['accounts'].split(','))
    else:
        accounts = Account.objects.all()

    data = []
    for account in accounts:
        data.append(account.totals())

    #import pprint
    #pprint.pprint(data)

    return HttpResponse(json.dumps(data), content_type='application/json')


def categories_by_month(request):
    data = {}

    for category in Category.objects.filter(parent__isnull=True).exclude(
            name="Transfers"
    ).exclude(name="Investments"):
        data[category.name] = category.expenses()
        for child in category.category_set.all():
            print child.name
            data[category.name] += child.expenses()
    print data.values()
    total = Money(0, 'GBP')
    for value in data.values():
        total += value
    print total.amount
    other = Money(0, 'GBP')
    for category, spend in data.items():
        print spend.amount / total.amount
        if (spend.amount / total.amount) < 0.01:
            other += spend
            del(data[category])
    data['Other'] = other
    return HttpResponse(json.dumps(
        [[name, float(value.amount)] for name, value in data.items()]
    ), content_type='application/json')
