from distutils.log import error
from django import dispatch
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_finished

from management.models import RationCard, Dependent
@receiver(request_finished)
@receiver(post_save, sender=Dependent, dispatch_uid= "update_no_of_dependents")
def add_dependents(sender, instance, created, **kwargs):
    
        try:
            if created:
                rc = RationCard.objects.get(card_no=instance.card.card_no)
                rc.no_of_dependants += 1
                rc.save()
        except UnboundLocalError:
            print("error")