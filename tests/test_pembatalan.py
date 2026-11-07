
import unittest

from layanan.pembatalan import batalkan_pesanan


class TestPembatalan(unittest.TestCase):

    def setUp(self):
        self.data = {
            "event": [
                {
                    "id": "EV001",
                    "nama": "Seminar Teknologi",
                    "tanggal": "2026-12-20"
                }
            ],
            "pesanan": [
                {
                    "kode": "TIX-EV001-0001",
                    "event": "EV001",
                    "kategori": "Reguler",
                    "jumlah": 2,
                    "total": 110000,
                    "biaya_layanan": 10000,
                    "status": "lunas",
                    "refund": 0
                }
            ]
        }

    def test_pembatalan_berhasil_refund_penuh(self):
        pesanan, error, status = batalkan_pesanan(
            self.data,
            "TIX-EV001-0001",
            "2026-11-07"
        )

        self.assertIsNone(error)
        self.assertEqual(status, 200)
        self.assertEqual(pesanan["status"], "batal")
        self.assertEqual(pesanan["refund"], 100000)

    def test_pembatalan_refund_setengah(self):
        pesanan, error, status = batalkan_pesanan(
            self.data,
            "TIX-EV001-0001",
            "2026-12-15"
        )

        self.assertIsNone(error)
        self.assertEqual(status, 200)
        self.assertEqual(pesanan["refund"], 50000)

    def test_pesanan_tidak_ditemukan(self):
        pesanan, error, status = batalkan_pesanan(
            self.data,
            "KODE-SALAH",
            "2026-11-07"
        )

        self.assertIsNone(pesanan)
        self.assertEqual(status, 404)

    def test_pesanan_sudah_dibatalkan(self):
        self.data["pesanan"][0]["status"] = "batal"

        pesanan, error, status = batalkan_pesanan(
            self.data,
            "TIX-EV001-0001",
            "2026-11-07"
        )

        self.assertIsNone(pesanan)
        self.assertEqual(status, 400)

    def test_pembatalan_pada_hari_h(self):
        pesanan, error, status = batalkan_pesanan(
            self.data,
            "TIX-EV001-0001",
            "2026-12-20"
        )

        self.assertIsNone(pesanan)
        self.assertEqual(status, 400)


if __name__ == "__main__":
    unittest.main()
