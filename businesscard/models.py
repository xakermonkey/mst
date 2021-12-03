# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DetCoords(models.Model):
    devid = models.IntegerField(primary_key=True)
    detid = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lon = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lanes = models.IntegerField(blank=True, null=True)
    lanenumbers = models.TextField(blank=True, null=True)
    direction = models.TextField(blank=True, null=True)
    angle = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    active = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'det_coords'

    def __str__(self):
        return self.name


class Detectors(models.Model):
    completeness = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    speed = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    occ = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    utilisation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    volume = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    number = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, primary_key=True)

    class Meta:
        managed = False
        db_table = 'detectors'

    def __str__(self):
        return self.time


class Fvf(models.Model):
    recid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    grz = models.TextField(blank=True, null=True)
    camera = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    speed = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lat = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lon = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    lanes = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    id = models.DecimalField(max_digits=65535, decimal_places=65535, primary_key=True)

    class Meta:
        managed = False
        db_table = 'fvf'

    def __str__(self):
        return self.address


class Sensors(models.Model):
    mac = models.BigIntegerField(primary_key=True)
    real_flag = models.BooleanField(default=False)
    timestamp = models.DateTimeField(blank=True, null=True)
    lon = models.CharField(max_length=255, verbose_name='Долгота')
    lat = models.CharField(max_length=255, verbose_name='Широта')

    class Meta:
        managed = False
        db_table = 'sensors'

    def __str__(self):
        return str(self.mac)
