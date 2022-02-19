from email.policy import default
from pyexpat import model
from turtle import color
from django.db import IntegrityError, models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.views import View
from django.contrib import admin
import random
import string
from django.utils.crypto import get_random_string

# Create your models here.

class RationStore(models.Model):
    store_id = models.CharField(max_length=10, primary_key=True, unique=True, null=False, default="0000000000")
    owner_name = models.CharField(max_length=20, null=False, default="----------")
    taluk_no = models.PositiveIntegerField( default=1,
        validators=[
            MaxValueValidator(78),
            MinValueValidator(1)
        ], null=False)
    ward_no = models.PositiveIntegerField( default=1,
        validators=[
            MaxValueValidator(2100),
            MinValueValidator(1)
        ], null=False)
    no_of_dependents = models.PositiveIntegerField(default=0, null=False) #auto
    no_of_yellow_cards = models.PositiveIntegerField(default=0, null=False) #auto
    no_of_pink_cards = models.PositiveIntegerField(default=0, null=False) #auto
    no_of_blue_cards = models.PositiveIntegerField(default=0, null=False) #auto
    no_of_white_cards = models.PositiveIntegerField(default=0, null=False) #auto
    sa= models.ManyToManyField('Granary', through='StockAcquisition')

class Quota(models.Model):
    color = models.CharField(max_length=10, primary_key=True, unique=True, null=False, default="----------")
    category = models.CharField(max_length=10, null=False, default="----------") 
    # monthly_income_cap = models.DecimalField(null=False, decimal_places=2, max_digits= 10, default=0.00)
    criteria = models.CharField(max_length=200, default="---------")
    Quota_sugar_in_kg_per_member = models.PositiveBigIntegerField(default=0, null=False)
    Quota_rice_in_kg_per_member = models.PositiveBigIntegerField(default=0, null=False)
    Quota_wheat_in_kg_per_member = models.PositiveBigIntegerField(default=0, null=False)
    Quota_kerosine_in_l_per_member = models.PositiveBigIntegerField(default=0, null=False)
    Price_sugar_per_kg = models.PositiveBigIntegerField(default=0, null=False)
    Price_rice_per_kg = models.PositiveBigIntegerField(default=0, null=False)
    Price_wheat_per_kg = models.PositiveBigIntegerField(default=0, null=False)
    Price_kerosine_per_l = models.PositiveBigIntegerField(default=0, null=False)
    
    
class RationCard(models.Model):
    card_no = models.CharField(max_length=10, primary_key=True, unique=True, null=False, default="0000000000", editable=False)
    taluk_no = models.PositiveIntegerField( default=1,
        validators=[
            MaxValueValidator(78),
            MinValueValidator(1)
        ], null=False, editable=False)
    no_of_adults = models.PositiveIntegerField(default=1, null=False)
    no_of_children = models.PositiveIntegerField(default=0, null=False) #auto no of members = adults + children
    ward_no = models.PositiveIntegerField( default=1,
        validators=[
            MaxValueValidator(2100),
            MinValueValidator(1)
        ], null=False, editable= False)
    store = models.ForeignKey(RationStore,on_delete=models.CASCADE)
    eligible_for_AAY= models.BooleanField(help_text="Landless laborers, marginal farmers, artisans, crafts men, widows, sick persons, illiterate, disabled adults with no means of subsistence.", default=False, null=False)
    color= models.ForeignKey(Quota,on_delete=models.CASCADE, editable=False, null=False)
    annual_income = models.DecimalField(null=False, default=0.00, decimal_places=2, max_digits= 10)
    no_of_dependants= models.IntegerField(default=0, editable=False)
    @property
    def _no_of_dependants(self,):
        return self.no_of_adults+ self.no_of_children
    
    @property
    def _taluk_no(self,):
        return self.store.taluk_no
    
    @property
    def _ward_no(self,):
        return self.store.ward_no

    # def create_new_ref_number(self):
    #     return get_random_string(10, allowed_chars='0123456789')

    def create_new_ref_number(self):
      rid = str(random.randint(1000000000, 9999999999))
      return str(rid)

    # def create_obj(self):
    #     self.card_no = ''.join(random.choices(string.digits, k=8))
    #     try:
    #         RationCard.objects.create(card_no=card_no)
    #     except:
    #         self.create_obj()

    def save(self,):
        self.card_no= self.create_new_ref_number()
        self.no_of_dependants= self._no_of_dependants
        self.taluk_no = self._taluk_no
        self.ward_no= self._ward_no
        if self.eligible_for_AAY :
            self.color=Quota.objects.get(color="Yellow") 
        elif self.annual_income<24200:
            self.color=Quota.objects.get(color="Pink")
        elif self.annual_income>100000 and self.annual_income<300000:
            self.color=Quota.objects.get(color="Blue")
        elif self.annual_income>300000:
            self.color=Quota.objects.get(color="White")
        try:
            super().save()
        except IntegrityError:
            self.save()    
    
    
class RationCardAdmin(admin.ModelAdmin):
    readonly_fields=('no_of_dependants','taluk_no','ward_no','color','card_no')
    
class Dependent(models.Model):
    card_no = models.ForeignKey(RationCard,on_delete=models.CASCADE)
    aadhar_card_no = models.CharField(max_length=12, unique=True, null=False, default="000000000000")
    name_of_dependent = models.CharField(max_length=20, null=False, default="----------")

class Provision(models.Model):
    card_no = models.ForeignKey(RationCard,on_delete=models.CASCADE)
    date_of_last_purchase = models.DateField(null=True, editable=True)
    rice_purchased_in_kg = models.DecimalField(null=True, decimal_places=2, max_digits= 4)
    sugar_purchased_in_kg = models.DecimalField(null=True, decimal_places=2, max_digits= 4)
    wheat_purchased_in_kg = models.DecimalField(null=True, decimal_places=2, max_digits= 4)
    kerosine_purchased_in_l = models.DecimalField(null=True, decimal_places=2, max_digits= 4)

class Granary(models.Model):
    granary_id = models.AutoField(primary_key=True,unique= True, null = False)
    location = models.CharField(max_length=50, null = False)
    sa= models.ManyToManyField('RationStore', through='StockAcquisition')
    Stock_sugar_in_kg = models.PositiveBigIntegerField(default=0, null=False)
    Stock_rice_in_kg = models.PositiveBigIntegerField(default=0, null=False)
    Stock_wheat_in_kg = models.PositiveBigIntegerField(default=0, null=False)
    Stock_kerosine_in_l = models.PositiveBigIntegerField(default=0, null=False)

class StockAcquisition(models.Model):
    store_id = models.ForeignKey(RationStore,on_delete=models.CASCADE)
    g_id = models.ForeignKey(Granary,on_delete=models.CASCADE)
    Stock_sugar_in_kg = models.PositiveBigIntegerField(default=0, null=False)
    Stock_rice_in_kg = models.PositiveBigIntegerField(default=0, null=False)
    Stock_wheat_in_kg = models.PositiveBigIntegerField(default=0, null=False)
    Stock_kerosine_in_l = models.PositiveBigIntegerField(default=0, null=False)
    # def save