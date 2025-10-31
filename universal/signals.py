from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import UniversalRegistration, AuditLog
from django.forms.models import model_to_dict
from .notifications import notify_new_registration
from datetime import datetime, date


def _make_json_safe(obj):
    """Recursively convert datetimes to ISO strings so JSONField can store the data."""
    if isinstance(obj, dict):
        return {k: _make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_json_safe(v) for v in obj]
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj


@receiver(pre_save, sender=UniversalRegistration)
def universal_presave(sender, instance, **kwargs):
    # attach previous state for update detection
    if instance.pk:
        try:
            prev = sender.objects.get(pk=instance.pk)
            instance._previous_state = model_to_dict(prev)
        except sender.DoesNotExist:
            instance._previous_state = None
    else:
        instance._previous_state = None


@receiver(post_save, sender=UniversalRegistration)
def universal_postsave(sender, instance, created, **kwargs):
    prev = getattr(instance, "_previous_state", None)
    new = model_to_dict(instance)
    prev = _make_json_safe(prev) if prev is not None else None
    new = _make_json_safe(new)
    if created:
        AuditLog.objects.create(
            action=AuditLog.ACTION_CREATE,
            model_name=sender.__name__,
            object_id=str(instance.pk),
            previous_data=None,
            new_data=new,
        )
    else:
        AuditLog.objects.create(
            action=AuditLog.ACTION_UPDATE,
            model_name=sender.__name__,
            object_id=str(instance.pk),
            previous_data=prev,
            new_data=new,
        )
    # send optional notification on new registration
    if created:
        try:
            notify_new_registration(instance)
        except Exception:
            # notification failures shouldn't break saving
            pass


@receiver(pre_delete, sender=UniversalRegistration)
def universal_predelete(sender, instance, **kwargs):
    prev = model_to_dict(instance)
    AuditLog.objects.create(
        action=AuditLog.ACTION_DELETE,
        model_name=sender.__name__,
        object_id=str(instance.pk),
        previous_data=prev,
        new_data=None,
    )
