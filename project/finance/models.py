import calendar
import csv
import datetime
import json

from djmoney.models.fields import MoneyField
from model_utils.models import TimeFramedModel

from django.db import models
from moneyed import Money


def thingy(account_name):
    account = Account.objects.get(name=account_name)
    total = Money(account.initial.amount, 'GBP')
    total_transactions = Money(0, 'GBP')
    for month in Month.objects.all().order_by('start'):
        trans_in = trans_out = transactions = Money(0, 'GBP')
        for t in month.get_transactions(account_name=account_name):
            if t.category.name == 'Transfers':
                if t.amount.amount > 0:
                    trans_in += t.amount
                else:
                    trans_out += t.amount
            else:
                transactions += t.amount
        net_transferred = trans_in + trans_out
        total += net_transferred + transactions
        total_transactions += transactions
        print transactions.amount, '    ', total_transactions.amount


def net_worth():
    amount = Money(0, 'gbp')
    for t in Transaction.objects.all():
        print t.amount.amount, t.amount.currency
        amount += t.amount
    for a in Account.objects.all():
        print a.initial.amount, a.initial.currency
        if a.initial.amount:
            amount += a.initial
    return amount.amount


def get_month_start_and_end(date):
    """
    Args:
        date - datetime.date object
    Returns:
        start - datetime.datetime - start of month
        end - datetime.datetime - end of month
    """
    start = datetime.datetime.combine(
        datetime.date(date.year, date.month, 1),
        datetime.datetime.min.time()
    )
    end = datetime.datetime.combine(
        datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month)[1]),
        datetime.datetime.max.time()
    )
    return start, end


class Account(models.Model):
    name = models.CharField(max_length=64)
    initial = MoneyField(max_digits=10, decimal_places=2, default_currency='GBP')

    def current_balance(self):
        balance = Money(self.initial.amount, "GBP")
        for t in self.transaction_set.all():
            balance += t.amount
        return balance.amount

    def __unicode__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        ordering = ['parent__name', 'name']

    def __unicode__(self):
        return self.name


class MonthManager(models.Manager):

    def lookup(self, date):

        try:
            month = self.get(start__lte=date, end__gte=date)
        except Month.DoesNotExist:
            start, end = get_month_start_and_end(date)
            month = self.create(start=start, end=end)
        return month


class Month(TimeFramedModel):
    objects = MonthManager()
    closed = models.BooleanField(default=False)  # Accepting new transaction in this month?

    class Meta:
        ordering = ['-start']

    def get_transactions(self, account_name=None):
        transactions = Transaction.objects.filter(date__gte=self.start, date__lte=self.end)
        if account_name:
            transactions = transactions.filter(account=Account.objects.get(name=account_name))
        return transactions


class TransactionManager(models.Manager):

    def create_from_csv(self):
        # Delete transactions in open months
        for pending_month in Month.objects.filter(closed=False):
            pending_month.get_transactions().delete()
        f = open('/Users/tom/Desktop/finance.csv', 'r')
        reader = csv.reader(f)
        for row in reader:
            date = datetime.datetime.strptime(row[7], '%d/%m/%Y').date()
            month = Month.objects.lookup(date=date)
            if month.closed:
                print 'month closed, not going further'
                continue
            description = row[4]
            category_name = row[6].split('>')[-1].strip()
            if any([description.startswith('Transfer to'),
                    description.startswith('ATM Withdrawal'),
                    description.startswith('Transfer from')]) and category_name == 'Other':
                category = Category.objects.get(name='Transfers')
            else:
                category, _ = Category.objects.get_or_create(name=category_name)
            account, _ = Account.objects.get_or_create(name=row[2])
            Transaction.objects.create(
                amount=Money(float(row[9].replace(',', '')), currency='GBP'),
                date=date,
                description=description,
                category=category,
                account=account
            )


class Transaction(models.Model):
    amount = MoneyField(max_digits=10, decimal_places=2, default_currency='GBP')
    date = models.DateField()
    description = models.CharField(max_length=512)
    category = models.ForeignKey(Category)
    account = models.ForeignKey(Account)
    objects = TransactionManager()