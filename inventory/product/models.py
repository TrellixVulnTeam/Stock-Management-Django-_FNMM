from django.db import models
from datetime import datetime


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_code = models.CharField(max_length=100)
    unit_name = models.CharField(max_length=100)
    per_unit_price = models.FloatField()
    total_unit_price = models.FloatField()
    team_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    quantity_value = models.FloatField()
    quantity_used_value = models.FloatField(default=0)
    cone_quantity_value = models.IntegerField()
    cone_quantity_used_value = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name


class ProductEntryInfo(models.Model):
    productID = models.ForeignKey('Product', on_delete=models.CASCADE)
    chequeNo = models.CharField(max_length=100)
    supplier_name = models.CharField(max_length=100)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.team_name


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.team_name


class Units(models.Model):
    unit_name = models.CharField(max_length=50)
    unit_si_name = models.CharField(max_length=50)

    def __str__(self):
        return self.unit_name


class TeamMember(models.Model):
    team_member_name = models.CharField(max_length=100)
    team_member_position = models.CharField(max_length=100)
    team_member_username = models.CharField(max_length=100)
    team_member_password = models.CharField(max_length=50)
    team = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.team_member_name


class Notifications(models.Model):
    changerID = models.ForeignKey('TeamMember', on_delete=models.CASCADE)
    changedID = models.ForeignKey('Product', on_delete=models.CASCADE)
    used = models.IntegerField(default=0)
    changeValue = models.DecimalField(max_digits=10, decimal_places=2)
    valueProgress = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.changerID


class Suppliers(models.Model):
    supplier_name = models.CharField(max_length=100)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    team = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self):
        return self.supplier_name
