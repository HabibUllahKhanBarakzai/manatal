from typing import Dict

from cerberus.validator import Validator
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..account.models import User
from ..account.views import BaseRegisterView, ValidatedModelViewSet
from .models import School, Student
from .serializers import SchoolSerializer, StudentSchoolSerializer, StudentSerializer
from .validations import (
    LINKED_STUDENT_SCHOOL_SCHEMA, STUDENT_VALIDATION_SCHEME, Schemas,
    SpecificEmailError,
)


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()


class StudentViewSet(BaseRegisterView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    validation_schema = STUDENT_VALIDATION_SCHEME
    validation_error_handler = SpecificEmailError

    @classmethod
    def create_type(cls, user: User, data: Dict):
        Student.objects.create(**{'user': user, **data})


class LinkedStudentViewSet(ValidatedModelViewSet):
    serializer_class = StudentSchoolSerializer
    queryset = School.objects.all()
    validation_schema = LINKED_STUDENT_SCHOOL_SCHEMA

    def create(self, request, school_pk=None, *args, **kwargs):
        request.data['school_id'] = school_pk
        return StudentViewSet().create(request, *args, **kwargs)

    def destroy(self, request, pk=None, school_pk=None,*args, **kwargs):
        instance = self.get_instance(**{'pk': pk, 'school__pk': school_pk})
        instance.delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk=None, school_pk=None, *args, **kwargs):
        instance = self.get_instance(**{'pk': pk, 'school__pk': school_pk})
        serializer = StudentSerializer(instance)
        return Response(serializer.data)

    @staticmethod
    def get_instance(**kwargs):
        try:
            return Student.objects.get(**kwargs)
        except ObjectDoesNotExist:
            raise ValidationError({'error': 'object not found'})

    def partial_update(self, request, pk=None, school_pk=None, *args, **kwargs):
        instance = self.get_instance(**{'pk': pk, 'school__pk': school_pk})
        basic_info = request.data.pop('user', None)
        if basic_info:
            instance.user.__dict__.update(**basic_info)
            instance.user.save()

        instance.__dict__.update(**request.data)
        instance.save()

        return Response({
            'user': {
                'first_name': instance.user.first_name,
                'last_name': instance.user.last_name,
                'email': instance.user.email,
            },
            'school': instance.school.name,
        })

