from django.db import models
from django.contrib.postgres.fields import ArrayField

from app.user.models import User

class Contract(models.Model):

    OPTION_SHEET = (
        (1, 'Economy'),
        (2, 'Standard'),
        (3, 'Premium'),
        (4, 'Customized')
    )
    
    option = models.IntegerField(blank=True, null=True, choices=OPTION_SHEET, default=1)

    date_of_issue = models.DateField(blank=True, null=True)

    date_of_expiry = models.DateField(blank=True, null=True)

    visit = ArrayField(models.IntegerField(default=0), size=5)

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='contract', blank=True, null=True)

 