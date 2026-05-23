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
        'company': 'Aerospace & Avionics Company',
        'role': 'Software Engineer',
        'period': '2024 – Present',
        'location': 'Slovakia / Remote',
        'description': (
            'Developing and maintaining safety-critical avionics software. '
            'Working across embedded systems and ground-support tooling, '
            'contributing to DO-178C compliant pipelines and automated test '
            'infrastructure.'
        ),
        'current': True,
        'order': 1,
        'technologies': [
            {'label': 'Python'},
            {'label': 'C/C++'},
            {'label': 'DO-178C'},
            {'label': 'CI/CD'},
            {'label': 'Linux'},
        ],
    },
    {
        'company': 'VUT FIT Brno — Research',
        'role': "Master's Researcher / Teaching Assistant",
        'period': '2022 – 2024',
        'location': 'Brno, Czech Republic',
        'description': (
            'Conducted research at the intersection of formal language theory '
            'and computational musicology. Co-authored a peer-reviewed paper on '
            'multi-generative grammar systems for music orchestration (EPTCS 2025). '
            'Assisted in lecturing and lab sessions for formal languages and '
            'automata courses.'
        ),
        'current': False,
        'order': 2,
        'technologies': [
            {'label': 'Python'},
            {'label': 'Formal Grammars'},
            {'label': 'Music Informatics'},
            {'label': 'LaTeX'},
            {'label': 'Research'},
        ],
    },
    {
        'company': 'Freelance / Open Source',
        'role': 'Full-Stack Developer',
        'period': '2021 – Present',
        'location': 'Remote',
        'description': (
            'Built full-stack web applications and automation scripts for '
            'various clients. Projects span game automation (browser userscripts '
            'with 1 000+ users on GreasyFork), computer-vision pipelines, cloud '
            'deployments on Microsoft Azure, and this portfolio.'
        ),
        'current': False,
        'order': 3,
        'technologies': [
            {'label': 'React'},
            {'label': 'TypeScript'},
            {'label': 'Django'},
            {'label': 'Azure'},
            {'label': 'Docker'},
            {'label': 'PostgreSQL'},
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
