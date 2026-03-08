import pandas as pd
import os

# Karena folder static kamu ada di luar (sejajar manage.py), path-nya seperti ini:
folder_path = os.path.join('static', 'lkps_app', 'excel_templates')
os.makedirs(folder_path, exist_ok=True)

# Skema Database: Nama file -> Nama Sheet -> Kolom & Data Dummy
# NAMA KOLOM HARUS 100% SAMA DENGAN ATRIBUT name="[...]" DI HTML!
files_schema = {
    'template_1a1.xlsx': {
        'Tabel_1A1': {
            'cols': ['unit_kerja', 'nama_ketua', 'periode_jabatan', 'pendidikan_terakhir', 'jabatan_fungsional', 'tupoksi'],
            'data': ['Fakultas Teknologi', 'Dr. Budi Santoso', '2022 - 2026', 'S3', 'Lektor Kepala', 'Memimpin Fakultas dan operasional akademik.']
        }
    },
    'template_1a4.xlsx': {
        'Tabel_1A4': {
            'cols': ['nama_dtpr', 'sks_pengajaran_ps_sendiri', 'sks_pengajaran_ps_lain', 'sks_pengajaran_pt_lain', 'sks_penelitian', 'sks_pengabdian', 'sks_manajemen_pt_sendiri', 'sks_manajemen_pt_lain'],
            'data': ['Dr. Andi Suryadi', 6, 2, 0, 3, 3, 0, 0]
        }
    },
    'template_1a_dana.xlsx': {
        'Tabel_1A2_Sumber': {
            'cols': ['sumber_dana', 'sumber_ts2', 'sumber_ts1', 'sumber_ts', 'link_sumber'],
            'data': ['Mahasiswa (SPP)', 150, 180, 200, 'https://pradita.ac.id/bukti-dana']
        },
        'Tabel_1A3_Penggunaan': {
            'cols': ['guna_dana', 'guna_ts2', 'guna_ts1', 'guna_ts', 'link_guna'],
            'data': ['Pendidikan', 100, 120, 150, 'https://pradita.ac.id/bukti-penggunaan']
        }
    },
    'template_1a5.xlsx': {
        'Tabel_1A5': {
            'cols': ['jenis_tendik', 'jml_s3', 'jml_s2', 'jml_s1', 'jml_d4', 'jml_d3', 'jml_d2', 'jml_d1', 'jml_sma', 'unit_kerja'],
            'data': ['Pustakawan', 0, 1, 2, 0, 1, 0, 0, 0, 'Perpustakaan Pusat Pradita']
        }
    },
    'template_2a_mahasiswa.xlsx': {
        'Tabel_2A1_Data_Mhs': {
            'cols': ['tahun_akademik', 'daya_tampung', 'pendaftar_reg', 'pendaftar_afi', 'pendaftar_khu', 'lulus_reg', 'lulus_afi', 'lulus_khu', 'lulus_rpl', 'maba_reg', 'maba_afi', 'maba_khu', 'maba_rpl', 'aktif_reg', 'aktif_afi', 'aktif_khu', 'aktif_rpl'],
            'data': ['TS', 100, 200, 10, 5, 100, 8, 2, 0, 95, 8, 2, 0, 380, 20, 5, 0]
        },
        'Tabel_2A2_Asal': {
            'cols': ['asal_mahasiswa', 'asal_ts2', 'asal_ts1', 'asal_ts', 'link_asal'],
            'data': ['Kota/Kabupaten Lain', 50, 60, 70, 'https://bukti-asal.com']
        },
        'Tabel_2A3_Kondisi': {
            'cols': ['status_mahasiswa', 'kondisi_ts2', 'kondisi_ts1', 'kondisi_ts'],
            'data': ['Mahasiswa Aktif pada saat TS', 300, 350, 400]
        }
    },
    'template_2b_kurikulum.xlsx': {
        'Tabel_2B1_Isi': {
            'cols': ['nama_mk', 'sks_mk', 'smt_mk', 'pl1', 'pl2', 'pl3', 'pl4'],
            'data': ['Pemrograman Berorientasi Objek', 3, 2, 1, 0, 1, 0]
        },
        'Tabel_2B2_Pemetaan': {
            'cols': ['kode_cpl', 'map_pl1', 'map_pl2', 'map_pl3', 'map_pl4'],
            'data': ['CPL 01', 1, 1, 0, 0]
        },
        'Tabel_2B3_Pemenuhan': {
            'cols': ['pem_cpl', 'pem_cpmk', 'pem_smt1', 'pem_smt2', 'pem_smt3'],
            'data': ['CPL 01', 'CPMK 01', 'Algoritma', 'Struktur Data', '']
        }
    },
    'template_2b_lulusan.xlsx': {
        'Tabel_2B4_Masa_Tunggu': {
            'cols': ['tahun_lulus', 'tunggu_lulusan', 'tunggu_terlacak', 'tunggu_bulan'],
            'data': ['TS', 100, 90, 3.5]
        },
        'Tabel_2B5_Bidang_Kerja': {
            'cols': ['tahun_lulus_bdg', 'bidang_lulusan', 'bidang_terlacak', 'bidang_info', 'bidang_non', 'bidang_multi', 'bidang_nas', 'bidang_wira'],
            'data': ['TS', 100, 90, 80, 10, 5, 75, 10]
        },
        'Tabel_2B6_Kepuasan': {
            'cols': ['kemampuan', 'kepuasan_sb', 'kepuasan_b', 'kepuasan_c', 'kepuasan_k', 'tindak_lanjut'],
            'data': ['Kerjasama Tim', 50.5, 39.5, 10, 0, 'Peningkatan project base learning di semester 5']
        }
    },
    'template_3_penelitian.xlsx': {
        'Tabel_3A1_Prasarana': {
            'cols': ['nama_prasarana', 'daya_tampung', 'luas_ruang', 'kepemilikan', 'lisensi', 'perangkat', 'link_bukti_prasarana'],
            'data': ['Lab Kecerdasan Buatan', 40, 60, 'M', 'L', '40 PC High End, GPU Server', 'https://lab-ai.com']
        },
        'Tabel_3A2_Penelitian': {
            'cols': ['nama_dtpr_ketua', 'jml_mhs_terlibat', 'judul_penelitian', 'jenis_hibah', 'sumber_lni', 'durasi_tahun', 'dana_ts2', 'dana_ts1', 'dana_ts', 'link_bukti_penelitian'],
            'data': ['Dr. Andi Suryadi', 2, 'Deteksi Hama via IoT', 'Hibah Bersaing', 'N', 1, 0, 50, 0, 'https://bukti-penelitian.com']
        },
        'Tabel_3C1_Kerjasama': {
            'cols': ['judul_kerjasama', 'mitra_kerjasama', 'sumber_kerjasama_lni', 'durasi_kerjasama', 'dana_k_ts2', 'dana_k_ts1', 'dana_k_ts', 'link_bukti_kerjasama'],
            'data': ['Pengembangan Sistem AI Pertanian', 'PT Telkom Agritech', 'N', 2, 0, 100, 100, 'https://bukti-kerjasama.com']
        },
        'Tabel_3C2_Publikasi': {
            'cols': ['nama_dtpr_pub', 'judul_pub', 'jenis_pub', 'pub_ts2', 'pub_ts1', 'pub_ts'],
            'data': ['Dr. Andi Suryadi', 'Jurnal Internasional Machine Learning', 'S1', 0, 1, 0]
        },
        'Tabel_3C3_HKI': {
            'cols': ['judul_hki', 'jenis_hki', 'nama_dtpr_hki', 'hki_ts2', 'hki_ts1', 'hki_ts'],
            'data': ['Algoritma Cerdas Pendeteksi Daun', 'Paten', 'Dr. Andi Suryadi', 0, 0, 1]
        }
    },
    'template_4_pkm.xlsx': {
        'Tabel_4A1_Prasarana': {
            'cols': ['nama_prasarana_pkm', 'daya_tampung_pkm', 'luas_ruang_pkm', 'kepemilikan_pkm', 'lisensi_pkm', 'perangkat_pkm', 'link_bukti_prasarana_pkm'],
            'data': ['Desa Binaan Tanjung', 100, 500, 'W', 'P', 'Peralatan Pertanian Pintar', 'https://desa-binaan.com']
        },
        'Tabel_4A2_PkM': {
            'cols': ['nama_dtpr_pkm', 'judul_kegiatan_pkm', 'jml_mhs_pkm', 'jenis_hibah_pkm', 'sumber_dana_pkm', 'durasi_pkm', 'dana_pkm_ts2', 'dana_pkm_ts1', 'dana_pkm_ts', 'link_bukti_dana_pkm'],
            'data': ['Dr. Budi Santoso', 'Pelatihan Komputer Desa', 5, 'Internal Kampus', 'L', 1, 10, 15, 20, 'https://bukti-pkm.com']
        },
        'Tabel_4C1_Kerjasama': {
            'cols': ['judul_kerjasama_pkm', 'mitra_kerjasama_pkm', 'sumber_kerja_pkm', 'durasi_kerja_pkm', 'dana_kpkm_ts2', 'dana_kpkm_ts1', 'dana_kpkm_ts', 'link_bukti_kerja_pkm'],
            'data': ['Pendampingan Digitalisasi UMKM', 'Dinas Koperasi Tangerang', 'L', 1, 0, 50, 0, 'https://bukti-kerja-pkm.com']
        },
        'Tabel_4C2_Diseminasi': {
            'cols': ['nama_dtpr_disem', 'judul_disem', 'lni_disem', 'disem_ts2', 'disem_ts1', 'disem_ts', 'link_bukti_disem'],
            'data': ['Dr. Budi Santoso', 'Artikel Jurnal Pengabdian Masyarakat', 'N', 0, 1, 0, 'https://bukti-disem.com']
        },
        'Tabel_4C3_HKI_PkM': {
            'cols': ['judul_hki_pkm', 'jenis_hki_pkm', 'nama_dtpr_hki_pkm', 'hkipkm_ts2', 'hkipkm_ts1', 'hkipkm_ts', 'link_bukti_hki_pkm'],
            'data': ['Modul Pelatihan IT Dasar', 'Hak Cipta', 'Dr. Budi Santoso', 0, 1, 0, 'https://bukti-hkipkm.com']
        }
    },
    'template_5_akuntabilitas.xlsx': {
        'Tabel_5_1_Tata_Kelola': {
            'cols': ['jenis_tata_kelola', 'nama_sistem_info', 'akses_sistem', 'unit_pengelola_sistem', 'link_bukti_sistem'],
            'data': ['Pendidikan', 'SIAKAD Pradita', 'Internet', 'Biro Akademik', 'https://siakad.pradita.ac.id']
        },
        'Tabel_5_2_Sarana': {
            'cols': ['nama_prasarana_pend', 'daya_tampung_pend', 'luas_ruang_pend', 'kepemilikan_pend', 'lisensi_pend', 'perangkat_pend', 'link_bukti_prasarana_pend'],
            'data': ['Ruang Kelas Eksekutif A', 40, 60, 'M', 'P', 'Proyektor Interaktif, AC Central', 'https://pradita.ac.id/fasilitas']
        }
    }
}

print(f"Mulai membuat dan menyinkronkan Template Excel V2.0 di folder: {folder_path} ...")

# Looping utama untuk membuat file dan sheets
for filename, sheets in files_schema.items():
    file_path = os.path.join(folder_path, filename)
    
    # Menggunakan ExcelWriter untuk mendukung multiple sheets dalam 1 file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for sheet_name, content in sheets.items():
            df = pd.DataFrame([content['data']], columns=content['cols'])
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
    print(f"  [SUKSES] {filename} berhasil dibuat dengan {len(sheets)} sheet(s).")

print("\nSELESAI! Seluruh file Excel sekarang 100% SINKRON dengan atribut HTML yang baru!")