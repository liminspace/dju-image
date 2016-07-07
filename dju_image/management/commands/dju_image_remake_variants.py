from django.core.management import CommandError
from dju_common.management import LoggingBaseCommand
from . import profiles_validate
from ...maintenance import remake_images_variants


class Command(LoggingBaseCommand):
    help = 'Remake variants for uploaded images.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-p', '--profiles', nargs='+',
                            help='Upload profiles. (Default: empty -- all profiles)')
        parser.add_argument('-c', '--clear', action='store_true', default=False,
                            help='Clear all variants before remaking.')

    def handle(self, *args, **options):
        profiles = options['profiles'] or None
        t = profiles_validate(profiles)
        if t:
            raise CommandError(t)
        clear = options['clear']
        self.log('Start remake variants for images (profiles: {}; clear: {})...'.format(
            ', '.join(profiles) if profiles else '-ALL-',
            ('no', 'yes')[int(clear)]
        ))
        removed, remade = remake_images_variants(profiles=profiles, clear=clear)
        self.log('Done. Removed / remade thumbs: {} / {}'.format(removed, remade), double_br=True)
