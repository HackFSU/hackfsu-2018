from django.contrib import admin
from . import models

admin.site.register(models.AnonStat)
admin.site.register(models.Hackathon)
admin.site.register(models.HelpRequest)
admin.site.register(models.JudgeInfo)
admin.site.register(models.MentorInfo)
admin.site.register(models.UserInfo)
admin.site.register(models.Subscriber)
admin.site.register(models.WifiCred)
admin.site.register(models.HackathonCountdown)
admin.site.register(models.HackathonMap)
admin.site.register(models.HackathonUpdate)
admin.site.register(models.ScheduleItem)
