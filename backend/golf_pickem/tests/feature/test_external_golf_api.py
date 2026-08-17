import requests
from django.test import TestCase

from golf_pickem.external_golf_api import (
    get_schedule,
)

class TestExternalGolfApi(TestCase):
    """Tests for the external golf api methods.
    """
    
    def test_get_schedule(self):
        """Test the get_schedule method to make sure the data is returned correctly.
        """
        # commented to reduce test runtime
        # uncomment below if you want to make sure the api request is working
        
        # response = get_schedule(2026)
        # self.assertEqual(response.status_code, 200)