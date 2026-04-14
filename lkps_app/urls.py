from django.urls import path
from . import views

urlpatterns = [
    #Export ke Docx
    path('export-word/', views.export_lkps_word, name='export_word'),

    # Auth & Master
    path('', views.login_view, name='login'),
    path('logout/', views.halaman_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sampul/', views.sampul, name='sampul'),
    path('program-studi/', views.program_studi, name='program_studi'),
    path('manajemen-user/', views.manajemen_user, name='manajemen_user'),

    # Kriteria 1
    path('tabel-1a1-pimpinan/', views.tabel_1a1, name='tabel_1a1'),
    path('tabel-1a-dana/', views.tabel_1a_dana, name='tabel_1a_dana'),
    path('tabel-1a4-beban-dtpr/', views.tabel_1a4, name='tabel_1a4'),
    path('tabel-1a5-tendik/', views.tabel_1a5, name='tabel_1a5'),

    # Kriteria 2
    path('tabel-2a-mahasiswa/', views.tabel_2a_mahasiswa, name='tabel_2a_mahasiswa'),
    path('tabel-2b-kurikulum/', views.tabel_2b_kurikulum, name='tabel_2b_kurikulum'),
    path('tabel-2b-lulusan/', views.tabel_2b_lulusan, name='tabel_2b_lulusan'),

    # Kriteria 3 - 6
    path('tabel-3-penelitian/', views.tabel_3_penelitian, name='tabel_3_penelitian'),
    path('tabel-4-pkm/', views.tabel_4_pkm, name='tabel_4_pkm'),
    path('tabel-5-akuntabilitas/', views.tabel_5_akuntabilitas, name='tabel_5_akuntabilitas'),
    path('tabel-6-misi/', views.tabel_6_misi, name='tabel_6_misi'),
    # --- ADDED FROM FRONTEND MERGE ---
    path('prodi/', views.program_studi, name='program_studi'),
    path('users/', views.manajemen_user, name='manajemen_user'),
    path('api/sync-lppm/', views.fetch_data_lppm, name='api_sync_lppm'),
    path('kriteria-1/1a1/', views.tabel_1a1, name='tabel_1a1'),
    path('kriteria-1/dana/', views.tabel_1a_dana, name='tabel_1a_dana'),
    path('kriteria-1/beban-dtpr/', views.tabel_1a4, name='tabel_1a4'),
    path('kriteria-1/tendik/', views.tabel_1a5, name='tabel_1a5'),
    path('kriteria-1/spmi/', views.tabel_1b, name='tabel_1b'),
    path('kriteria-2/mhs-reguler/', views.tabel_2a1, name='tabel_2a1'),
    path('kriteria-2/asal-mhs/', views.tabel_2a2, name='tabel_2a2'),
    path('kriteria-2/kondisi-mhs/', views.tabel_2a3, name='tabel_2a3'),
    path('kriteria-2/kurikulum/', views.tabel_2b1, name='tabel_2b1'),
    path('kriteria-2/pemetaan-cpl/', views.tabel_2b2, name='tabel_2b2'),
    path('kriteria-2/pemenuhan-cpl/', views.tabel_2b3, name='tabel_2b3'),
    path('kriteria-2/masa-tunggu/', views.tabel_2b4, name='tabel_2b4'),
    path('kriteria-2/bidang-kerja/', views.tabel_2b5, name='tabel_2b5'),
    path('kriteria-2/kepuasan/', views.tabel_2b6, name='tabel_2b6'),
    path('kriteria-2/fleksibilitas/', views.tabel_2c, name='tabel_2c'),
    path('kriteria-2/rekognisi/', views.tabel_2d, name='tabel_2d'),
    path('kriteria-3/penelitian/', views.tabel_3_penelitian, name='tabel_3_penelitian'),
    path('kriteria-3/dev-dtpr/', views.tabel_3a3, name='tabel_3a3'),
    path('kriteria-4/pkm/', views.tabel_4_pkm, name='tabel_4_pkm'),
    path('kriteria-5/sarana/', views.tabel_5_akuntabilitas, name='tabel_5_akuntabilitas'),
    path('kriteria-6/visi-misi/', views.tabel_6, name='tabel_6'),
]