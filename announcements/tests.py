import pytest
from rest_framework import status
from django.urls import reverse
from announcements.models import Announcement, Review
from users.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    return User.objects.create(
        email="test@yandex.ru", password="12345", role="user"
    )


@pytest.fixture
def create_admin(db):
    return User.objects.create(
        email="admin@yandex.ru", password="12345", role="admin"
    )


@pytest.fixture
def create_announcement(db, create_user):
    return Announcement.objects.create(
        author=create_user,
        title="Объявление",
        description="Описание",
        price=100,
    )


@pytest.fixture
def admin_create_announcement(db, create_admin):
    return Announcement.objects.create(
        author=create_admin,
        title="Объявление админа",
        description="Описание админа",
        price=150,
    )


def test_user_create_announcement(api_client, create_user):
    api_client.force_authenticate(user=create_user)

    url = reverse("announcements:announcement-list")
    data = {
        "author": create_user.id,
        "title": "Новое объявление",
        "description": "Новое описание для объявления",
        "price": 150,
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Announcement.objects.count() == 1
    assert Announcement.objects.get().title == "Новое объявление"


def test_user_can_view_own_announcement(api_client, create_user, create_announcement):
    api_client.force_authenticate(user=create_user)

    url = reverse("announcements:announcement-detail", args=[create_announcement.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == create_announcement.title


def test_user_can_update_own_announcement(api_client, create_user, create_announcement):
    api_client.force_authenticate(user=create_user)

    url = reverse("announcements:announcement-detail", args=[create_announcement.id])
    data = {
        "author": create_user.id,
        "title": "Обновленное объявление",
        "description": "Обновленное описание для объявления",
        "price": 200,
    }

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Announcement.objects.get().title == "Обновленное объявление"


def test_user_can_delete_own_announcement(api_client, create_user, create_announcement):
    api_client.force_authenticate(user=create_user)

    url = reverse("announcements:announcement-detail", args=[create_announcement.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Announcement.objects.count() == 0


def test_user_cannot_delete_any_announcement(api_client, create_user, admin_create_announcement):
    api_client.force_authenticate(user=create_user)

    url = reverse("announcements:announcement-detail", args=[admin_create_announcement.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Announcement.objects.count() == 1


def test_admin_can_delete_any_announcement(api_client, create_admin, create_announcement):
    api_client.force_authenticate(user=create_admin)

    url = reverse("announcements:announcement-detail", args=[create_announcement.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Announcement.objects.count() == 0


def test_user_can_create_review(api_client, create_user, create_announcement):
    api_client.force_authenticate(user=create_user)

    url = reverse("announcements:review-list")
    data = {
        "author": create_user.id,
        "announcement": create_announcement.id,
        "text": "Новый отзыв",
    }

    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Review.objects.count() == 1
    assert Review.objects.get().text == "Новый отзыв"


def test_user_can_delete_review(api_client, create_user, create_announcement):
    api_client.force_authenticate(user=create_user)
    review = Review.objects.create(author=create_user, ad=create_announcement, text="Отзыв")

    response = api_client.delete(
        reverse("announcements:review-detail", kwargs={"pk": review.id})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


def test_admin_can_delete_any_review(api_client, create_admin, create_user, create_announcement):
    api_client.force_authenticate(user=create_admin)
    review = Review.objects.create(author=create_user, ad=create_announcement, text="Отзыв")

    response = api_client.delete(
        reverse("announcements:review-detail", kwargs={"pk": review.id})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_anonymous_user_can_view_announcements(api_client):
    response = api_client.get(reverse("announcements:announcement-list"))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_anonymous_user_cannot_create_announcement(api_client):
    response = api_client.post(
        reverse("announcements:announcement-list"),
        {
            "title": "Недоступное объявление",
            "description": "Это не должно пройти",
            "price": 1000,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_create_review(api_client, create_announcement):
    response = api_client.post(
        reverse("announcements:review-list"),
        {
            "author": 1,
            "announcement": create_announcement.id,
            "text": "Новый отзыв о телефоне.",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_anonymous_user_cannot_view_review(api_client):
    response = api_client.get(reverse("announcements:review-list"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
