"""
Management command to seed the database with work experience entries.

Usage:
    python manage.py seed_experiences
    python manage.py seed_experiences --clear-only
"""

from django.core.management.base import BaseCommand
from projects.models import WorkExperience, WorkExperienceTechnology


EXPERIENCES_DATA = [
    {
        'company': 'Honeywell',
        'role': 'Software Engineer I',
        'period': 'Jul 2024 – Present',
        'location': 'Brno, Czech Republic',
        'description': (
            'I work on system test suites for an onboarding maintenance system running '
            'on custom hardware. I utilize internal Python frameworks to verify behavior '
            'at the hardware level and support failure analysis and root cause investigation '
            'across both software and hardware.'
        ),
        'current': True,
        'order': 1,
        'technologies': [
            {'label': 'Python'},
            {'label': 'SQL'},
            {'label': 'REST API'},
            {'label': 'Linux'}, 
            {'label': 'Testing'},
        ],
    },
    {
        'company': 'Anthology Inc.',
        'role': 'Software Developer Intern',
        'period': 'Apr 2023 – Apr 2024',
        'location': 'Brno, Czech Republic',
        'description': (
            'I worked on a cloud enterprise information system within Microsoft Azure. '
            'My main responsibilities included migrating legacy U-SQL jobs into PySpark '
            'and Databricks workflows, using SQL daily for data processing and validation, '
            'and supporting the backend data workflow implementation.'
        ),
        'current': False,
        'order': 2,
        'technologies': [
            {'label': 'Python'},
            {'label': 'PySpark'},
            {'label': 'Databricks'},
            {'label': 'Azure'},
            {'label': 'SQL'},
        ],
    },
    {
        'company': 'Independent Research & Projects',
        'role': 'Graduate Researcher & Developer',
        'period': '2022 – Present',
        'location': 'Brno, Czech Republic',
        'description': (
            'I developed a Master\'s thesis on Computational Musicology that was recognized '
            'among the top student IT projects in Czechia and Slovakia in the IT SPY 2025 competition, '
            'and co-authored an international scientific publication on music grammar systems (EPTCS 422). '
            'In my free time, I continue to build personal software projects, including designing and '
            'developing a full-stack Personal Portfolio Platform using React, TypeScript, and Django REST.'
        ),
        'current': False,
        'order': 3,
        'technologies': [
            {'label': 'Python'},
            {'label': 'React'},
            {'label': 'TypeScript'},
            {'label': 'Django REST'},
            {'label': 'Docker Compose'},
            {'label': 'Formal Grammars'},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with work experience entries.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Only clear existing entries, do not seed.',
        )

    def handle(self, *args, **options):
        if options['clear_only']:
            count = WorkExperience.objects.count()
            WorkExperience.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {count} experience(s).'))
            return

        # Clear existing
        WorkExperience.objects.all().delete()
        self.stdout.write('Cleared existing work experiences.')

        for data in EXPERIENCES_DATA:
            technologies = data.pop('technologies', [])
            experience = WorkExperience.objects.create(**data)
            for tech_data in technologies:
                WorkExperienceTechnology.objects.create(
                    experience=experience, **tech_data
                )
            self.stdout.write(self.style.SUCCESS(f'  ✓ {experience.role} at {experience.company}'))

        total = WorkExperience.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nSeeded {total} work experience(s).'))
