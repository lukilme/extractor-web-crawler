import tempfile
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User
from .views import SignUpView, login_view, profile_edit_view

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             email='test@example.com',
                                             password='testpass123',
                                             user_type='comum')

    def test_user_creation(self):

        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.user_type, 'comum')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str_method(self):
        expected_str = f"testuser (Usuário Comum)"
        self.assertEqual(str(self.user), expected_str)



class CustomUserCreationFormTest(TestCase):

    def test_form_valid_data(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'user_type': 'comum',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):

        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'user_type': 'comum',
            'password1': 'password123',
            'password2': 'differentpassword123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_save(self):
        form_data = {
            'username': 'formuser',
            'email': 'formuser@example.com',
            'user_type': 'admin',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'formuser')
        self.assertEqual(user.user_type, 'admin')
        self.assertTrue(user.check_password('testpass123'))


class UserProfileFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='profileuser',
                                             email='profile@example.com',
                                             password='testpass123')

    def test_profile_form_valid_data(self):
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'bio': 'Uma breve biografia sobre mim.',
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_form_save(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane.doe@example.com',
            'bio': 'Nova biografia atualizada.',
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.bio, 'Nova biografia atualizada.')


class AuthenticationViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser',
                                             password='testpass123',
                                             user_type='comum')
        self.admin_user = User.objects.create_user(username='adminview',
                                                   password='adminpass123',
                                                   user_type='admin')

    def test_signup_view_get(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_signup_view_post_success(self):
        response = self.client.post(
            reverse('accounts:signup'), {
                'username': 'newuser',
                'email': 'new@example.com',
                'user_type': 'comum',
                'password1': 'complexpass123',
                'password2': 'complexpass123',
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))

        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_get_authenticated(self):
        self.client.login(username='viewuser', password='testpass123')
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'viewuser',
            'password': 'testpass123',
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('news:feed'))

    def test_login_view_post_admin(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'adminview',
            'password': 'adminpass123',
        })

        self.assertEqual(response.status_code, 302)

    def test_login_view_post_failure(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'viewuser',
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha incorretos')

    def test_logout_view(self):
        self.client.login(username='viewuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))

        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)


class ProfileViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='profiletest',
                                             password='testpass123')
        self.client.login(username='profiletest', password='testpass123')

    def test_profile_view_authenticated(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_view_get(self):
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')
        self.assertIsInstance(response.context['form'], UserProfileForm)

    def test_profile_edit_view_post_success(self):
        response = self.client.post(
            reverse('accounts:profile_edit'), {
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': 'updated@example.com',
                'bio': 'Biografia atualizada',
            })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.bio, 'Biografia atualizada')

    def test_profile_edit_view_with_avatar(self):
        image = Image.new('RGB', (100, 100), color='red')
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        with open(tmp_file.name, 'rb') as img:
            response = self.client.post(
                reverse('accounts:profile_edit'), {
                    'first_name':
                    'Avatar',
                    'last_name':
                    'User',
                    'email':
                    'avatar@example.com',
                    'bio':
                    'Usuário com avatar',
                    'avatar':
                    SimpleUploadedFile('test_avatar.jpg',
                                       img.read(),
                                       content_type='image/jpeg')
                })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile'))

        self.user.refresh_from_db()
        self.assertIsNotNone(self.user.avatar)


class MiddlewareAndDecoratorsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='middlewareuser',
                                             password='testpass123')

    def test_login_required_decorator(self):

        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)

    def test_user_type_choices(self):

        choices = User.USER_TYPE_CHOICES
        self.assertEqual(len(choices), 2)
        self.assertIn(('comum', 'Usuário Comum'), choices)
        self.assertIn(('admin', 'Administrador'), choices)
