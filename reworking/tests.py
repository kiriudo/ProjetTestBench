import datetime

from django.test import TestCase
from django.utils import timezone
from .models import ProductsHasReworksmanager,LogsManager,Batchs,ProductsHasReworks,Products,Logs,Tests,TestBenchs,Manufacturers,SerialNumbers,Reworks,Models
# Create your tests here.
class ProductsHasReworksModelTests(TestCase):
    def test_executed_recently_with_old(self):
        time = timezone.now() + datetime.timedelta(days = 1,seconds=1)
        future_product_has_rework = ProductsHasReworks(date = time)
        self.assertIs(future_product_has_rework.executed_recently(),False)

    def test_executed_recently_with_recent(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        future_product_has_rework = ProductsHasReworks(date=time)
        self.assertIs(future_product_has_rework.executed_recently(), True)

    def test_probability(self):
        test = Tests(pk=1)
        log1 = Logs(pk=1,test=test,date = timezone.now())
        log2 = Logs(pk=2,test=test,date = timezone.now())
        rework1 = Reworks(pk=1,designator="R2change")
        rework2 = Reworks(pk=2,designator="C2change")
        PHR1 = ProductsHasReworks(pk=1,log = log1,rework = rework1,date=timezone.now())
        PHR2 = ProductsHasReworks(pk=2,log = log2,rework= rework2,date=timezone.now())
        self.assertIs(ProductsHasReworks.objects.get(pk=1).log.id_log,1)
        self.assertIs(ProductsHasReworks.objects.probability(test,rework1),1/2)

class LogsTests(TestCase):
    def test_executed_recently_with_old(self):
        time = timezone.now() + datetime.timedelta(days = 1,seconds=1)
        future_Log = Logs(date = time)
        self.assertIs(future_Log.executed_recently(),False)

    def test_executed_recently_with_recent(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        future_Log = Logs(date=time)
        self.assertIs(future_Log.executed_recently(), True)

    def test_number_of_reworks(self):
        log = Logs(id_log=1)
        rework1 = Reworks()
        rework2 = Reworks()
        PHR1 = ProductsHasReworks(pk = 1,rework=rework1,log=log)
        PHR2 = ProductsHasReworks(pk = 2,rework=rework2,log=log)
        self.assertIs(Logs.objects.number_of_reworks(log),'2')

    def test_last_rework(self):
        log = Logs(id_log = 1)
        rework1 = Reworks(operation= 'R1')
        rework2 = Reworks(operation= 'R2')
        PHR1 = ProductsHasReworks(log = log,rework = rework1,date=timezone.now())
        PHR2 = ProductsHasReworks(log= log, rework= rework2,date=timezone.now() + datetime.timedelta(days=1))
        self.assertIs(Logs.objects.last_rework(1) ,rework1)