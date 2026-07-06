"""
Management command to seed the database with project entries.

Usage:
    python manage.py seed_projects
    python manage.py seed_projects --clear-only
"""

from django.core.management.base import BaseCommand
from django.core.files import File
from pathlib import Path
from projects.models import Project, ProjectLink, Tag


TAGS_DATA = [
    {'name': 'Python'},
    {'name': 'Data Engineering'},
    {'name': 'Azure'},
    {'name': 'Computer Vision'},
    {'name': 'Machine Learning'},
    {'name': 'Full-Stack'},
    {'name': 'React'},
    {'name': 'Django REST'},
    {'name': 'Hardware Testing'},
    {'name': 'Music Informatics'},
    {'name': 'Formal Grammars'},
    {'name': 'Web Scraping'},
    {'name': 'TypeScript'}

]

PROJECTS_DATA = [
    {
        'title': 'Hardware Onboarding Maintenance System Testing',
        'description': (
            'Built and maintained system test suites for an onboarding '
            'maintenance system running on custom hardware. '
            'Utilized internal Python frameworks to verify hardware-level behavior '
            'and supported root cause investigation.'
        ),
        'category': 'testing',
        'image': 'projects/plane.jpg',
        'stat': 'Python · Hardware Validation',
        'order': 1,
        'tag_names': ['Hardware Testing', 'Python'],
        'links': [],
    },
    {
        'title': 'Azure Data Pipelines & Infrastructure',
        'description': (
            'Developed workflows for a cloud enterprise information system in Microsoft Azure. '
            'Migrated legacy U-SQL jobs into PySpark and Databricks workflows, '
            'and implemented routine data processing and validation using SQL.'
        ),
        'category': 'cloud',
        'image': 'projects/microsoft_azure.png',
        'stat': 'Databricks · PySpark · Azure',
        'order': 2,
        'tag_names': ['Azure', 'Data Engineering', 'Python'],
        'links': [],
    },
    {
        'title': 'Computer Vision: Upscaling & Tracking',
        'description': (
            'Completed applied computer vision projects utilizing Stable Diffusion '
            'for image upscaling and YOLO for vehicle speed estimation and tracking. '
            'Leveraged OpenCV for core image and video processing tasks.'
        ),
        'category': 'cv',
        'image': 'projects/mozaika_comparison_2.png',
        'stat': 'Stable Diffusion · YOLO · OpenCV',
        'order': 3,
        'tag_names': ['Computer Vision', 'Machine Learning', 'Python'],
        'links': [],
    },
    {
        'title': 'Personal Portfolio Platform',
        'description': (
            'Designed and built a full-stack portfolio application using React and TypeScript '
            'on the frontend with a Django REST backend. '
            'Configured APIs for project management and deployed locally using Docker Compose.'
        ),
        'category': 'fullstack',
        'image': '',
        'stat': 'React · TypeScript · Django REST',
        'order': 4,
        'tag_names': ['Full-Stack', 'React', 'Django REST', 'Python'],
        'links': [],
    },
    {
        'title': 'Computational Musicology & Grammar Systems',
        'description': (
            'Master\'s thesis selected among top student IT projects in CZ and SK (IT SPY 2025). '
            'Generates multi-instrument orchestrations using multi-generative grammar systems. '
            'Co-authored publication "Orchestration of Music by Grammar Systems".'
        ),
        'category': 'ml',
        'image': 'projects/music.png',
        'stat': 'IT SPY 2025 · EPTCS 422',
        'order': 5,
        'tag_names': ['Formal Grammars', 'Music Informatics', 'Python'],
        'links': [
            {'label': 'arXiv Paper', 'url': 'https://arxiv.org/abs/2507.15314'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/music-grammar-orchestrator'},
        ],
    },
    {
        'title': 'Grepolis Game Bot',
        'description': (
            'Designed and implemented automated bot for the web-based strategy game Grepolis. '
            'Currently it has the biggest popularity in slovak game scene with 77 downloads and more. '
            'Application is built within tempermonkey extension using typescript. '
        ),
        'category': 'fullstack',
        'image': 'projects/grepolisbot_preview.png',
        'stat': 'Typescript, Web Scraping, Web Development',
        'order': 6,
        'tag_names': ['Web Scraping', 'Typescript'],
        'links': [
            {'label': 'Geasyfork', 'url': 'https://greasyfork.org/en/scripts/468760-grepolisbot'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/GrepolisBot'},
        ],
    }
]


class Command(BaseCommand):
    help = 'Seeds the database with project entries.'

    @staticmethod
    def _upload_project_image(project, image_path):
        if not image_path:
            return

        project_root = Path(__file__).resolve().parents[3]
        local_image_path = project_root / 'media' / image_path
        if not local_image_path.exists():
            return

        with local_image_path.open('rb') as image_file:
            project.image.save(local_image_path.name, File(image_file), save=True)

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Only clear existing entries, do not seed.',
        )

    def handle(self, *args, **options):
        if options['clear_only']:
            count = Project.objects.count()
            Project.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Cleared {count} project(s) and all tags.'))
            return

        # Clear existing
        Project.objects.all().delete()
        Tag.objects.all().delete()
        self.stdout.write('Cleared existing projects and tags.')

        # Create tags
        tag_map = {}
        for tag_data in TAGS_DATA:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            tag_map[tag.name] = tag
        self.stdout.write(f'  ✓ Created {len(tag_map)} tags.')

        # Create projects
        for data in PROJECTS_DATA:
            tag_names = data.pop('tag_names', [])
            links = data.pop('links', [])
            image_path = data.pop('image', '')
            project = Project.objects.create(**data)
            self._upload_project_image(project, image_path)
            for tag_name in tag_names:
                if tag_name in tag_map:
                    project.tags.add(tag_map[tag_name])
            for link_data in links:
                ProjectLink.objects.create(project=project, **link_data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {project.title}'))

        total = Project.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nSeeded {total} project(s).'))
