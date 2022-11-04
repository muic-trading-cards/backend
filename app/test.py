import unittest

from app import main


class TestPost(unittest.TestCase):
    def test_post(self):

        self.test_app = main.test_client()

        response = self.test_app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()