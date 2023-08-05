from django.test import TestCase
# from selenium import webdriver

from .models import ActorCategory, Actor
from .models import ActivityReason, Activity

# Tests for Actor models
class ActorTestCase(TestCase):
    def setUp(self):

        self.category1 = ActorCategory.objects.create(
            name = 'Founder',
        )
        self.category2 = ActorCategory.objects.create(
            name = 'Contributor',
        )

        self.actor1 = Actor.objects.create(
            name = f'Jeremy Actor Test',
            email = 'jeremy@gmail.com',
            category = ActorCategory.objects.get(name = 'Founder'),
            cellphone = '(10) 98765-4321',
            telephone = '55 4433-2211',
        )
        self.actor2 = Actor.objects.create(
            name = f'John Actor Test',
            email = 'john@gmail.com',
            category = ActorCategory.objects.get(name = 'Contributor'),
            cellphone = '(11) 98765-4321',
            telephone = '66 4433-2211',
        )

        # self.reason1 = ActivityReason.objects.create(
        #     name = 'Temporary Installation',
        #     type = 'INSTALL',
        # )
        # self.reason2 = ActivityReason.objects.create(
        #     name = 'Temporary Remotion',
        #     type = 'REMOVE',
        # )

    def test_actor_models(self):

        self.assertEqual(self.actor1.name, 'Jeremy Actor Test')
        self.assertEqual(self.actor1.email, 'jeremy@gmail.com')
        self.assertEqual(self.actor1.category.name, 'Founder')
        self.assertEqual(self.actor1.cellphone, '(10) 98765-4321')
        self.assertEqual(self.actor1.telephone, '55 4433-2211')
        self.assertEqual(self.actor1.first_name, 'Jeremy')

        self.assertEqual(self.actor2.name, 'John Actor Test')
        self.assertEqual(self.actor2.email, 'john@gmail.com')
        self.assertEqual(self.actor2.category.name, 'Contributor')
        self.assertEqual(self.actor2.cellphone, '(11) 98765-4321')
        self.assertEqual(self.actor2.telephone, '66 4433-2211')
        self.assertEqual(self.actor2.first_name, 'John')
