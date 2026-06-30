"""
Management command to seed the database with research publication entries.

Usage:
    python manage.py seed_publications
    python manage.py seed_publications --clear-only
    python manage.py seed_publications --project-title "Computational Musicology & Grammar Systems"
"""

from django.core.management.base import BaseCommand
from projects.models import Project, Publication


PUBLICATIONS_DATA = [
    {
        'badge': 'IT SPY 2025',
        'title': 'Výpočetná muzikológia: modely, metódy a aplikácie',
        'subtitle': 'Computational Musicology: Models, Methods and Applications',
        'authors': 'Jozef Makiš, supervised by prof. RNDr. Alexandr Meduna, CSc.',
        'venue': 'VUT FIT Brno · IT SPY 2025 competition (best student IT projects in CZ & SK)',
        'description': (
            "Master's thesis selected for the IT SPY competition. The work explores the "
            'intersection of formal grammar systems and music theory, defining models and '
            'methods for computational musicology: parsing symbolic music and generating '
            'orchestrations using multi-generative grammar systems.'
        ),
        'links': [
            {
                'label': 'IT SPY entry',
                'url': 'https://www.itspy.cz/sk/thesis/vypocetna-muzikologia-modely-metody-a-aplikacie/',
            },
        ],
    },
    {
        'badge': 'arXiv 2025',
        'title': 'Orchestration of Music by Grammar Systems',
        'subtitle': '',
        'authors': 'Jozef Makiš, Alexander Meduna, Zbyněk Křivka · VUT FIT Brno',
        'venue': 'EPTCS 422, 2025, pp. 45-58 · Formal Languages & Automata Theory (cs.FL)',
        'description': (
            'We define multi-generative rule-synchronized scattered-context grammar systems '
            '(without erasing rules) and demonstrate how to simultaneously arrange a musical '
            'composition for a full orchestra consisting of several instruments. Classical and '
            'jazz orchestration examples are provided, followed by five open problem areas '
            'related to this approach.'
        ),
        'links': [
            {'label': 'arXiv:2507.15314', 'url': 'https://arxiv.org/abs/2507.15314'},
            {'label': 'PDF', 'url': 'https://arxiv.org/pdf/2507.15314'},
            {'label': 'DOI 10.4204/EPTCS.422.4', 'url': 'https://doi.org/10.4204/EPTCS.422.4'},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with research publication entries.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Only clear existing publication entries, do not seed.',
        )
        parser.add_argument(
            '--project-title',
            default='Computational Musicology & Grammar Systems',
            help='Project title to attach publications to.',
        )

    def handle(self, *args, **options):
        project_title = options['project_title']

        if options['clear_only']:
            count = Publication.objects.count()
            Publication.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {count} publication(s).'))
            return

        try:
            project = Project.objects.get(title=project_title)
        except Project.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Project with title "{project_title}" does not exist. '
                    'Run seed_projects first or pass --project-title.'
                )
            )
            return

        Publication.objects.filter(project=project).delete()
        self.stdout.write(f'Cleared existing publications for project: {project.title}')

        for data in PUBLICATIONS_DATA:
            publication = Publication.objects.create(project=project, **data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {publication.title}'))

        total = Publication.objects.filter(project=project).count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSeeded {total} publication(s) for project: {project.title}'
            )
        )
