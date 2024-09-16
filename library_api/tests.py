from django.test import TestCase
from time import time

class APITests(TestCase):
    def test_recommended_books_response_time(self):
        # Simulate a user with favorite books
        start = time()
        response = self.client.get('/api/recommended_books/')
        end = time()
        response_time = end - start
        self.assertLess(response_time, 1, "Response took too long")
