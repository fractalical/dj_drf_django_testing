from http import HTTPStatus

import pytest

from students.models import Course


@pytest.mark.django_db
def test_create_first_course(api_client, courses_factory):
    course = courses_factory(_quantity=1)

    response = api_client.get('/api/v1/courses/1/')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert course[0].name == data['name']


@pytest.mark.django_db
def test_create_many_courses(api_client, courses_factory):
    course = courses_factory(_quantity=15)

    response = api_client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    for i, m in enumerate(data):
        assert course[i].name == m['name']


@pytest.mark.django_db
def test_filter_id_courses(api_client, courses_factory):
    course = courses_factory(_quantity=5)

    course_number = 3
    filter_data = course[course_number].id
    response = api_client.get(f'/api/v1/courses/?id={filter_data}')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert course[course_number].id == data[0]['id']


@pytest.mark.django_db
def test_filter_name_courses(api_client, courses_factory):
    course = courses_factory(_quantity=5)

    course_number = 3
    filter_data = course[course_number].name
    response = api_client.get(f'/api/v1/courses/?name={filter_data}')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert course[course_number].name == data[0]['name']


@pytest.mark.django_db
def test_create_course(api_client):

    data = {
        "name": "test create course",
        "students": []
    }
    response = api_client.post(f'/api/v1/courses/', data=data, format='json')

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_update_course(api_client):

    data = {
        "name": "test update course",
        "students": []
    }
    api_client.post(f'/api/v1/courses/', data=data, format='json')

    course = Course.objects.last()
    new_data = {
        "name": "updated course"
    }
    response = api_client.patch(f'/api/v1/courses/{course.id}/', data=new_data,
                                format='json')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'updated course'


@pytest.mark.django_db
def test_delete_course(api_client):

    data = {
        "name": "test delete course",
        "students": []
    }
    api_client.post(f'/api/v1/courses/', data=data, format='json')

    course = Course.objects.last()
    response = api_client.delete(f'/api/v1/courses/{course.id}/')

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_correct_students_per_course(api_client, students_factory):

    students = students_factory(_quantity=30)

    data = {
        "name": "course1",
        "students": [s.id for s in students[:10]]
    }
    response = api_client.post(f'/api/v1/courses/', data=data, format='json')

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.django_db
def test_incorrect_students_per_course(api_client, students_factory):

    students = students_factory(_quantity=30)

    data = {
        "name": "course1",
        "students": [s.id for s in students]
    }
    response = api_client.post(f'/api/v1/courses/', data=data, format='json')

    assert response.status_code == HTTPStatus.BAD_REQUEST
