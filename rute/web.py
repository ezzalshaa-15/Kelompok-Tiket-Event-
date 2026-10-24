
import datetime

from flask import Blueprint, request, render_template_string

from repositori.json_repo import baca_data, simpan_data
from layanan.event import (
    cari_event,
    hitung_sisa_kuota,
)
from layanan.pemesanan import buat_pesanan_web
from utils.format import format_rupiah, format_tanggal_indonesia

web = Blueprint("web", __name__)


@web.route("/")
def index():
    data = baca_data()
    kartu = ""

    for event in data["event"]:
        info = ""

        for nama_kat, kategori in event["kategori"].items():
            sisa = hitung_sisa_kuota(data, event, nama_kat)

            status = (
                "<b style='color:red'>HABIS</b>"
                if sisa <= 0
                else "sisa " + str(sisa)
            )

            info += (
                "<li>" + nama_kat
                + ": Rp " + format_rupiah(kategori["harga"])
                + " — " + status + "</li>"
            )

        kartu += (
            "<div style='border:1px solid #ccc;"
            "border-radius:10px;padding:14px;margin:12px 0'>"
            "<h2><a href='/event/" + event["id"] + "'>"
            + event["nama"] + "</a></h2>"
        )

        kartu += (
            "<p>" + format_tanggal_indonesia(event["tanggal"])
            + " · " + event["lokasi"] + "</p>"
            + "<ul>" + info + "</ul></div>"
        )

    return (
        "<html><head><title>Tiket Event</title></head>"
        "<body style='font-family:Arial;margin:30px;max-width:760px'>"
        "<h1>🎫 Event Kampus</h1>"
        + kartu
        + "<p><a href='/cek'>Cek pesanan</a></p>"
        "</body></html>"
    )


@web.route("/event/<id_event>", methods=["GET", "POST"])
def detail(id_event):
    data = baca_data()
    event = cari_event(data, id_event)

    if event is None:
        return "Event tidak ditemukan", 404

    pesan = ""

    if request.method == "POST":
        kategori = request.form.get("kategori", "")
        nama = request.form.get("nama", "").strip()
        email = request.form.get("email", "").strip()
        kode_promo = request.form.get("promo", "").strip().upper()

        try:
            jumlah = int(request.form.get("jumlah", "0"))
        except ValueError:
            jumlah = 0

        pesanan, error = buat_pesanan_web(
            data,
            event,
            kategori,
            jumlah,
            nama,
            email,
            kode_promo,
            datetime.date.today().isoformat(),
        )

        if error:
            pesan = error
        else:
            simpan_data(data)
            pesan = (
                "Pesanan " + pesanan["kode"]
                + " berhasil. Total bayar Rp "
                + format_rupiah(pesanan["total"])
            )

    pilihan = "".join(
        "<option>" + nama + "</option>"
        for nama in event["kategori"]
    )

    return render_template_string(
        """<html><body style='font-family:Arial;margin:30px'>
        <a href='/'>← semua event</a>
        <h1>{{ e.nama }}</h1>
        <p>{{ e.tanggal }} · {{ e.lokasi }}</p>
        <p><b>{{ pesan }}</b></p>
        <form method='post'>
        Kategori <select name='kategori'>"""
        + pilihan
        + """</select><br>
        Jumlah <input name='jumlah' type='number' value='1'><br>
        Nama <input name='nama'><br>
        Email <input name='email'><br>
        Kode promo <input name='promo'><br>
        <button>Pesan</button></form></body></html>""",
        e=event,
        pesan=pesan,
    )


@web.route("/cek")
def cek():
    data = baca_data()
    kode = request.args.get("kode", "").strip().upper()

    hasil = next(
        (p for p in data["pesanan"] if p["kode"] == kode),
        None,
    )

    return render_template_string(
        """<html><body style='font-family:Arial;margin:30px'>
        <a href='/'>← semua event</a><h1>Cek Pesanan</h1>
        <form><input name='kode' value='{{ kode }}'
        placeholder='TIX-...'><button>Cek</button></form>
        {% if p %}
        <p>{{ p.kode }} · {{ p.event }} {{ p.kategori }} ×
        {{ p.jumlah }} · status <b>{{ p.status }}</b> · total
        {{ p.total }}</p>
        {% elif kode %}<p>Tidak ditemukan</p>{% endif %}
        </body></html>""",
        p=hasil,
        kode=kode,
    )
