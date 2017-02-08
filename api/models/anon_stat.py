from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class AnonStat(models.Model):
    KEY_CHOICES = (
        ('GEN', 'Gender'),
        ('ETH', 'Ethnicity')
    )

    VALUE_CHOICES = (
        ('Gender', (
            ('MAL', 'Male'),
            ('FEM', 'Female'),
            ('OTH', 'Other')
        )),
        ('Ethnicity', (
            ('ASI', 'Asian'),
            ('BLK', 'Black'),
            ('HIS', 'Hispanic'),
            ('MLT', 'Multicultural'),
            ('WHT', 'White'),
            ('OTH', 'Other')
        ))
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    key = models.CharField(max_length=3, choices=KEY_CHOICES)
    value = models.CharField(max_length=3, choices=VALUE_CHOICES)


@admin.register(AnonStat, site=hackfsu_admin)
class AnonStatAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'key')
    list_display = ('id', 'key', 'value')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('key', 'value')
    ordering = ('hackathon', 'key')
