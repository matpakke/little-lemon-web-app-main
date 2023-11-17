from django.test import TestCase
from restaurant.models import Menu
from LittleLemonAPI.models import MenuItem

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from LittleLemonAPI.serializers import MenuItemSerializer
from django.contrib.auth.models import User


# TestCase class
class MenuItemTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")


# # TestCase class
# class TestMenu(TestCase):
#     def test_get_item(self):
#         item = Menu.objects.create(title="Pizza", price=80, inventory=100)
#         self.assertEqual(item.title, "Pizza")


class MenuViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="max", password="backeND-219")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create test instances of Menu model
        MenuItem.objects.create(title="Pizza", price=9.99, inventory=100)
        MenuItem.objects.create(title="Pasta", price=50, inventory=100)
        # ... other instances ...

    def test_getall(self):
        # Use the authenticated client from setUp
        response = self.client.get(
            reverse("menu-items")
        )  # Make sure "menu-items" is the correct URL name

        menus = MenuItem.objects.all()
        serializer = MenuItemSerializer(menus, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
