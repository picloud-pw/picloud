from cloud.models import MemeSource
from memes.models import MemesSource


def migrate_memes():
    for source in MemeSource.objects.all():
        MemesSource.objects.get_or_create(
            source=source.link,
            author=source.author,
        )
