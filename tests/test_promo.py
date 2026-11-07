
import unittest

from layanan.promo import (
    cari_promo,
    validasi_promo
)


class TestPromo(unittest.TestCase):

    def setUp(self):
        self.data = {
            "promo": [
                {
                    "kode": "HEMAT10",
                    "terpakai": 2,
                    "kuota": 10,
                    "berlaku_sampai": "2026-12-31",
                    "persen": 10,
                    "maks": 20000
                }
            ]
        }

    def test_cari_promo_berhasil(self):
        hasil = cari_promo(self.data, "HEMAT10")

        self.assertIsNotNone(hasil)
        self.assertEqual(hasil["kode"], "HEMAT10")

    def test_cari_promo_tidak_ditemukan(self):
        hasil = cari_promo(self.data, "SALAH")

        self.assertIsNone(hasil)

    def test_validasi_promo_berhasil(self):
        hasil = validasi_promo(
            self.data, "HEMAT10", "2026-11-07"
        )

        self.assertTrue(hasil["valid"])
        self.assertEqual(hasil["persen"], 10)

    def test_validasi_promo_tidak_dikenal(self):
        hasil = validasi_promo(
            self.data, "SALAH", "2026-11-07"
        )

        self.assertFalse(hasil["valid"])
        self.assertEqual(
            hasil["alasan"], "Kode tidak dikenal"
        )

    def test_validasi_promo_kuota_habis(self):
        self.data["promo"][0]["terpakai"] = 10

        hasil = validasi_promo(
            self.data, "HEMAT10", "2026-11-07"
        )

        self.assertFalse(hasil["valid"])
        self.assertEqual(
            hasil["alasan"], "Kuota promo habis"
        )

    def test_validasi_promo_kedaluwarsa(self):
        hasil = validasi_promo(
            self.data, "HEMAT10", "2027-01-01"
        )

        self.assertFalse(hasil["valid"])
        self.assertEqual(
            hasil["alasan"], "Promo sudah berakhir"
        )


if __name__ == "__main__":
    unittest.main()
