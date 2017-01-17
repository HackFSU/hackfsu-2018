from django.db import models
from api.models import Hackathon


class AnonStat(models.Model):
    KEY_CHOICES = (
        ('GEN', 'Gender'),
        ('ETH', 'Ethnicity')
    )

    VALUE_CHOICES = (
        ('Gender', (
            ('MAL', 'Male'),
            ('FEM', 'Female'),
            ('OTH', 'Other')
        )),
        ('Ethnicity', (
            ('ASI', 'Asian'),
            ('BLK', 'Black'),
            ('HIS', 'Hispanic'),
            ('MLT', 'Multicultural'),
            ('WHT', 'White'),
            ('OTH', 'Other')
        ))
    )

    hackathon = models.ForeignKey(to=Hackathon, on_delete=models.CASCADE)
    key = models.CharField(max_length=3, choices=KEY_CHOICES)
    value = models.CharField(max_length=3, choices=VALUE_CHOICES)
