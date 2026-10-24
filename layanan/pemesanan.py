
import datetime
import re

from config import (
    EARLY_BIRD_HARI,
    EARLY_BIRD_PERSEN,
    BIAYA_LAYANAN_PER_TIKET,
    BATAS_TIKET_PER_PESANAN,
)
from layanan.event import hitung_terjual
from layanan.promo import cari_promo


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validasi_identitas(nama, email):
    return bool(nama.strip()) and bool(EMAIL_RE.match(email.strip()))


def hitung_harga(event, kategori, jumlah, tanggal, promo=None):
    dasar = event["kategori"][kategori]["harga"] * jumlah

    tanggal_event = datetime.date.fromisoformat(event["tanggal"])
    tanggal_pesan = datetime.date.fromisoformat(tanggal)

    if (tanggal_event - tanggal_pesan).days >= EARLY_BIRD_HARI:
        early = dasar * EARLY_BIRD_PERSEN // 100
    else:
        early = 0

    diskon_promo = 0

    if promo:
        diskon_promo = min(
            (dasar - early) * promo["persen"] // 100,
            promo["maks"]
        )

    layanan = BIAYA_LAYANAN_PER_TIKET * jumlah
    total = dasar - early - diskon_promo + layanan

    return {
        "harga_dasar": dasar,
        "diskon_early": early,
        "diskon_promo": diskon_promo,
        "biaya_layanan": layanan,
        "total": total,
    }


def buat_pesanan_web(
    data, event, kategori, jumlah,
    nama, email, kode_promo, tanggal
):
    if not validasi_identitas(nama, email):
        return None, "Nama dan email yang valid wajib diisi"

    if jumlah < 1 or jumlah > BATAS_TIKET_PER_PESANAN:
        return None, "Jumlah tiket 1–5 per pesanan"

    if kategori not in event["kategori"]:
        return None, "Kategori tidak tersedia"

    terjual = hitung_terjual(data, event["id"], kategori)
    kuota = event["kategori"][kategori]["kuota"]

    if terjual + jumlah > kuota:
        return None, "Kuota tidak mencukupi"

    promo = None

    if kode_promo:
        calon_promo = cari_promo(data, kode_promo)

        if (
            calon_promo
            and calon_promo["terpakai"] < calon_promo["kuota"]
            and tanggal <= calon_promo["berlaku_sampai"]
        ):
            promo = calon_promo

    rincian = hitung_harga(
        event, kategori, jumlah, tanggal, promo
    )

    if promo and rincian["diskon_promo"] > 0:
        promo["terpakai"] += 1

    kode = (
        f"TIX-{event['id']}-"
        f"{str(len(data['pesanan']) + 1).zfill(4)}"
    )

    pesanan = {
        "kode": kode,
        "event": event["id"],
        "kategori": kategori,
        "jumlah": jumlah,
        "nama": nama.strip(),
        "email": email.strip(),
        "tanggal_pesan": tanggal,
        **rincian,
        "kode_promo": (
            kode_promo if rincian["diskon_promo"] > 0 else ""
        ),
        "status": "lunas",
        "refund": 0,
    }

    data["pesanan"].append(pesanan)
    return pesanan, None


def buat_pesanan_api(data, event, body, tanggal_default):
    if event is None:
        return None, {"error": "Event tidak ditemukan"}, 404

    nama = str(body.get("nama", "")).strip()
    email = str(body.get("email", "")).strip()

    if not validasi_identitas(nama, email):
        return None, {
            "error": "Nama dan email yang valid wajib diisi"
        }, 400

    jumlah = body.get("jumlah")

    if (
        not isinstance(jumlah, int)
        or isinstance(jumlah, bool)
        or jumlah < 1
        or jumlah > BATAS_TIKET_PER_PESANAN
    ):
        return None, {
            "error": "Jumlah tiket 1–5 per pesanan"
        }, 400

    kategori = body.get("kategori")

    if kategori not in event["kategori"]:
        return None, {
            "error": "Kategori tidak tersedia"
        }, 400

    kuota = event["kategori"][kategori]["kuota"]
    terjual = hitung_terjual(data, event["id"], kategori)
    sisa = kuota - terjual

    if sisa < jumlah:
        return None, {
            "error": "Kuota tidak mencukupi",
            "sisa": sisa,
        }, 409

    tanggal = body.get("tanggal") or tanggal_default
    tanggal_obj = datetime.date.fromisoformat(tanggal)
    tanggal_iso = tanggal_obj.isoformat()

    kode_promo = str(body.get("promo", "")).upper()
    promo = None

    if kode_promo:
        promo = cari_promo(data, kode_promo)

        if (
            promo is None
            or promo["terpakai"] >= promo["kuota"]
            or tanggal_iso > promo["berlaku_sampai"]
        ):
            return None, {
                "error": "Kode promo tidak berlaku"
            }, 400

    rincian = hitung_harga(
        event, kategori, jumlah, tanggal_iso, promo
    )

    if promo:
        promo["terpakai"] += 1

    kode = (
        f"TIX-{event['id']}-"
        f"{str(len(data['pesanan']) + 1).zfill(4)}"
    )

    pesanan = {
        "kode": kode,
        "event": event["id"],
        "kategori": kategori,
        "jumlah": jumlah,
        "nama": nama,
        "email": email,
        "tanggal_pesan": tanggal_iso,
        **rincian,
        "kode_promo": kode_promo,
        "status": "lunas",
        "refund": 0,
    }

    data["pesanan"].append(pesanan)
    return pesanan, None, 201
