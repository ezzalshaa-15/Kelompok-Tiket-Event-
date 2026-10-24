
import datetime

from flask import Blueprint, request, jsonify

from repositori.json_repo import baca_data, simpan_data
from layanan.event import daftar_event_dengan_sisa, cari_event
from layanan.promo import validasi_promo
from layanan.pemesanan import buat_pesanan_api
from layanan.pembatalan import batalkan_pesanan
from layanan.laporan import laporan_event

api = Blueprint("api", __name__)


@api.route("/api/event")
def api_event():
    data = baca_data()
    daftar = daftar_event_dengan_sisa(data)

    hasil = [
        {
            "id": event["id"],
            "nama": event["nama"],
            "tanggal": event["tanggal"],
            "lokasi": event["lokasi"],
            "sisa_kuota": event["sisa_kuota"],
        }
        for event in daftar
    ]

    return jsonify(hasil)


@api.route("/api/promo/<kode>")
def api_promo(kode):
    data = baca_data()
    tanggal = (
        request.args.get("tanggal")
        or datetime.date.today().isoformat()
    )

    return jsonify(validasi_promo(data, kode, tanggal))


@api.route("/api/pesan", methods=["POST"])
def api_pesan():
    data = baca_data()
    body = request.get_json(silent=True) or {}
    event = cari_event(data, body.get("event"))

    pesanan, error, status = buat_pesanan_api(
        data,
        event,
        body,
        datetime.date.today().isoformat(),
    )

    if error:
        return jsonify(error), status

    simpan_data(data)
    return jsonify(pesanan), status


@api.route("/api/batal", methods=["POST"])
def api_batal():
    data = baca_data()
    body = request.get_json(silent=True) or {}
    tanggal = (
        body.get("tanggal")
        or datetime.date.today().isoformat()
    )

    pesanan, error, status = batalkan_pesanan(
        data,
        body.get("kode"),
        tanggal,
    )

    if error:
        return jsonify(error), status

    simpan_data(data)

    return jsonify({
        "kode": pesanan["kode"],
        "status": "batal",
        "refund": pesanan["refund"],
    })


@api.route("/api/laporan/<id_event>")
def api_laporan(id_event):
    data = baca_data()
    event = cari_event(data, id_event)

    if event is None:
        return jsonify({
            "error": "Event tidak ditemukan"
        }), 404

    return jsonify(laporan_event(data, event))
