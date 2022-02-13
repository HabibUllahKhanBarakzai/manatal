from uuid import uuid4

from django.db import models
from django.http.response import Http404


class Student(models.Model):
    user = models.OneToOneField(
        'account.User',
        related_name='student',
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(
        'school.School', related_name='students', on_delete=models.CASCADE)
    identification_number = models.UUIDField(default=uuid4)

    def __str__(self):
        return f'{self.user.first_name}'

    def validate_maximum_students_allowed(self):
        students_in_this_school = self.__class__.objects.filter(school_id=self.school_id).count()
        if self.school.total_students_allowed <= students_in_this_school:
            raise Http404('Maximum Students Limit Reached')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        print("self.state", self._state.adding)
        if self._state.adding:
            self.validate_maximum_students_allowed()
        return super(Student, self).save(force_insert=False,
                                         force_update=False,
                                         using=None,
                                         update_fields=None)


class School(models.Model):
    name = models.CharField(max_length=256)
    total_students_allowed = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}'
