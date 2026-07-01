"""
Management command to seed the database with work experience entries.

Usage:
    python manage.py seed_aboutme
    python manage.py seed_aboutme
"""

from django.core.management.base import BaseCommand
from projects.models import AboutItem


ABOUT_ME_DATA = [
    {
        'order': 1,
        'icon': '🧑‍💻',
        'title': 'Who am I?',
        'text': "I'm a Slovak software developer with a background in computer science research, currently working in aerospace and avionics. I build things: research prototypes, automation scripts, full-stack applications and cloud systems.",
    },
    {
        'order': 2,
        'icon': '🎓',
        'title': 'Education',
        'text': "Master's degree (Ing.) from the Faculty of Information Technology, Brno University of Technology (VUT FIT). My studies covered formal grammars, music informatics, machine learning, computer vision and AI. My thesis sits at the intersection of formal language theory and computational musicology.",
    },
    {
        'order': 3,
        'icon': '🎵',
        'title': 'Interests',
        'text': 'Music informatics, computer vision, formal language theory, game automation, aerospace & avionics systems, and building tools that make repetitive work disappear.',
    },
]

class Command(BaseCommand):
    help = "Seeds the database with 'About Me' section data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding About Me items...")

        for data in ABOUT_ME_DATA:
            item, created = AboutItem.objects.get_or_create(
                title=data['title'],
                defaults={
                    'icon': data['icon'],
                    'text': data['text'],
                    'order': data['order']
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created: {item.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Skipped (Already exists): {item.title}'))

        total = AboutItem.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\nDatabase seeding complete. Total About Items in DB: {total}'
            )
        )
