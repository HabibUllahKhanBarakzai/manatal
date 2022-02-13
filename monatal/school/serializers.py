from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer

from .models import School, Student


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class StudentSerializer(ModelSerializer):
    school = serializers.CharField(source='school.name')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Student
        fields = (
            'id',
            'school',
            'first_name',
            'last_name',
            'email',
            'identification_number',
        )


class StudentSchoolSerializer(NestedHyperlinkedModelSerializer):
    parent_lookup_kwargs = {
        'school_pk': 'school_pk',
    }

    students = StudentSerializer(many=True)

    class Meta:
        model = School
        fields = '__all__'
