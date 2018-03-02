from django.contrib import admin
from django.db import models
from django.db.models.manager import BaseManager

from hackfsu_com.admin import hackfsu_admin
from api.models import JudgingCriteria

class NominationQuerySet(models.QuerySet):
    pass


class Nomination(models.Model):
    objects = BaseManager.from_queryset(NominationQuerySet)()
    hack = models.ForeignKey(to='api.Hack', on_delete=models.CASCADE)
    superlative = models.ForeignKey(to='api.JudgingCriteria', on_delete=models.CASCADE)


class SuperlativeNameFilter(admin.SimpleListFilter):
    title = 'Superlative'
    parameter_name = 'superlative'

    def lookups(self, request, model_admin):
        superlative_categories = JudgingCriteria.objects.all()
        superlative_names = list(superlative_categories.values_list('name', flat=True))
        return zip(superlative_names, superlative_names)

    def queryset(self, request, queryset):
        superlative_categories = JudgingCriteria.objects.all()
        superlative_names = list(superlative_categories.values_list('name', flat=True))
        if self.value() in superlative_names:
            return queryset.filter(superlative__name = self.value())
        return queryset

@admin.register(Nomination, site=hackfsu_admin)
class NominationAdmin(admin.ModelAdmin):
    list_filter = (SuperlativeNameFilter, )
    list_display = ('id', 'hack_name', 'superlative_name')
    list_display_links = ('id',)
    search_fields = ('hack_name', 'superlative_name')

    def hack_name(self, obj: Nomination):
        return obj.hack.name

    hack_name.admin_order_field = "hack__name"

    @staticmethod
    def superlative_name(obj: Nomination):
        return obj.superlative.name

