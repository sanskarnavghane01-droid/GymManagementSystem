from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


class LoginRedirectTests(TestCase):
    def test_trainer_login_redirects_to_original_page(self):
        trainer_group = Group.objects.create(name='Trainer')
        user = User.objects.create_user(
            username='trainer1',
            email='trainer@example.com',
            password='strong-password-123',
        )
        user.groups.add(trainer_group)

        response = self.client.post(
            reverse('login'),
            {
                'email': 'trainer@example.com',
                'password': 'strong-password-123',
                'is_trainer': 'on',
                'next': '/trainers/',
            },
            follow=False,
        )

        self.assertRedirects(response, reverse('trainer_dashboard'))


# Create your tests here.
