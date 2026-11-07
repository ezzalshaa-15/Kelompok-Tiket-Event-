import unittest
import os

from unittest.mock import patch

from auth.logic_login_register import (
    register_user,
    login_user
)


TEST_DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "test_users_db.json"
)


class TestAuthLogic(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    @patch(
        "auth.logic_login_register.DB_PATH",
        TEST_DB_PATH
    )
    def test_register_success(self):
        success, msg = register_user(
            "alice",
            "alice@example.com",
            "123456"
        )

        self.assertTrue(success)
        self.assertEqual(msg, "Registrasi berhasil")

    @patch(
        "auth.logic_login_register.DB_PATH",
        TEST_DB_PATH
    )
    def test_register_duplicate_username(self):
        register_user("bob", "bob@example.com", "123456")

        success, msg = register_user(
            "bob",
            "another@example.com",
            "123456"
        )

        self.assertFalse(success)
        self.assertEqual(msg, "Username sudah terdaftar")

    @patch(
        "auth.logic_login_register.DB_PATH",
        TEST_DB_PATH
    )
    def test_register_duplicate_email(self):
        register_user("charlie", "same@example.com", "123456")

        success, msg = register_user(
            "dave",
            "same@example.com",
            "123456"
        )

        self.assertFalse(success)
        self.assertEqual(msg, "Email sudah digunakan")

    @patch(
        "auth.logic_login_register.DB_PATH",
        TEST_DB_PATH
    )
    def test_login_success(self):
        register_user("eve", "eve@example.com", "123456")

        success, msg = login_user("eve", "123456")

        self.assertTrue(success)
        self.assertEqual(msg, "Login berhasil")

    @patch(
        "auth.logic_login_register.DB_PATH",
        TEST_DB_PATH
    )
    def test_login_wrong_password(self):
        register_user("frank", "frank@example.com", "123456")

        success, msg = login_user("frank", "wrongpass")

        self.assertFalse(success)
        self.assertEqual(msg, "Password salah")

    @patch(
        "auth.logic_login_register.DB_PATH",
        TEST_DB_PATH
    )
    def test_login_user_not_found(self):
        success, msg = login_user(
            "nonexistent",
            "123456"
        )

        self.assertFalse(success)
        self.assertEqual(
            msg,
            "Username atau email tidak ditemukan"
        )


if __name__ == "__main__":
    unittest.main()