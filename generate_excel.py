import pandas as pd
import os

# Pastikan folder static ada
folder_path = os.path.join('static', 'lkps_app', 'excel_templates')
os.makedirs(folder_path, exist_ok=True)

# SKEMA LENGKAP SEMUA TABEL (KRITERIA 1-6)
master_schema = {
    # Kriteria 1: Tata Pamong & Penjaminan Mutu
    'Tabel_1A1': {'cols': ['unit_kerja', 'nama_ketua', 'periode_jabatan', 'pendidikan_terakhir', 'jabatan_fungsional', 'tupoksi'], 'data': ['Fakultas Teknologi', 'Dr. Budi Santoso', '2022-2026', 'S3', 'Lektor Kepala', 'Memimpin UPPS']},
    'Tabel_1A2_Sumber': {'cols': ['sumber_dana', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Mahasiswa', 1000, 1200, 1500, 'http://link-dana.com']},
    'Tabel_1A3_Penggunaan': {'cols': ['jenis_penggunaan', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Penelitian', 200, 250, 300, 'http://link-guna.com']},
    'Tabel_1A4': {'cols': ['nama_dtpr', 'sks_ps_sendiri', 'sks_ps_lain', 'sks_pt_lain', 'sks_penelitian', 'sks_pkm', 'sks_man_pt_sendiri', 'sks_man_pt_lain'], 'data': ['Andi, M.Kom', 6, 2, 0, 3, 1, 0, 0]},
    'Tabel_1A5': {'cols': ['jenis_tendik', 's3', 's2', 's1', 'd4', 'd3', 'd2', 'd1', 'sma', 'unit_kerja'], 'data': ['Pustakawan', 0, 1, 2, 0, 0, 0, 0, 0, 'Perpustakaan']},
    'Tabel_1B_SPMI': {'cols': ['nama_unit', 'dok_spmi', 'auditor_cert', 'auditor_non', 'freq_audit', 'bukti_pt', 'bukti_upps'], 'data': ['SPMI Pradita', 'SK-01', 2, 3, 2, 'link1', 'link2']},

    # Kriteria 2: Mahasiswa & Lulusan
    'Tabel_2A1_Mahasiswa': {'cols': ['tahun', 'daya_tampung', 'daftar_reg', 'daftar_rpl', 'daftar_afirm', 'daftar_khusus', 'baru_reg', 'baru_rpl', 'baru_afirm', 'baru_khusus', 'aktif_reg', 'aktif_rpl', 'aktif_afirm', 'aktif_khusus'], 'data': ['2025', 100, 150, 5, 2, 0, 90, 5, 2, 0, 300, 10, 5, 0]},
    'Tabel_2A2_Asal': {'cols': ['wilayah', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Lokal', 40, 50, 60, 'link-asal']},
    'Tabel_2A3_Kondisi': {'cols': ['tahun', 'mhs_baru', 'mhs_aktif', 'mhs_lulus', 'mhs_do'], 'data': ['2025', 100, 400, 80, 5]},
    'Tabel_2B1_Kurikulum': {
        'cols': ['kode_mk', 'nama_mk', 'bobot_sks', 'semester', 'cpl_sikap', 'cpl_pengetahuan', 'cpl_umum', 'cpl_khusus'],
        'data': ['INF101', 'Algoritma Pemrograman', 3, 1, 'v', 'v', 'v', 'v']
    },
    'Tabel_2B2_Pemetaan_CPL': {
        'cols': ['profil_lulusan', 'cpl_1', 'cpl_2', 'cpl_3', 'cpl_4', 'cpl_5'],
        'data': ['Software Engineer', 'v', 'v', '', 'v', '']
    },
    'Tabel_2B3_Pemenuhan_CPL': {
        'cols': ['capaian_pembelajaran', 'target_pencapaian', 'realisasi_ts2', 'realisasi_ts1', 'realisasi_ts'],
        'data': ['Mampu merancang arsitektur perangkat lunak', '80%', '75%', '78%', '82%']
    },
    'Tabel_2B4_Masa_Tunggu': {'cols': ['tahun', 'lulusan', 'terlacak', 'waktu_bulan'], 'data': ['2024', 100, 90, 4]},
    'Tabel_2B5_Bidang_Kerja': {'cols': ['tahun', 'terlacak', 'infokom', 'non_infokom', 'multi', 'nasional', 'wirausaha'], 'data': ['2024', 90, 70, 20, 10, 50, 10]},
    'Tabel_2B6_Kepuasan': {'cols': ['kemampuan', 'sangat_baik', 'baik', 'cukup', 'kurang', 'tindak_lanjut'], 'data': ['Etika', 60, 30, 10, 0, 'Sertifikasi']},
    'Tabel_2C_Fleksibilitas': {'cols': ['bentuk', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Magang', 20, 25, 30, 'link-flex']},
    'Tabel_2D_Rekognisi': {'cols': ['sumber', 'jenis', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Industri', 'Sertifikasi IT', 5, 10, 15, 'link-rek']},

    # Kriteria 3: DTPR & Penelitian
    'Tabel_3A1_Sarana': {'cols': ['nama', 'tampung', 'luas', 'milik', 'lisensi', 'alat', 'bukti'], 'data': ['Lab AI', 40, 60, 'M', 'P', 'Server GPU', 'link-sarana']},
    'Tabel_3A2_Penelitian': {'cols': ['ketua', 'mhs', 'judul', 'hibah', 'sumber', 'durasi', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Dr. Andi', 2, 'AI Tani', 'DIKTI', 'N', 1, 0, 50, 0, 'link-pen']},
    'Tabel_3A3_Pengembangan': {'cols': ['jenis', 'nama', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['S3', 'Budi', 1, 0, 0, 'link-dev']},
    'Tabel_3C1_Kerjasama': {'cols': ['judul', 'mitra', 'sumber', 'durasi', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['AI Dev', 'Google', 'I', 2, 0, 100, 100, 'link-ker']},
    'Tabel_3C2_Publikasi': {'cols': ['nama', 'judul', 'jenis', 'ts2', 'ts1', 'ts'], 'data': ['Andi', 'Paper AI', 'S1', 0, 1, 0]},
    'Tabel_3C3_HKI': {'cols': ['judul', 'jenis', 'nama', 'ts2', 'ts1', 'ts'], 'data': ['App Tani', 'Paten', 'Andi', 0, 0, 1]},

    # Kriteria 4: PkM (Pengabdian Masyarakat)
    'Tabel_4A1_Sarana_PkM': {'cols': ['nama', 'tampung', 'luas', 'milik', 'lisensi', 'alat', 'bukti'], 'data': ['Desa Digital', 100, 500, 'W', 'P', 'Internet', 'link-pkm']},
    'Tabel_4A2_PkM': {'cols': ['nama', 'judul', 'mhs', 'hibah', 'sumber', 'durasi', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Dr. Budi', 'Literasi IT', 5, 'Internal', 'L', 1, 10, 10, 10, 'link-pkm-res']},
    'Tabel_4C1_Kerja_PkM': {'cols': ['judul', 'mitra', 'sumber', 'durasi', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['UMKM Go Digital', 'PLN', 'N', 1, 0, 20, 0, 'link-pkm-ker']},
    'Tabel_4C2_Disem': {'cols': ['nama', 'judul', 'lni', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Budi', 'Jurnal PkM', 'N', 0, 1, 0, 'link-dis']},
    'Tabel_4C3_HKI_PkM': {'cols': ['judul', 'jenis', 'nama', 'ts2', 'ts1', 'ts', 'bukti'], 'data': ['Modul IT', 'Hak Cipta', 'Budi', 0, 1, 0, 'link-hki']},

    # Kriteria 5 & 6
    'Tabel_5_1_SI': {'cols': ['jenis', 'nama_si', 'akses', 'pengelola', 'bukti'], 'data': ['Akademik', 'SIAKAD', 'Web', 'Biro IT', 'link-si']},
    'Tabel_5_2_Sarana_Pendidikan': {'cols': ['nama', 'tampung', 'luas', 'milik', 'lisensi', 'alat', 'bukti'], 'data': ['Kelas 401', 40, 60, 'M', 'P', 'Proyektor', 'link-fas']},
    'Tabel_6_VisiMisi': {'cols': ['visi_pt', 'visi_upps', 'visi_ps', 'misi_pt', 'misi_upps'], 'data': ['Visi PT', 'Visi UPPS', 'Visi PS', 'Misi PT', 'Misi UPPS']}
}

file_path = os.path.join(folder_path, 'Template_Master_LKPS.xlsx')
with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
    for sheet_name, content in master_schema.items():
        pd.DataFrame([content['data']], columns=content['cols']).to_excel(writer, sheet_name=sheet_name, index=False)

print(f"SUKSES! {file_path} dibuat dengan {len(master_schema)} sheets.")