import datetime

from django.db import models
# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib import admin

#classes manager
class SerialNumbersManager(models.Manager):
    def value(self,id):
        serial = SerialNumbers.objects.get(id_serial_number=id)
        return str(id) + "-" +\
               str(serial.batch) + "-" +\
               str(serial.year) + "-" +\
               str(serial.week) + "-" +\
               str(serial.identifiant)

class ProductsManager(models.Manager):
    def LastRework(self,product):
        return ProductsHasReworks.objects.filter(product_id= product).order_by('date').values_list('rework',flat=True)[0]

class LogsManager(models.Manager):
    def last_ProductsHasReworks(self,id_log):
        if ProductsHasReworks.objects.filter(log = id_log):# le log est bien présent dans productsHasReworks
            return ProductsHasReworks.objects.filter(log=id_log).order_by('date').values_list('id',flat = True)[0]

    def last_rework(self, id_log: int):
        return str(ProductsHasReworks.objects.get(id = self.last_ProductsHasReworks(id_log)).rework)

    def last_rework_date(self,id_log:int):
        return str(ProductsHasReworks.objects.get(id = self.last_ProductsHasReworks(id_log)).date)

    def executed_recently(self,date):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= date <= now

    def number_of_reworks(self,id):
        return str(len(ProductsHasReworks.objects.filter(log=id)))

class ProductsHasReworksmanager(models.Manager):
    def getlogs(self, id_product:int):
        return Logs.objects.filter(product_id=id_product)

    def getlogsrework(self,id_rework:int):
        return Logs.objects.filter(id_log = ProductsHasReworks.objects.filter(rework = id_rework))

    def test(self,id):
        return Tests.objects.get(logs=id.log)

    def probability(self,test,rework):#prbabilité qu'un rework soit lié à un test
        nt  = 0
        ntr = 0
        #nombre de réparations pour le test
        for PHR in ProductsHasReworks.objects.all():
            for log in Logs.objects.filter(test = test).values_list('id_log',flat = True):
                if PHR.log.id_log == log:
                    nt = nt+1

        #nombre de reworks en paramètre dans le test
        for PHR in ProductsHasReworks.objects.filter(rework = rework):
            for log in Logs.objects.filter(test = test).values_list('id_log',flat = True):
                if PHR.log.id_log == log:
                    ntr = ntr+1
        if nt>0:
            return ntr/nt
        else:
            return 0

    def probalist(self,test):#liste des probabilités
        result = dict
        for PHR in ProductsHasReworks.objects.all():
            for log in Logs.objects.filter(test = test).values_list('id_log',flat = True):
                if PHR.log.id_log == log:
                    result[PHR.rework.designator] = self.probability(test,PHR.rework.id_rework)

class TestsManager(models.Manager):
    def reworks_test(self,test):
        i=0
        n=0
        query = list(Logs.objects.filter(test_id = test).values_list('productshasreworks__rework__designator',flat = True))
        #supprimer les doublons
        query = list(set(query))
        return query

        # for l in Logs.objects.filter(test = test):
        #     n = n+1
            #ProductsHasReworks.objects.filter(log = l.id_log).value_list('rework',flat = True):

#models
class Batchs(models.Model):
    id_batch = models.AutoField(primary_key=True)
    batch_reference = models.CharField(unique=True, max_length=45)
    size = models.PositiveSmallIntegerField()
    model = models.ForeignKey('Models', models.DO_NOTHING, null=True)
    description = models.TextField(blank=True, null=True)
    number_electrical_ok = models.PositiveSmallIntegerField()
    number_electrical_nok = models.PositiveSmallIntegerField()
    number_functional_ok = models.PositiveSmallIntegerField()
    number_functional_nok = models.PositiveSmallIntegerField()
    batch_date_start = models.DateTimeField(blank=True, null=True)
    batch_date_end = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.id_batch)
    class Meta:
        db_table = 'batchs'
        unique_together = (('id_batch', 'model'),)


class Logs(models.Model):
    id_log = models.AutoField(primary_key=True)
    test = models.ForeignKey('Tests', models.DO_NOTHING, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, null=True)
    date = models.DateTimeField()
    test_bench = models.ForeignKey('TestBenchs', models.DO_NOTHING, null=True)
    result = models.CharField(max_length=3)
    value = models.FloatField(blank=True, null=True)
    min_value = models.FloatField(blank=True, null=True)
    max_value = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    details = models.CharField(max_length=50, blank=True, null=True)
    objects = LogsManager()

    def __str__(self):
        if self.__class__.objects.executed_recently(self.date):
            return " log n°" + str(self.id_log) + " - product "  + str(self.product) + " - test " + str(self.test) + " (" + self.result +")" + " - (recent)"
        else:
            return "product "  + str(self.product) + " - log n°" + str(self.id_log) + " - test " + str(self.test) + " (" + self.result +")" + " - (not recent)"
    class Meta:
        db_table = 'logs'
        unique_together = (('id_log', 'test_bench', 'product', 'test'),)

class Manufacturers(models.Model):
    id_manufacturer = models.SmallAutoField(primary_key=True)
    manufacturer_name = models.TextField()
    location = models.TextField()
    def __str__(self):
        return self.manufacturer_name
    class Meta:
        db_table = 'manufacturers'

class Models(models.Model):
    id_model = models.SmallAutoField(primary_key=True)
    model_number = models.CharField(max_length=40)
    firmware = models.TextField()
    bootloader = models.TextField()
    xbee_firmware = models.TextField()
    electrical_test = models.TextField()
    functional_test = models.TextField()
    valid_model = models.CharField(max_length=3)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.model_number
    class Meta:
        db_table = 'models'

class Products(models.Model):
    id_product = models.AutoField(primary_key=True,null = False,unique=True)
    serial_number = models.OneToOneField('SerialNumbers', models.DO_NOTHING, blank=True, null=True)
    batch = models.ForeignKey(Batchs, models.DO_NOTHING, blank=True, null=True)
    model = models.ForeignKey(Models, models.DO_NOTHING, blank=True, null=True)
    mac_address = models.CharField(max_length=23, blank=True, null=True)
    electrical_result = models.CharField(max_length=3, blank=True, null=True)
    electrical_date = models.DateTimeField(blank=True, null=True)
    electrical_count = models.PositiveSmallIntegerField()
    functional_result = models.CharField(max_length=3, blank=True, null=True)
    functional_date = models.DateTimeField(blank=True, null=True)
    functional_count = models.PositiveSmallIntegerField()
    objects = ProductsManager
    def getlogs(self):
        return self.logs_set.all
    def __str__(self):
        return str(self.serial_number)
    class Meta:
        db_table = 'products'


class ProductsHasReworks(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    date = models.DateTimeField()
    objects = ProductsHasReworksmanager()
    log = models.ForeignKey(Logs,models.DO_NOTHING,null=True,)
    rework = models.ForeignKey('Reworks', models.DO_NOTHING, null=True)
    def __str__(self):
        return str(self.product) + " " + str(self.rework) + " " + str(self.date)
    class Meta:
        db_table = 'products_has_reworks'
        managed = True

class Reworks(models.Model):
    id_rework = models.SmallAutoField(primary_key=True)
    designator = models.TextField()
    operation = models.TextField()
    def __str__(self):
        return self.designator
    class Meta:
        db_table = 'reworks'


class SerialNumbers(models.Model):
    id_serial_number = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batchs, models.DO_NOTHING, null=True)
    year = models.SmallIntegerField()
    week = models.SmallIntegerField()
    identifiant = models.PositiveSmallIntegerField()
    affected = models.CharField(max_length=3)
    objects = SerialNumbersManager()
    def __str__(self):
        return str(self.id_serial_number)
    class Meta:
        db_table = 'serial_numbers'
        unique_together = (('id_serial_number', 'batch'),)

class TestBenchs(models.Model):
    id_test_bench = models.SmallAutoField(primary_key=True)
    manufacturer = models.ForeignKey(Manufacturers, models.DO_NOTHING, blank=True, null=True)
    type = models.CharField(max_length=10)
    computer_serial_number = models.CharField(max_length=100)
    date_creation = models.DateTimeField(blank=True, null=True)
    date_last_calibration = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.id_test_bench)
    class Meta:
        db_table = 'test_benchs'


class Tests(models.Model):
    id_test = models.SmallAutoField(primary_key=True)
    test = models.TextField()
    objects = TestsManager()
    def __str__(self):
        return self.test
    class Meta:
        db_table = 'tests'
