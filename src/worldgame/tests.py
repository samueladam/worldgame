import unittest

from django.test import Client
from django.contrib.auth.models import User

from .models import Country
from .forms import CountryForm

class CountryTest(unittest.TestCase):
    def setUp(self):
        "Runs before each call to a test method."
        self.user = User.objects.create_user(username='tester',
                                             email='tester@dom.ext',
                                             password='pass')
        
        self.country = Country.objects.create(name='test', user=self.user)

        self.client = Client()

    def tearDown(self):
        "Runs after each test method."
        self.user.delete()


    def test_form(self):
        # empty form
        form = CountryForm()
        self.assertEqual(form.is_valid(), False)

        # valid form
        form = CountryForm({'name': 'test2', 'color': 1})
        self.assertEqual(form.is_valid(), True)

        # invalid form, name cannot start with _
        form = CountryForm({'name': '_test', 'color': 1})
        self.assertEqual('name' in form.errors, True)


    def test_creation(self):
        # anonymous access to the form should redirect to login
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 302) # redirect

        # log user in
        self.client.login(username='tester', password='pass')

        # access the form
        response = self.client.get("/new/")
        self.assertEqual(response.status_code, 200) # ok

        # submit an empty form
        response = self.client.post("/new/", {})
        self.assertEqual(response.status_code, 200) # ok, no redirect

        # submit a form
        response = self.client.post("/new/", {'name': 'test2',
                                              'color': '1'})
        self.assertEqual(response.status_code, 302) # redirect on success

        # count if the new object was created
        self.assertEqual(Country.objects.count(), 2) # we have 2 objects


    def test_listing(self):
        # access objects list
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200) # Ok
        self.assertEqual(len(response.context['object_list']), 1) # 1 object
        
        # create a new object and test if we have 2
        Country.objects.create(name='test2', user=self.user)
        response = self.client.get("/")
        self.assertEqual(len(response.context['object_list']), 2)


    def test_display(self):
        # check if we can access the object inside the response
        response = self.client.get("/1/")
        self.assertEqual(response.context['object'].name, 'test')
        
        # access undefined object
        response = self.client.get("/404/")
        self.assertEqual(response.status_code, 404) # not found


    def test_delete(self):
        # log user in
        self.client.login(username='tester', password='pass')

        self.assertEqual(Country.objects.count(), 1)

        # delete object
        response = self.client.get("/1/delete/")

        self.assertEqual(Country.objects.count(), 0)


    def test_edition(self):
        # log user in
        self.client.login(username='tester', password='pass')

        # get the first object and check its name
        country = Country.objects.get(pk=1)
        self.assertEqual(country.name, 'test')

        # change the country name through the form
        response = self.client.post("/1/edit/", {'name': 'changed',
                                              'color': '1'})
        self.assertEqual(response.status_code, 302) # redirect on success

        # get the first object after the name change
        country = Country.objects.get(pk=1)
        self.assertEqual(country.name, 'changed')
        
        # edit an undefined object
        response = self.client.get("/404/edit/")
        self.assertEqual(response.status_code, 404) # not found



if __name__ == '__main__':
    unittest.main()
