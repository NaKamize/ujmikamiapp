from django.test import TestCase
from rest_framework.test import APIClient

from .models import (
    AboutItem,
    Project,
    ProjectLink,
    Publication,
    Tag,
    WorkExperience,
    WorkExperienceTechnology,
)


class ProjectAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tag = Tag.objects.create(name='Python')
        self.ml_project = Project.objects.create(
            title='ML Project',
            description='A machine learning project',
            category='ml',
            order=1,
        )
        self.ml_project.tags.add(self.tag)
        ProjectLink.objects.create(project=self.ml_project, label='GitHub', url='https://example.com')

        self.cv_project = Project.objects.create(
            title='CV Project',
            description='A computer vision project',
            category='cv',
            order=2,
        )

    def test_list_projects_returns_all(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_list_projects_ordered_by_order_field(self):
        response = self.client.get('/api/projects/')
        titles = [item['title'] for item in response.json()]
        self.assertEqual(titles, ['ML Project', 'CV Project'])

    def test_list_projects_includes_nested_tags_and_links(self):
        response = self.client.get('/api/projects/')
        ml_project_data = next(item for item in response.json() if item['title'] == 'ML Project')
        self.assertEqual(ml_project_data['tags'][0]['name'], 'Python')
        self.assertEqual(ml_project_data['links'][0]['label'], 'GitHub')

    def test_list_projects_filter_by_category(self):
        response = self.client.get('/api/projects/?category=cv')
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'CV Project')

    def test_detail_project(self):
        response = self.client.get(f'/api/projects/{self.ml_project.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'ML Project')
        self.assertEqual(response.json()['category_display'], 'Machine Learning')

    def test_detail_project_not_found(self):
        response = self.client.get('/api/projects/9999/')
        self.assertEqual(response.status_code, 404)


class WorkExperienceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.recent = WorkExperience.objects.create(
            company='Honeywell',
            role='Software Engineer I',
            period='Jul 2024 to Present',
            description='System test suites',
            current=True,
            order=0,
        )
        WorkExperienceTechnology.objects.create(experience=self.recent, label='Python')

        self.older = WorkExperience.objects.create(
            company='Anthology Inc.',
            role='Software Developer Intern',
            period='Apr 2023 to Apr 2024',
            description='Cloud data workflows',
            current=False,
            order=1,
        )

    def test_list_experiences_returns_all_ordered(self):
        response = self.client.get('/api/experiences/')
        self.assertEqual(response.status_code, 200)
        companies = [item['company'] for item in response.json()]
        self.assertEqual(companies, ['Honeywell', 'Anthology Inc.'])

    def test_list_experiences_includes_technologies(self):
        response = self.client.get('/api/experiences/')
        honeywell = next(item for item in response.json() if item['company'] == 'Honeywell')
        self.assertEqual(honeywell['technologies'][0]['label'], 'Python')


class PublicationAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        project = Project.objects.create(title='Thesis Project', description='...', category='other')
        Publication.objects.create(
            project=project,
            badge='EPTCS 422',
            title='Orchestration of Music by Grammar Systems',
            authors='Jozef Makis',
            venue='EPTCS',
            description='Co-authored publication',
        )

    def test_list_publications(self):
        response = self.client.get('/api/publications/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Orchestration of Music by Grammar Systems')


class AboutItemAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        AboutItem.objects.create(icon='🧑‍💻', title='Who am I?', text='...', order=1)
        AboutItem.objects.create(icon='🎓', title='Education', text='...', order=0)

    def test_list_about_items_ordered(self):
        response = self.client.get('/api/about/')
        self.assertEqual(response.status_code, 200)
        titles = [item['title'] for item in response.json()]
        self.assertEqual(titles, ['Education', 'Who am I?'])
