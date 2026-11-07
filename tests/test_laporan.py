
import unittest

from layanan.laporan import laporan_event


class TestLaporan(unittest.TestCase):

    def setUp(self):
        self.event = {
            "id": "EV001",
            "nama": "Seminar Teknologi",
            "kategori": {
                "Reguler": {
                    "kuota": 100,
                    "harga": 50000
                },
                "VIP": {
                    "kuota": 50,
                    "harga": 100000
                }
            }
        }

        self.data = {
            "event": [self.event],
            "pesanan": [
                {
                    "event": "EV001",
                    "kategori": "Reguler",
                    "jumlah": 20,
                    "total": 1000000,
                    "refund": 0,
                    "status": "lunas"
                },
                {
                    "event": "EV001",
                    "kategori": "VIP",
                    "jumlah": 5,
                    "total": 500000,
                    "refund": 250000,
                    "status": "batal"
                }
            ]
        }

    def test_laporan_event_berhasil(self):
        hasil = laporan_event(self.data, self.event)

        self.assertEqual(hasil["event"], "EV001")
        self.assertEqual(hasil["pesanan_batal"], 1)

    def test_laporan_per_kategori(self):
        hasil = laporan_event(self.data, self.event)

        self.assertEqual(
            hasil["per_kategori"]["Reguler"]["terjual"], 20
        )

        self.assertEqual(
            hasil["per_kategori"]["Reguler"]["sisa"], 80
        )

        self.assertEqual(
            hasil["per_kategori"]["VIP"]["terjual"], 0
        )

    def test_laporan_pendapatan(self):
        hasil = laporan_event(self.data, self.event)

        self.assertEqual(
            hasil["pendapatan"], 1250000
        )

    def test_laporan_okupansi(self):
        hasil = laporan_event(self.data, self.event)

        self.assertEqual(
            hasil["okupansi_persen"], 13.3
        )


if __name__ == "__main__":
    unittest.main()
