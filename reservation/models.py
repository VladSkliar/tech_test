from django.db import models
from django.utils.translation import gettext_lazy as _


class Reservation(models.Model):
    checkin = models.DateField(
        verbose_name=_('Checkin')
    )
    checkout = models.DateField(
        verbose_name=_('Checkout')
    )
    rental = models.ForeignKey(
        'rental.Rental',
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name=_('Rental')
    )

    def __str__(self):
        return f'({self.id}, {self.checkin}, {self.checkout})'
