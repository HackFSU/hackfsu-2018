from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class JudgingCriteria(models.Model):
    CRITERIA_TYPE_OVERALL = 0,
    CRITERIA_TYPE_SUPERLATIVE = 1
    CRITERIA_TYPE_MANUAL = 2
    CRITERIA_TYPE = (
        (CRITERIA_TYPE_OVERALL, 'Overall'),             # Final grade is accumulation of each overall criteria
        (CRITERIA_TYPE_SUPERLATIVE, 'Superlative'),     # Final grade is independent of other superlatives,
        (CRITERIA_TYPE_MANUAL, 'Manual')                # Graded manually, outside of judging system
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    point_contribution = models.IntegerField()
    criteria_type = models.SmallIntegerField(choices=CRITERIA_TYPE)
    description_long = models.CharField(max_length=500)     # Displayed in instructions
    description_short = models.CharField(max_length=100)    # Displayed next to score entry
    devpost_name = models.CharField(max_length=200)  # The name that should correspond with devpost csv 'Desired Prizes'


@admin.register(JudgingCriteria, site=hackfsu_admin)
class JudgingCriteriaAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'criteria_type')
    list_display = ('id', 'criteria_type', 'point_contribution', 'name', 'description_long', 'description_short')
    list_editable = ('criteria_type', 'point_contribution', 'name', 'description_long', 'description_short')
    list_display_links = ('id',)
    search_fields = ('name',)
    ordering = ('-point_contribution',)
