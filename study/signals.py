from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender=apps.get_model('study', "UserModel"))

def create_notification(serder, instance_model, is_created, **kwarg):

    if is_created:
        default_notification = apps.get_model('study', "NotificationsModel").objects.get(pk=1)
        instance_model.message = default_notification
        instance_model.save()