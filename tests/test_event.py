
import unittest

from layanan.event import (
    cari_event,
    hitung_sisa_kuota,
    daftar_event_dengan_sisa,
    hitung_terjual
)


class TestEvent(unittest.TestCase):

    def setUp(self):
        self.data = {
            "event": [
                {
                    "id": 1,
                    "nama": "Seminar Teknologi",
                    "kategori": {
                        "Reguler": {
                            "kuota": 100,
                            "harga": 50000
                        }
                    }
                }
            ],
            "pesanan": [
                {
                    "event": 1,
                    "kategori": "Reguler",
                    "jumlah": 20,
                    "status": "lunas"
                },
                {
                    "event": 1,
                    "kategori": "Reguler",
                    "jumlah": 10,
                    "status": "batal"
                }
            ]
        }

    def test_cari_event_berhasil(self):
        hasil = cari_event(self.data, 1)
        self.assertIsNotNone(hasil)
        self.assertEqual(hasil["nama"], "Seminar Teknologi")

    def test_cari_event_tidak_ditemukan(self):
        hasil = cari_event(self.data, 99)
        self.assertIsNone(hasil)

    def test_hitung_sisa_kuota(self):
        event = self.data["event"][0]
        hasil = hitung_sisa_kuota(
            self.data, event, "Reguler"
        )
        self.assertEqual(hasil, 80)

    def test_daftar_event_dengan_sisa(self):
        hasil = daftar_event_dengan_sisa(self.data)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["sisa_kuota"], 80)

    def test_hitung_terjual(self):
        hasil = hitung_terjual(
            self.data, 1, "Reguler"
        )
        self.assertEqual(hasil, 20)


if __name__ == "__main__":
    unittest.main()
