from django.db import models
from subjects.base_model import BaseModel
from django.utils.text import slugify
from teachers.models import Teacher
from django.urls import reverse


class Group(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    GRADE_LEVEL = [
        ('grade_9', 'Grade 9'),
        ('grade_10', 'Grade 10'),
        ('grade_11', 'Grade 11'),

    ]

    SCHEDULE_CHOICES = [
        ('morning_session', 'Morning Session'),
        ('afternoon_session', 'Afternoon Session'),
        ('evening_session', 'Evening Session')
    ]


    group_name = models.CharField(max_length=50)
    class_teacher = models.OneToOneField(Teacher, on_delete=models.SET_NULL, null=True, related_name='group')
    academic_year = models.PositiveIntegerField()
    grade_level = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    max_students = models.PositiveIntegerField()
    description = models.TextField()
    subjects = models.ManyToManyField('subjects.Subject', related_name='groups')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='inactive')
    slug = models.SlugField(unique=True)

    @property
    def teacher_count(self):
        return self.teachers.count()

    @property
    def student_count(self):
        return self.students.count()


    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.group_name)
            slug = base_slug
            counter = 1
            while Group.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super(Group, self).save(*args, **kwargs)


    def get_detail_url(self):
        return reverse(
            'groups:detail',
            kwargs={
                'year': self.created_at.year,
                'month': self.created_at.month,
                'day': self.created_at.day,
                'slug': self.slug
            })


    def get_update_url(self):
        return reverse('groups:update', args=[self.pk])

    def get_delete_url(self):
        return reverse('groups:delete', args=[self.pk])


