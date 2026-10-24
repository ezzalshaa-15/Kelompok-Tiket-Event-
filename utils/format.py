
import datetime


def format_rupiah(nilai):
    return "{:,}".format(nilai).replace(",", ".")


def format_tanggal_indonesia(tanggal):
    tgl = datetime.date.fromisoformat(tanggal)

    bulan = [
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
        "Jul", "Agu", "Sep", "Okt", "Nov", "Des",
    ]

    return f"{tgl.day} {bulan[tgl.month - 1]} {tgl.year}"
