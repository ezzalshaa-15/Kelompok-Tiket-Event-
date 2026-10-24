
def cari_promo(data, kode):
    return next(
        (
            promo for promo in data["promo"]
            if promo["kode"] == kode.upper()
        ),
        None
    )


def validasi_promo(data, kode, tanggal):
    promo = cari_promo(data, kode)

    if promo is None:
        return {
            "kode": kode.upper(),
            "valid": False,
            "alasan": "Kode tidak dikenal"
        }

    if promo["terpakai"] >= promo["kuota"]:
        return {
            "kode": promo["kode"],
            "valid": False,
            "alasan": "Kuota promo habis"
        }

    if tanggal > promo["berlaku_sampai"]:
        return {
            "kode": promo["kode"],
            "valid": False,
            "alasan": "Promo sudah berakhir"
        }

    return {
        "kode": promo["kode"],
        "valid": True,
        "persen": promo["persen"],
        "maks": promo["maks"]
    }
