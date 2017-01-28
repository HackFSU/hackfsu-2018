from django.db import models
from api.models import Hackathon


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
        return 'hackathon={} name="{}" tier={} order={} website_link="{}" logo_link="{}"'.format(
            self.hackathon.id,
            self.name,
            self.tier,
            self.order,
            self.website_link,
            self.logo_link
        )
