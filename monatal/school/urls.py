from django.urls import path, include
from .views import SchoolViewSet, StudentViewSet, LinkedStudentViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register('school', SchoolViewSet, basename='school')
router.register('student', StudentViewSet, basename='student')

nested_routers = NestedDefaultRouter(router, r'school', lookup='school')
nested_routers.register('student', LinkedStudentViewSet, basename='student-school')


school_urls = [
    path('', include(router.urls)),
    path('', include(nested_routers.urls)),
]
