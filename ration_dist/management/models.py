from email.policy import default
from pyexpat import model
from turtle import color
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator



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
    
    
class RationCard(models.Model):
    PINK = 1
    WHITE = 2
    BLUE = 3
    YELLOW = 4
    COLOR_CHOICES = [(PINK, 'Pink'), (WHITE, 'White'), (BLUE, 'Blue'), (YELLOW, 'Yellow')]
    color_id = models.IntegerField(choices=COLOR_CHOICES, default=WHITE)
    card_no = models.CharField(max_length=10, primary_key=True, unique=True, null=False, default="0000000000")
    taluk_no = models.PositiveIntegerField( default=1,
        validators=[
            MaxValueValidator(78),
            MinValueValidator(1)
        ], null=False)
    no_of_adults = models.PositiveIntegerField(default=1, null=False)
    no_of_children = models.PositiveIntegerField(default=0, null=False) #auto no of members = adults + children
    ward_no = models.PositiveIntegerField( default=1,
        validators=[
            MaxValueValidator(2100),
            MinValueValidator(1)
        ], null=False)
    store_id = models.ForeignKey(RationStore,on_delete=models.CASCADE)
    monthly_income = models.DecimalField(null=False, default=0.00, decimal_places=2, max_digits= 10)

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

class Quota(models.Model):
    pass

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