# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models



class Copyright(models.Model):
    field_id = models.CharField(db_column='_id', max_length=50, blank=True, null=True)  # Field renamed because it started with '_'.
    company_info = models.CharField(max_length=20, blank=True, null=True)
    artist_info = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.CharField(max_length=10, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    song_info = models.CharField(max_length=30, blank=True, null=True)
    url = models.CharField(max_length=40, blank=True, null=True)
    company = models.CharField(max_length=30, blank=True, null=True)
    company_pic = models.CharField(max_length=50, blank=True, null=True)
    classify = models.CharField(max_length=40, blank=True, null=True)
    date = models.CharField(max_length=20, blank=True, null=True)
    album_info = models.CharField(max_length=30, blank=True, null=True)
    desc = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'copyright'


