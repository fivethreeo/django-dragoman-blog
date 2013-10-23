from django.test import testcases

class FixtureTestCase(testcases.TestCase):
    def setUp(self):
        if callable(getattr(self, 'create_fixtures', None)):
            self.create_fixtures()