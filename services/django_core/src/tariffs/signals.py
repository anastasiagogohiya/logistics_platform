from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Tariff
from .services.es_service import ElasticsearchService


@receiver(post_save, sender=Tariff)
def update_es_on_save(sender, instance, **kwargs):
    es_service = ElasticsearchService()
    es_service.index_tariff(instance)

@receiver(post_delete, sender=Tariff)
def update_es_on_delete(sender, instance, **kwargs):
    es_service = ElasticsearchService()
    es_service.delete_tariff(instance.id)