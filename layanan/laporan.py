
from layanan.event import hitung_terjual


def laporan_event(data, event):
    per_kategori = {}
    pendapatan = 0
    batal = 0
    total_kuota = 0
    total_terjual = 0

    for nama_kat, kategori in event["kategori"].items():
        terjual = hitung_terjual(data, event["id"], nama_kat)

        per_kategori[nama_kat] = {
            "terjual": terjual,
            "sisa": kategori["kuota"] - terjual,
        }

        total_kuota += kategori["kuota"]
        total_terjual += terjual

    for pesanan in data["pesanan"]:
        if pesanan["event"] == event["id"]:
            if pesanan["status"] == "lunas":
                pendapatan += pesanan["total"]
            else:
                batal += 1
                pendapatan += pesanan["total"] - pesanan["refund"]

    okupansi = (
        round(total_terjual / total_kuota * 100, 1)
        if total_kuota else 0
    )

    return {
        "event": event["id"],
        "per_kategori": per_kategori,
        "pendapatan": pendapatan,
        "pesanan_batal": batal,
        "okupansi_persen": okupansi,
    }
