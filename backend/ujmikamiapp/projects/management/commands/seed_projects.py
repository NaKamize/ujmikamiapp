"""
Management command to seed the database with project entries.

Usage:
    python manage.py seed_projects
    python manage.py seed_projects --clear-only
"""

from django.core.management.base import BaseCommand
from projects.models import Project, ProjectLink, Tag


TAGS_DATA = [
    {'name': 'Game Automation'},
    {'name': 'Azure'},
    {'name': 'DevOps'},
    {'name': 'Aerospace'},
    {'name': 'Formal Grammars'},
    {'name': 'Image Processing'},
    {'name': 'Music Informatics'},
    {'name': 'Python'},
    {'name': 'Computer Vision'},
    {'name': 'JavaScript'},
    {'name': 'Data Engineering'},
    {'name': 'Transfer Learning'},
]

PROJECTS_DATA = [
    {
        'title': 'ACARS Onboarding Maintenance System',
        'description': (
            'Avionics automation and testing for ACARS-based onboard maintenance '
            'systems. Built test harnesses, simulated aircraft bus data, and '
            'automated regression suites for DO-178C compliant avionics software.'
        ),
        'category': 'aerospace',
        'image': '',
        'stat': 'DO-178C · automated test pipelines',
        'order': 1,
        'tag_names': ['Aerospace', 'Python', 'DevOps'],
        'links': [],
    },
    {
        'title': 'Azure Data Pipelines & Infrastructure',
        'description': (
            'Built data pipelines with Azure Databricks and Data Factory. '
            'Deployed infrastructure via Terraform, automated CI/CD with '
            'GitHub Actions. Focus on reliable, repeatable cloud deployments.'
        ),
        'category': 'cloud',
        'image': 'projects/microsoft_azure.png',
        'stat': 'Databricks · Data Factory · Terraform',
        'order': 2,
        'tag_names': ['Azure', 'Data Engineering', 'DevOps'],
        'links': [],
    },
    {
        'title': 'U-Net Image Upscaling with Transfer Learning',
        'description': (
            'Applied transfer learning with U-Net and Stable Diffusion for '
            'image upscaling. Fine-tuned pre-trained models on domain-specific '
            'datasets to improve resolution while preserving fine details.'
        ),
        'category': 'cv',
        'image': '',
        'stat': 'U-Net · Stable Diffusion · transfer learning',
        'order': 3,
        'tag_names': ['Computer Vision', 'Image Processing', 'Transfer Learning', 'Python'],
        'links': [],
    },
    {
        'title': 'GrepolisBot — Game Automation Userscript',
        'description': (
            'Tampermonkey userscript for Grepolis. Automates farming, culture '
            'celebrations, silver vault management, and attack dodging. '
            'Draggable panel UI. Built with ES modules and esbuild.'
        ),
        'category': 'automation',
        'image': '',
        'stat': '71 installs · 4 automation modules',
        'order': 4,
        'tag_names': ['Game Automation', 'JavaScript', 'DevOps'],
        'links': [
            {'label': 'GreasyFork', 'url': 'https://greasyfork.org/en/scripts/468760-grepolisbot'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/GrepolisBot'},
        ],
    },
    {
        'title': 'Music Grammar Orchestrator',
        'description': (
            'Generates multi-instrument orchestrations using multi-generative '
            'grammar systems. Takes a symbolic melody and produces a full '
            'orchestral score. Published at EPTCS 2025.'
        ),
        'category': 'ml',
        'image': '',
        'stat': 'EPTCS 422 · arXiv:2507.15314',
        'order': 5,
        'tag_names': ['Formal Grammars', 'Music Informatics', 'Python'],
        'links': [
            {'label': 'arXiv Paper', 'url': 'https://arxiv.org/abs/2507.15314'},
            {'label': 'GitHub Repo', 'url': 'https://github.com/NaKamize/music-grammar-orchestrator'},
        ],
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with project entries.'

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
            project = Project.objects.create(**data)
            for tag_name in tag_names:
                if tag_name in tag_map:
                    project.tags.add(tag_map[tag_name])
            for link_data in links:
                ProjectLink.objects.create(project=project, **link_data)
            self.stdout.write(self.style.SUCCESS(f'  ✓ {project.title}'))

        total = Project.objects.count()
        self.stdout.write(self.style.SUCCESS(f'\nSeeded {total} project(s).'))
