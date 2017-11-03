from django.db import models
from api.models import Hackathon, JudgingExpo, JudgingCriteria, JudgeInfo
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackManager(models.Manager):
    def get_next_table_number(self):
        number = 1
        hackathon = Hackathon.objects.current()
        while self.filter(hackathon=hackathon, table_number=number).exists():
            number += 1
        return number


class Hack(models.Model):
    objects = HackManager()
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    name = models.CharField(max_length=100)                                             # Devpost "Submission Title"
    description = models.TextField()                                                    # Devpost "Plain Description"
    extra_judging_criteria = models.ManyToManyField(to=JudgingCriteria, blank=True)     # Devpost "Desired Prizes"
    current_judges = models.ManyToManyField(to=JudgeInfo, blank=True, related_name='judges_current')
    judges = models.ManyToManyField(to=JudgeInfo, blank=True, related_name='judges')
    total_judge_score = models.IntegerField(default=0)
    times_judged = models.IntegerField(default=0)

    @staticmethod
    def get_active_hacks_for_judge(judge):
        return Hack.objects.filter(current_judges=judge)

    def get_expo(self):
        expo = JudgingExpo.objects.filter(
            hackathon=self.hackathon,
            table_number_start__lte=self.table_number,
            table_number_end__gte=self.table_number
        )
        if expo.exists():
            return expo.all()[0]
        return None

    def get_expo_name(self) -> str:
        expo = self.get_expo()
        if expo is None:
            return 'N/A'
        return expo.name

    def get_criteria_names(self) -> str:
        names = []
        for criteria in self.extra_judging_criteria.all():
            names.append(criteria.name)
        return ', '.join(names)

    def __str__(self):
        return self.name


@admin.register(Hack, site=hackfsu_admin)
class HackAdmin(admin.ModelAdmin):
    list_filter = ('hackathon',)
    list_display = ('id', 'name', 'expo', 'table_number', 'extra_criteria')
    list_editable = ('table_number',)
    list_display_links = ('id',)
    search_fields = ('name', 'table_number')
    ordering = ('table_number',)

    @staticmethod
    def expo(obj: Hack):
        return obj.get_expo_name()

    @staticmethod
    def extra_criteria(obj: Hack) -> str:
        return obj.get_criteria_names()
