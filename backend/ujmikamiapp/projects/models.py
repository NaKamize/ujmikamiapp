from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ml', 'Machine Learning'),
        ('cv', 'Computer Vision'),
        ('cloud', 'Cloud & InfoSys'),
        ('automation', 'Automation'),
        ('aerospace', 'Aerospace & Avionics'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    stat = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower = first)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title


class ProjectLink(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    label = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return f'{self.project.title} — {self.label}'


class WorkExperience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0, help_text='Display order (lower = first / most recent)')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.role} at {self.company}'


class WorkExperienceTechnology(models.Model):
    experience = models.ForeignKey(WorkExperience, on_delete=models.CASCADE, related_name='technologies')
    label = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.experience} — {self.label}'
