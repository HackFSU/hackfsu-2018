from django.db import models
from api.models import Hackathon, JudgingCriteria, Hack, JudgeInfo
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class JudgingGrade(models.Model):
    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    hack = models.ForeignKey(to=Hack, on_delete=models.CASCADE)
    criteria = models.ForeignKey(to=JudgingCriteria, on_delete=models.CASCADE)
    by_judge = models.ForeignKey(to=JudgeInfo, on_delete=models.CASCADE)
    grade = models.IntegerField()   # 0-100 grade. Will be weighted based on criteria's point contribution


@admin.register(JudgingGrade, site=hackfsu_admin)
class JudgingGradeAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'criteria')
    list_display = ('id', 'grade_type', 'criteria__name', 'grade', 'by_judge')
    list_display_links = ('id',)
    search_fields = ('hack__name', 'hack__table_number', 'judge__user__first_name', 'judge__user__last_name')
    ordering = ('grade_type', '-grade')
