#!/usr/bin/env python3.5

"""
guillaumecantin.pythonanywhere.com/simulation
Web interface for simulating dynamical systems
Current file: tests.py
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from random import random, randint

class TestViews(TestCase):

    def test_url_about(self):
        print('\nTest about view.')
        self.c = Client()
        self.r = self.c.get('/about/')
        self.assertEqual(self.r.status_code, 200)
        print('Status:', self.r.status_code)

    def test_login(self):
        print('\nTest login.')
        self.c = Client()
        self.user = User.objects.create(username='testuser', password='12345', is_active=True, is_staff=False, is_superuser=False)
        self.user.set_password('hello')
        self.user.save()

        print('\nTest correct login.')
        self.user = authenticate(username='testuser', password='hello')
        login = self.c.login(username='testuser', password='hello')
        self.assertTrue(login)
        print('Response:', login)
        self.c.logout()

        print('\nTest invalid login.')
        badlogin = self.c.login(username='testuser', password='hellO')
        self.assertFalse(badlogin)
        self.r = self.c.post('/login/', {'username': 'testuser', 'password': 'hellO'})
        self.assertEqual(self.r.status_code, 200)
        print('Status:', self.r.status_code)
        print('Response:', badlogin)
        self.assertIn(b'Invalid login', self.r.content)

    def test_fhn(self):
        print('\nTest fhn view.')
        self.c = Client()

        print('\nTest correct post.')
        self.r = self.c.get('/fhn/')
        randomnumber = random()
        self.r = self.c.post('/fhn/', {'c': str(randomnumber)})
        self.assertEqual(self.r.status_code, 200)
        self.assertIn(b'can make many simulations', self.r.content)
        print('Post:', str(randomnumber))
        print('Status:', self.r.status_code)

        print('\nTest invalid post.')
        self.r = self.c.get('/fhn/')
        randomstring = ''
        length = randint(1, 10)
        for k in range(length):
            randomstring = randomstring + chr(randint(1, 100))
        self.r = self.c.post('/fhn/', {'c': randomstring})
        self.assertEqual(self.r.status_code, 200)
        self.assertIn(b'must enter', self.r.content)
        print('Post:', randomstring)
        print('Status:', self.r.status_code)

