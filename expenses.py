#!/usr/bin/env python
#
# Input Example:
#
# $35.00, expense category, 03/03/2011, Comment about expense
# +$5.00, income category, 03/05/2011, Comment about income
#
# lines not maching the above are ignored
#

import os
import sys
import copy
import urllib
import operator
import webbrowser
from itertools import groupby
from datetime import datetime


class Date(datetime):
    def month_str(self):
        return ["January","February","March","April","May",
                "June","July","August","September",
                "October","November","December"][self.month-1]

    def sameday(self):
        "Return a new date only with month and year ignoring the rest"
        return Date(year=self.year, month=self.month, day=1)

    def __str__(self):
        return "%s %s" % (self.month_str(), self.year)


undefined, income, expense = range(3) # transaction type
class Transaction:
    amount = 0.0
    category = ""
    typ = undefined
    date = Date.now()
    comment = ""

    def __radd__(self, other):
        return self.amount + other


class Writer:
    def __init__(self, out, transactions):
        self.out = out
        self.transactions = transactions

    def write(self, x):
        self.out.write("%s\n" % x)

    def write_aligned(self, x, y):
        r = "%.2f" % y
        self.out.write("%s : %s\n" % (str(x).rjust(20),
                                      r.rjust(10)))

    def write_sum(self, name, transactions):
        self.write_aligned(name, sum(transactions))

    def write_categories(self, transactions):
        def sorted(group):
            def sort(x,y):
                if x[1] >= y[1]: return 1
                else: return -1
            sums = [(category, sum(lst)) for category,lst in group.items()]
            sums.sort(cmp=sort)
            return sums

        for category,total in sorted(group_by_category(get_expenses(transactions))):
            self.write_aligned(category, total)
            
        for category,total in sorted(group_by_category(get_incomes(transactions))):
            self.write_aligned(category, total)
    
    def write_months(self, transactions, month_sep=""):
        _txs = group_by_month(transactions)
        dates = _txs.keys()
        dates.sort()
        for date in dates:
            self.write("* %s" % date)
            self.write_categories(_txs[date])
            self.write_summary(_txs[date])
            self.write(month_sep)

    def write_summary(self, transactions):
        self.write("-"*33)
        self.write_aligned("Expenses", sum_expenses(transactions))
        self.write_aligned("Incomes", sum_incomes(transactions))
        self.write_aligned("Total", sum(transactions))
        
    def write_overall(self):
        self.write("\n*** Overall ***")
        self.write_categories(self.transactions)
        self.write_summary(self.transactions)

    def write_report(self):
        self.write_overall()
        self.write("\n\n\n")
        self.write_months(self.transactions)


def parse_transactions(text):
    """Parse the text and return a list of transaction objects"""
    line_num = 0
    all_transactions = []
    for line in text:
        line_num += 1
        if not line.count(',') == 3: continue
        amount,category,date,comment = line.strip().split(',')
        try:
            tx = Transaction()
            if amount.startswith('+$'):
                tx.typ = income
                tx.amount = float(amount[2:])
            elif amount.startswith('$'):
                tx.typ = expense
                tx.amount = -float(amount[1:])
            else:
                continue
            tx.category = category.strip()
            month, day, year = [int(j) for j in date.split('/')]
            tx.date = Date(day=day, month=month, year=year)
            tx.comment = comment
        except Exception, error:
            sys.stderr.write("Error on line: %s\n" % line_num)
            sys.stderr.write("%s\n" % line)
            sys.stderr.write("----\n%s\n" % error)
        all_transactions.append(tx)
    return all_transactions


##### Transaction Helpers #####
def get_expenses(transactions):
    return [tx for tx in transactions if tx.typ == expense]

def get_incomes(transactions):
    return [tx for tx in transactions if tx.typ == income]

def group(transactions, keyfunc):
    grp = {}
    transactions = sorted(transactions, key=keyfunc)
    for k,g in groupby(transactions, keyfunc):
        grp[k] = list(g)
    return grp

def group_by_category(transactions):
    return group(transactions, lambda tx: tx.category)

def group_by_month(transactions):
    return group(transactions, lambda tx: tx.date.sameday())

def sum_incomes(transactions):
    return sum(get_incomes(transactions))

def sum_expenses(transactions):
    return sum(get_expenses(transactions))


##### Google Charts helpers #####
def get_chart_for_expense_categories(transactions):
    base_chart = "https://chart.googleapis.com/chart?cht=p&chs=600x350&chtt=Expenses+by+category"

    def iter_color(color):
        def get_hex(i):
            x = hex(i)[2:]
            if len(x) == 1:
                return "0%s" % x
            return x
        r = int("0x%s" % color[:2], 16)
        g = int("0x%s" % color[2:4], 16)
        b = int("0x%s" % color[4:6], 16)
        r = (r + 30) % 255
        g = (g + 20) % 255
        b = (b + 55) % 255
        return "%s%s%s" % (get_hex(r), get_hex(g), get_hex(b))

    def sort_by_percentage(x,y):
        if x[1] >= y[1]: return 1
        else: return -1

    data = []
    color = "f0459a"

    expenses = get_expenses(transactions)
    all_expenses = sum(expenses)
    categories = group_by_category(expenses)
    for c,lst in categories.items():
        percentage = (sum_expenses(lst) / all_expenses) * 100
        data.append((c.replace(' ', '+'), percentage))

    data.sort(cmp=sort_by_percentage)

    chd=[]; chl=[]; chco=[]
    for d in data:
        chd.append(str(d[1])); chl.append(d[0]); chco.append(color)
        color = iter_color(color)

    chart = "%s&chd=t:%s&chl=%s&chco=%s" %(base_chart, ",".join(chd),
                                         "|".join(chl), "|".join(chco))
    return chart


def get_chart_by_month(transactions):
    base_chart = "https://chart.googleapis.com/chart?chxt=x,y&chs=600x350&cht=bvg&chtt=Monthly+Report&chbh=40&chco=22FF22,FF2222&"

    data = []
    maximum = 0
    all_expenses = sum_expenses(transactions)
    all_incomes = sum_incomes(transactions)
    _txs = group_by_month(transactions)
    dates = _txs.keys()
    dates.sort()
    for date in dates:
        lst = _txs[date]
        maximum = max(-sum_expenses(lst) + sum_incomes(lst), maximum)
        per_expenses = (sum_expenses(lst) / all_expenses) * 100
        per_incomes = (sum_incomes(lst) / all_incomes) * 100
        data.append((date, per_expenses, per_incomes))

    chxl=[]; chd_income=[]; chd_expense=[]
    for d in data:
        chxl.append(str(d[0]).replace(' ', '+'))
        chd_expense.append(str(abs(d[1])))
        chd_income.append(str(d[2]))

    chart = "%s&chxl=0:|%s&chd=t:%s|%s&chxr=1,0,%d" % (base_chart,
                                                       "|".join(chxl),
                                                       ",".join(chd_income),
                                                       ",".join(chd_expense),
                                                       maximum)
    return chart


if __name__ == "__main__":
    try:
        text = open(sys.argv[1])
    except:
        text = sys.stdin.read()

    transactions = parse_transactions(text)

    url = get_chart_for_expense_categories(transactions)
    open("all_expenses_category.png", "w").write(urllib.urlopen(url).read())

    url = get_chart_by_month(transactions)
    open("all_months.png", "w").write(urllib.urlopen(url).read())

    report = open("expense_report.html", "w")
    writer = Writer(report, transactions)
    report.write("""
<html>
<head>
<title>Expense Report</title>
</head>
<body>
<img src='all_expenses_category.png'/>
<img src='all_months.png'/>
<pre>
""")
    writer.write_report()
    report.write("</pre></body></html>")
    report.close()

    path = os.path.abspath("expense_report.html")
    webbrowser.open("file://%s" % path)
