from django.db import models
from api.models import Hackathon
from django.contrib import admin
from hackfsu_com.admin import hackfsu_admin


class HackathonSponsor(models.Model):

    SPONSOR_TIERS = (
        (0, 'Co-Host'),
        (1, 'Tier 3'),
        (2, 'Tier 2'),
        (3, 'Tier 1'),
        (4, 'Partner')
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    website_link = models.CharField(max_length=500)
    logo_link = models.CharField(max_length=500)
    tier = models.SmallIntegerField(default=0, choices=SPONSOR_TIERS)
    order = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


@admin.register(HackathonSponsor, site=hackfsu_admin)
class HackathonSponsorAdmin(admin.ModelAdmin):
    list_filter = ('hackathon', 'tier')
    list_display = ('id', 'hackathon', 'name', 'tier', 'order', 'logo_link', 'website_link')
    list_editable = ('hackathon', 'tier', 'order', 'logo_link')
    list_display_links = ('id',)
    actions = ('duplicate',)
    search_fields = ('name',)
    ordering = ('hackathon', 'tier', 'name')

    def duplicate(self, request, queryset):
        current_hackathon = Hackathon.objects.current()
        new_count = 0
        for sponsor in queryset:
            HackathonSponsor.objects.create(
                hackathon=current_hackathon,
                name=sponsor.name,
                website_link=sponsor.website_link,
                logo_link=sponsor.logo_link
            )
            new_count += 1
        self.message_user(request, str(new_count) + ' new sponsors created for ' + str(current_hackathon))

    duplicate.short_description = 'Duplicate selected sponsors for current hackathon'
