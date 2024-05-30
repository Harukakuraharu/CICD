from django.urls import reverse
from rest_framework.test import APIClient

import pytest
from model_bakery import baker

from students.models import Course, Student


#Создание фикстур
@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory



pytestmark = pytest.mark.django_db


# @pytest.mark.django_db
def test_get_first_course(client, course_factory):
    courses = course_factory()

    # response = client.get('/api/v1/courses/')
    response = client.get(reverse('courses-list'))
    data = response.json()[0]

    assert response.status_code == 200
    assert data['name'] == courses.name



# @pytest.mark.django_db
def test_get_list_course(client, course_factory):
    courses = course_factory(_quantity = 5)
    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    #Проверяем количество записей
    assert len(response.data) == len(courses)
    #Проверяем соответствие записей по полю 'name'
    for i, m in enumerate(data):
        assert m['name'] == courses[i].name


# @pytest.mark.django_db
def test_filtered_id(client, course_factory):
    courses = course_factory(_quantity = 5)
    response = client.get(f'/api/v1/courses/?id={courses[0].id}')
    data = response.json()[0]

    assert response.status_code == 200
    assert data['id'] == courses[0].id


# @pytest.mark.django_db
def test_filtered_name(client, course_factory):
    courses = course_factory(_quantity = 5)
    response = client.get(f'/api/v1/courses/?name={courses[3].name}')
    data = response.json()[0]

    assert response.status_code == 200
    assert data['name'] == courses[3].name



# @pytest.mark.django_db
def test_create_course(client):
    data = {'name': 'Python developer'}
    response = client.post('/api/v1/courses/', data=data)

    assert response.status_code == 201
    assert Course.objects.get().name == 'Python developer'
    assert Course.objects.count() == 1



# @pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory()
    print(courses)
    data = {'name': 'Java developer'}
    # response = client.put(f'/api/v1/courses/{courses[0].id}/', data=data)
    # response = client.put(reverse("courses-detail", kwargs={'pk': courses.id}), data=data)
    response = client.put(reverse("courses-detail", args=[courses.id]), data=data)
    data_response = response.json()

    assert response.status_code == 200
    assert data_response['name'] == data['name']
    assert Course.objects.get(pk=courses.id).name == data['name']




# @pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory()
    response = client.delete(reverse('courses-detail', args=[courses.id]))
    # response = client.delete(f'/api/v1/courses/{courses.id}/')

    assert response.status_code == 204
    assert Course.objects.count() == 0




@pytest.mark.parametrize(
        ['count'],
        (
            (20, ),
            (15, ),
        )
)
# @pytest.mark.django_db
def test_maxcount_student(count, settings):
    assert count <= settings.MAX_STUDENTS_PER_COURSE

