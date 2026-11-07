
import unittest

from layanan.pemesanan import (
    validasi_identitas,
    hitung_harga,
    buat_pesanan_web,
    buat_pesanan_api
)


class TestPemesanan(unittest.TestCase):

    def setUp(self):
        self.event = {
            "id": "EV001",
            "nama": "Seminar Teknologi",
            "tanggal": "2026-12-20",
            "kategori": {
                "Reguler": {
                    "kuota": 100,
                    "harga": 50000
                }
            }
        }

        self.data = {
            "event": [self.event],
            "pesanan": [],
            "promo": [
                {
                    "kode": "HEMAT10",
                    "terpakai": 0,
                    "kuota": 10,
                    "berlaku_sampai": "2026-12-31",
                    "persen": 10,
                    "maks": 20000
                }
            ]
        }

    def test_validasi_identitas_berhasil(self):
        hasil = validasi_identitas(
            "Andi", "andi@gmail.com"
        )
        self.assertTrue(hasil)

    def test_validasi_identitas_gagal(self):
        hasil = validasi_identitas(
            "", "email_salah"
        )
        self.assertFalse(hasil)

    def test_hitung_harga_tanpa_promo(self):
        hasil = hitung_harga(
            self.event,
            "Reguler",
            2,
            "2026-11-07"
        )

        self.assertEqual(hasil["harga_dasar"], 100000)
        self.assertEqual(hasil["diskon_early"], 15000)
        self.assertEqual(hasil["diskon_promo"], 0)
        self.assertEqual(hasil["biaya_layanan"], 10000)
        self.assertEqual(hasil["total"], 95000)

    def test_hitung_harga_dengan_promo(self):
        promo = self.data["promo"][0]

        hasil = hitung_harga(
            self.event,
            "Reguler",
            2,
            "2026-11-07",
            promo
        )

        self.assertEqual(hasil["diskon_promo"], 8500)
        self.assertEqual(hasil["total"], 86500)

    def test_buat_pesanan_web_berhasil(self):
        pesanan, error = buat_pesanan_web(
            self.data,
            self.event,
            "Reguler",
            2,
            "Andi",
            "andi@gmail.com",
            "",
            "2026-11-07"
        )

        self.assertIsNone(error)
        self.assertIsNotNone(pesanan)
        self.assertEqual(pesanan["jumlah"], 2)
        self.assertEqual(pesanan["status"], "lunas")
        self.assertEqual(len(self.data["pesanan"]), 1)

    def test_buat_pesanan_web_gagal_email(self):
        pesanan, error = buat_pesanan_web(
            self.data,
            self.event,
            "Reguler",
            2,
            "",
            "email_salah",
            "",
            "2026-11-07"
        )

        self.assertIsNone(pesanan)
        self.assertIsNotNone(error)

    def test_buat_pesanan_api_berhasil(self):
        body = {
            "nama": "Budi",
            "email": "budi@gmail.com",
            "jumlah": 2,
            "kategori": "Reguler"
        }

        pesanan, error, status = buat_pesanan_api(
            self.data,
            self.event,
            body,
            "2026-11-07"
        )

        self.assertIsNone(error)
        self.assertEqual(status, 201)
        self.assertEqual(pesanan["jumlah"], 2)
        self.assertEqual(pesanan["status"], "lunas")

    def test_buat_pesanan_api_event_tidak_ditemukan(self):
        body = {}

        pesanan, error, status = buat_pesanan_api(
            self.data,
            None,
            body,
            "2026-11-07"
        )

        self.assertIsNone(pesanan)
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
