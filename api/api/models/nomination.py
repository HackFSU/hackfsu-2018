from django.contrib import admin
from django.db import models
from django.db.models.manager import BaseManager

from hackfsu_com.admin import hackfsu_admin


class NominationQuerySet(models.QuerySet):
    pass


class Nomination(models.Model):
    objects = BaseManager.from_queryset(NominationQuerySet)()
    hack = models.ForeignKey(to='api.Hack', on_delete=models.CASCADE)
    superlative = models.ForeignKey(to='api.JudgingCriteria', on_delete=models.CASCADE)


@admin.register(Nomination, site=hackfsu_admin)
class NominationAdmin(admin.ModelAdmin):
    list_display = ('id', 'hack_name', 'superlative_name')
    list_display_links = ('id',)
    search_fields = ('hack_name', 'superlative_name')

    @staticmethod
    def hack_name(obj: Nomination):
        return obj.hack.name

    @staticmethod
    def superlative_name(obj: Nomination):
        return obj.superlative.name