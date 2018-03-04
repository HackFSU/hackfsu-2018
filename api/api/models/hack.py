from django.db import models
from api.models import Hackathon
from api.models.judging_criteria import JudgingCriteria
from api.models.judging_expo import JudgingExpo
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackQuerySet(models.QuerySet):
    from api.models.judge_info import JudgeInfo

    def from_expo(self, expo: JudgingExpo):
        return self.filter(
            table_number__gte=expo.table_number_start,
            table_number__lte=expo.table_number_end
        )

    def from_table_number(self, table: int):
        return self.get(table_number=table)

    def with_active_judge(self, judge: JudgeInfo):
        return self.filter(current_judges=judge)

    def without_previous_judge(self, judge: JudgeInfo):
        return self.exclude(judges=judge)


class HackManager(models.Manager):
    def get_next_table_number(self):
        number = 1
        hackathon = Hackathon.objects.current()
        while self.filter(hackathon=hackathon, table_number=number).exists():
            number += 1
        return number


class Hack(models.Model):
    objects = HackManager.from_queryset(HackQuerySet)()
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    name = models.CharField(max_length=100)                                             # Devpost "Submission Title"
    description = models.TextField()                                                    # Devpost "Plain Description"
    extra_judging_criteria = models.ManyToManyField(to=JudgingCriteria, blank=True)     # Devpost "Desired Prizes"
    current_judges = models.ManyToManyField(to='api.JudgeInfo', blank=True, related_name='judges_current')
    judges = models.ManyToManyField(to='api.JudgeInfo', blank=True, related_name='judges')
    total_judge_score = models.IntegerField(default=0)
    times_judged = models.IntegerField(default=0)

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
    list_display = ('id', 'name', 'expo', 'table_number', 'total_judge_score', 'average_score')
    list_editable = ('table_number',)
    list_display_links = ('id', 'name')
    search_fields = ('name', 'table_number')
    ordering = ('table_number', 'total_judge_score')

    @staticmethod
    def expo(obj: Hack):
        return obj.get_expo_name()

    @staticmethod
    def extra_criteria(obj: Hack) -> str:
        return obj.get_criteria_names()

    def average_score(self, obj: Hack):
        return obj.total_judge_score / len(obj.judges)
