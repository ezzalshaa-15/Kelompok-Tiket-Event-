
import unittest
from unittest.mock import patch

from layanan.event import cari_event
from layanan.pemesanan import buat_pesanan_web
from layanan.pembatalan import batalkan_pesanan


class TestIntegrasi(unittest.TestCase):

    def setUp(self):
        self.data = {
            "event": [
                {
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
            ],
            "promo": [],
            "pesanan": []
        }

    def test_integrasi_pemesanan_berhasil(self):
        event = cari_event(self.data, "EV001")

        pesanan, error = buat_pesanan_web(
            self.data,
            event,
            "Reguler",
            2,
            "Alesha",
            "alesha@gmail.com",
            "",
            "2026-11-07"
        )

        self.assertIsNone(error)
        self.assertIsNotNone(pesanan)
        self.assertEqual(len(self.data["pesanan"]), 1)

    def test_integrasi_event_tidak_ditemukan(self):
        event = cari_event(self.data, "EV999")

        self.assertIsNone(event)

    def test_integrasi_pemesanan_dan_pembatalan(self):
        event = cari_event(self.data, "EV001")

        pesanan, error = buat_pesanan_web(
            self.data,
            event,
            "Reguler",
            2,
            "Alesha",
            "alesha@gmail.com",
            "",
            "2026-11-07"
        )

        self.assertIsNone(error)

        hasil, error ,status = batalkan_pesanan(
            self.data,
            pesanan["kode"],
            "2026-11-07"
        )

        self.assertIsNone(error)
        self.assertEqual(hasil["status"], "batal")


if __name__ == "__main__":
    unittest.main()
