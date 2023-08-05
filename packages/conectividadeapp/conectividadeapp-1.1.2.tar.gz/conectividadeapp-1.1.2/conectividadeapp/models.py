from datetime import date
from simple_history.models import HistoricalRecords

from django.db import models
from django.db.models.deletion import CASCADE, PROTECT

from dcim.models import Device, Site

class ActorCategory(models.Model):
    name = models.CharField(
        max_length=80,
        verbose_name='Name',
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Complete Name',
    )

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='E-mail',
    )

    category = models.ForeignKey(
        ActorCategory,
        on_delete=models.PROTECT,
        verbose_name='Category',
    )

    cellphone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Cellphone',
    )

    telephone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Telephone',
    )

    history = HistoricalRecords(
        table_name='conectividadeapp_actor_history',
        custom_model_name=lambda x:f'{x}History',
    )

    # This attribute does not allow to be changed by actor._active = True or actor._active = False
    # To change this attribute, use the actor.activate() method for True or actor.deactivate() for False
    # To get this attribute, use the actor.is_active()
    _active = models.BooleanField(
        default = True,
    )

    def is_active(self):
        '''Returns True if the instance is active and False if the instance is inactive'''
        return self._active

    def activate(self):
        '''Changes the status of active to True'''
        self._active = True
        self.save()

    def deactivate(self):
        '''Change the status of active to False'''
        self._active = False
        self.save()

    def __str__(self):
        return self.name

    # If called like 'Actor.first_name', return the first name of the Actor in 'Actor.name'
    @property
    def first_name(self):
        return self.name.split()[0]

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

class OldDevice(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    rack = models.CharField(max_length=100, null=True, blank=True)
    site = models.CharField(max_length=100, null=True, blank=True)
    ipv4 = models.CharField(max_length=40, null=True, blank=True)
    ipv6 = models.CharField(max_length=70, null=True, blank=True)

class ActivityReason(models.Model):
    CHOICES = [
        ('INSTALL', 'Instalação'),
        ('REMOVE', 'Remoção'),
    ]

    name = models.CharField(
        max_length=256,
    )

    type = models.CharField(
        max_length=7,
        choices=CHOICES,
        default='INSTALL',
    )

    # This attribute does not allow to be changed by reason._active = True or reason._active = False
    # To change this attribute, use the reason.activate() method for True or reason.deactivate() for False
    # To get this attribute, use the reason.is_active()
    _active = models.BooleanField(
        default = True,
    )

    def is_active(self):
        '''Returns True if the instance is active and False if the instance is inactive'''
        return self._active

    def activate(self):
        '''Changes the status of active to True'''
        self._active = True
        self.save()

    def deactivate(self):
        '''Change the status of active to False'''
        self._active = False
        self.save()

    def __str__(self):
        return f'{self.type} - {self.name}'

class Activity(models.Model):
    device = models.ForeignKey(
        Device,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    olddevice = models.OneToOneField(
        OldDevice,
        on_delete=CASCADE,
        null=True,
        blank=True,
    )

    actor = models.ManyToManyField(
        Actor,
    )

    when = models.DateField(
        default=date.today,
    )

    description = models.TextField(
        max_length=255,
        null=True,
        blank=True,
    )

    reason = models.ForeignKey(
        'ActivityReason',
        on_delete=models.PROTECT,
    )

    history = HistoricalRecords(
        table_name='conectividadeapp_activity_history',
        custom_model_name=lambda x:f'{x}History',
    )

    # This attribute does not allow to be changed by activity._active = True or activity._active = False
    # To change this attribute, use the activity.activate() method for True or activity.deactivate() for False
    # To get this attribute, use the activity.is_active()
    _active = models.BooleanField(
        default = True,
    )

    @property
    def type(self):
        return self.reason.type

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def is_active(self):
        '''Returns True if the instance is active and False if the instance is inactive'''
        return self._active

    def activate(self):
        '''Change the status of active to True'''
        self._active = True

    def deactivate(self):
        '''Change the status of active to False'''
        self._active = False

    def __str__(self):
        return f'{self.id}'

'''
DJANGO SIGNALS FOR ACTIVITY MANAGEMENT
'''

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Activity)
def set_technical_reservation_to_device_site(sender, instance, created, **kwargs):
    if created and instance.type == 'REMOVE':
        site, created = Site.objects.get_or_create(
            name='Technical Reservation',
            defaults={'slug': 'technical-reservation', 'status': 'active'}
        )
        device = instance.device
        device.site = site
        device.rack = None
        device.save()

post_save.connect(set_technical_reservation_to_device_site, sender=Activity)
