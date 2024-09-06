import unittest
from test_leaflet import get_city_coordinates_from_name
from unittest.mock import patch, MagicMock

class GeoTest(unittest.TestCase):

    @patch('test_leaflet.Nominatim.geocode')
    def test_get_coordinates_valid_city(self,mock_geocode):
        # Mock the return value for a valid city
        mock_location = MagicMock()
        mock_location.latitude = 48.8566
        mock_location.longitude = 2.3522
        mock_geocode.return_value = mock_location

        result = get_city_coordinates_from_name("Paris")

        self.assertEqual(result,(48.8556,2.3522))


    @patch('test_leaflet.Nominatim.geocode')
    def test_get_coordinates_invalid_city(self,mock_geocode):
        mock_geocode.return_value = None

        # Call the function with an invalid city name
        result = get_city_coordinates_from_name("InvalidCity")

        # Assert the result is None
        self.assertIsNone(result)


    @patch('test_leaflet.Nominatim.geocode')
    def test_get_coordinates_no_city(self,mock_geocode):
        mock_geocode.return_value = None

        result = get_city_coordinates_from_name("")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
