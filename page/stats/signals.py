from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from stats.models import Set

@receiver(m2m_changed, sender=Set.teamplayers.through)
def teamplayers_changed(sender, **kwargs):
    if kwargs['instance'].teamplayers.count() > 5:
        raise ValidationError("Set have to contain no more than 5 players")
