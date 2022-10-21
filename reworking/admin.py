from django.contrib import admin
from .models import ProductsHasReworksmanager,LogsManager, Logs,Reworks, Products, SerialNumbers, ProductsHasReworks, Models, Manufacturers, Batchs, Tests, TestBenchs
from django.utils import timezone
from django import forms
# Register your models here.

class ReworksAdmin(admin.ModelAdmin):
    fieldsets = [
        ('désignation',{'fields':['designator']}),
        ('operande',{'fields':['operation']}),
    ]
    list_display = ('designator','operation')

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('serial numbers')

class ProductHasReworksAdmin(admin.ModelAdmin):
    list_display = ('product','test','rework')
    list_filter = ['product']
    fields = ('product','date','log','rework')
    def test(self,obj):
        return ProductsHasReworks.objects.test(obj)
    def get_form(self, request,obj=None, change=False, **kwargs):
        form = super().get_form(request,obj,**kwargs)
        form.base_fields["product"].label = "le produit"
        return form

class ProductHasReworksAdminForm(forms.ModelForm):
    class meta:
        model = ProductsHasReworks
        fields = "__all__"
    def list_log(self):
        pass

class LogsAdmin(admin.ModelAdmin):
    list_display = ('id_log',
                    'product',
                    'test',
                    'result',
                    'date',
                    'number_of_reworks',
                    'last_rework',
                    'last_rework_date',
                    )
    list_filter = ['product']
    def number_of_reworks(self,obj):
        return Logs.objects.number_of_reworks(obj.id_log)
    def last_rework(self,obj):
        return Logs.objects.last_rework(obj.id_log)
    def last_rework_date(self,obj):
        return Logs.objects.last_rework_date(obj.id_log)

class LogsAdminForm(forms.ModelForm):
    class Meta:
        model = ProductsHasReworks
        fields = "__all__"


admin.site.register(Logs,LogsAdmin)
admin.site.register(Reworks, ReworksAdmin)
admin.site.register(Products)
admin.site.register(SerialNumbers)
admin.site.register(ProductsHasReworks,ProductHasReworksAdmin)
admin.site.register(Models)
admin.site.register(Manufacturers)
admin.site.register(Batchs)
admin.site.register(Tests)
admin.site.register(TestBenchs)

