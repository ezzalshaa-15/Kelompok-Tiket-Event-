import unittest

from auth.validators import (
    validate_username,
    validate_email,
    validate_password
)


class TestValidators(unittest.TestCase):

    def test_validate_username(self):
        self.assertTrue(validate_username("uwais_alqarni"))
        self.assertFalse(validate_username("ab"))
        self.assertFalse(validate_username("a" * 21))
        self.assertFalse(validate_username(123))

    def test_validate_email(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertFalse(validate_email("invalid-email"))
        self.assertFalse(validate_email("test@"))
        self.assertFalse(validate_email(123))

    def test_validate_password(self):
        self.assertTrue(validate_password("123456"))
        self.assertFalse(validate_password("12345"))
        self.assertFalse(validate_password(""))
        self.assertFalse(validate_password(123))


if __name__ == "__main__":
    unittest.main()