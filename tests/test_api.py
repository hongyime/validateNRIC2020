import unittest

from app import app


class ValidationApiTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def assert_bad_request(self, response):
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.is_json)
        self.assertIs(response.json['valid'], False)
        self.assertIsNone(response.json['barcode'])
        self.assertIsInstance(response.json['message'], str)

    def test_rejects_non_object_json_without_server_error(self):
        for payload in [[], ['not an object'], 'text', 42, True]:
            with self.subTest(payload_type=type(payload).__name__):
                self.assert_bad_request(self.client.post('/validate', json=payload))

    def test_rejects_non_string_identifier_without_server_error(self):
        for value in [None, 123456789, [], {}, False]:
            with self.subTest(value_type=type(value).__name__):
                self.assert_bad_request(self.client.post('/validate', json={'nric': value}))

    def test_invalid_json_and_missing_body_return_json_error(self):
        self.assert_bad_request(self.client.post('/validate', data='{', content_type='application/json'))
        self.assert_bad_request(self.client.post('/validate'))
        self.assert_bad_request(self.client.post('/validate', data='null', content_type='application/json'))

    def test_invalid_string_keeps_validation_response(self):
        response = self.client.post('/validate', json={'nric': 'not-an-id'})
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.json['valid'], False)
        self.assertIsNone(response.json['barcode'])

    def test_empty_identifier_keeps_validation_response(self):
        for payload in [{}, {'nric': ''}]:
            with self.subTest(payload=payload):
                response = self.client.post('/validate', json=payload)
                self.assertEqual(response.status_code, 200)
                self.assertIs(response.json['valid'], False)
                self.assertIsNone(response.json['barcode'])

    def test_synthetic_valid_identifier_still_generates_barcode(self):
        response = self.client.post('/validate', json={'nric': 's0000000j'})
        self.assertEqual(response.status_code, 200)
        self.assertIs(response.json['valid'], True)
        self.assertTrue(response.json['barcode'].startswith('data:image/png;base64,'))


if __name__ == '__main__':
    unittest.main()
