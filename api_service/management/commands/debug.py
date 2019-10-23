from django.core.management import BaseCommand

from api_service.utils import get_user_pnac_groups, get_group_users


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # get_group_users('unit4')
        get_user_pnac_groups('p.druzhinin')
