from dju_common.management import LoggingBaseCommand
from ...maintenance import remove_old_tmp_files


class Command(LoggingBaseCommand):
    help = 'Remove old temporary uploaded files.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-p', '--profiles', action='append', dest='profiles', default=[],
                            help='Upload profiles. Dont set for all.')
        parser.add_argument('-m', '--max-lifetime', action='store', type=int, dest='max_lifetime', default=168,
                            help='Time of life file in hours. Default: 168 (7 days)')

    def handle(self, *args, **options):
        profiles = options['profiles'] or None
        removed, total = remove_old_tmp_files(profiles=profiles, max_lifetime=options['max_lifetime'])
        self.log('Removed: {} / {}'.format(removed, total))
