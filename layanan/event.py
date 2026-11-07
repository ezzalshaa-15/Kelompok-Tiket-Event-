
def cari_event(data, id_event):
    """Mencari event berdasarkan ID."""
    for event in data.get("event", []):
        if str(event.get("id")) == str(id_event):
            return event
    return None


def hitung_terjual(data, event_id, kategori):
    """Menghitung tiket yang sudah lunas."""
    return sum(
        int(pesanan.get("jumlah", 0))
        for pesanan in data.get("pesanan", [])
        if str(pesanan.get("event")) == str(event_id)
        and pesanan.get("kategori") == kategori
        and pesanan.get("status") == "lunas"
    )


def hitung_sisa_kuota(data, event, nama_kategori):
    """Menghitung sisa kuota tiket."""
    kategori = event.get("kategori", {}).get(nama_kategori, {})
    kuota = int(kategori.get("kuota", 0))

    terjual = hitung_terjual(
        data, event.get("id"), nama_kategori
    )

    return max(0, kuota - terjual)


def daftar_event_dengan_sisa(data):
    """Menampilkan daftar event beserta sisa kuota."""
    daftar = []

    for event_asli in data.get("event", []):
        event = event_asli.copy()

        event["sisa_kuota"] = sum(
            hitung_sisa_kuota(data, event, nama_kategori)
            for nama_kategori in event.get("kategori", {})
        )

        daftar.append(event)

    return daftar
