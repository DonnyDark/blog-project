from django.test import TestCase
from .models import CustomUser
from .views import LoginView, SignupView, UserView


class CustomUserTestCase(TestCase):

    def setUp(self):
        CustomUser.objects.create_user(username='User', email='User@mail.com', password='UserPass')
        CustomUser.objects.create_superuser(username='Superuser', email='Superuser@mail.com', password='SuperuserPass')

    def test_user(self):
        user = CustomUser.objects.get(username='User')
        self.assertEqual(user.email, 'User@mail.com')
        self.assertNotEqual(user.password, 'UserPass')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)

    def test_superuser(self):
        superuser = CustomUser.objects.get(username='Superuser')
        self.assertEqual(superuser.email, 'Superuser@mail.com')
        self.assertNotEqual(superuser.password, 'SuperuserPass')
        self.assertEqual(superuser.is_active, True)
        self.assertEqual(superuser.is_admin, True)

