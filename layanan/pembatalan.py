
import datetime

from config import REFUND_PENUH_MIN_HARI
from layanan.event import cari_event


def batalkan_pesanan(data, kode, tanggal):
    pesanan = next(
        (p for p in data["pesanan"] if p["kode"] == kode),
        None
    )

    if pesanan is None:
        return None, {"error": "Pesanan tidak ditemukan"}, 404

    if pesanan["status"] != "lunas":
        return None, {"error": "Pesanan sudah dibatalkan"}, 400

    event = cari_event(data, pesanan["event"])

    sisa_hari = (
        datetime.date.fromisoformat(event["tanggal"])
        - datetime.date.fromisoformat(tanggal)
    ).days

    if sisa_hari < 1:
        return None, {
            "error": "Pembatalan ditutup pada hari H"
        }, 400

    bisa_refund = pesanan["total"] - pesanan["biaya_layanan"]

    if sisa_hari >= REFUND_PENUH_MIN_HARI:
        refund = bisa_refund
    else:
        refund = bisa_refund * 50 // 100

    pesanan["status"] = "batal"
    pesanan["refund"] = refund

    return pesanan, None, 200
