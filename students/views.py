from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view


from students.filters import CourseFilter
from students.models import Course
from students.serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = CourseFilter

@api_view(['GET'])
def sample_view(request):
    return Response({'message': 'мехехеехехехехеех'})
