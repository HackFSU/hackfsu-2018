from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class JudgingExpoManager(models.Manager):
    def current(self, hackathon: Hackathon):
        curr = self.filter(hackathon=hackathon, current=True)
        if curr.exists():
            return curr.all()[0]
        else:
            return None

    def set_current(self, expo):
        """ Sets expo as the current expo and sets current to false for other expos of same hackathon """
        for current_expo in self.filter(hackathon=expo.hackathon, current=True).all():
            current_expo.current = False
            current_expo.save()

        expo.current = True
        expo.save()


class JudgingExpo(models.Model):
    objects = JudgingExpoManager()
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    table_number_start = models.IntegerField()
    table_number_end = models.IntegerField()
    current = models.BooleanField()


@admin.register(JudgingExpo, site=hackfsu_admin)
class JudgingExpoAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'name', 'table_number_start', 'table_number_end', 'current')
    list_editable = ('table_number_start', 'table_number_end')
    list_display_links = ('id',)
    search_fields = ()
    ordering = ('-name',)
    actions = ('set_as_current', 'end_expo')

    def set_as_current(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, 'You may only set exactly one expo as current at a time.')
            return

        expo = queryset[0]
        JudgingExpo.objects.set_current(expo)

        self.message_user(request, 'Expo {} is now the current expo for hackathon {}'.format(
            expo.name, expo.hackathon.name
        ))
    set_as_current.short_description = 'Assign as current expo for current hackathon'

    def end_expo(self, request, queryset):
        total = 0
        for expo in queryset:
            if expo.current:
                expo.current = False
                expo.save()
                total += 1
        self.message_user(request, 'Ended {} expo(s)'.format(total))
    end_expo.short_description = 'End the expo (unset current)'

