from django.urls import path
from . import views

urlpatterns = [
    # Export ke Docx
    path('export/word/', views.export_lkps_word, name='export_word'),

    # Auth & Master
    path('', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sampul/', views.sampul, name='sampul'),
    path('prodi/', views.program_studi, name='program_studi'),
    path('users/', views.manajemen_user, name='manajemen_user'),
    path('db-explorer/', views.db_explorer, name='db_explorer'),
    path('api/sync-lppm/', views.fetch_data_lppm, name='api_sync_lppm'),
    path('api/import-excel/', views.import_excel, name='import_excel'),

    # =====================================================
    # DYNAMIC ROUTING — Satu URL pattern, banyak tabel
    # Kode tabel yang didukung: 1a1, 1b, 2b1, 2b2, 2b3, 2c, 2d, 3a3
    # =====================================================
    path('tabel/<str:kode_tabel>/', views.halaman_tabel_dinamis, name='halaman_tabel_dinamis'),

    # Backward-compatible named URLs agar {% url 'tabel_1a1' %} dll di template HTML tetap berfungsi.
    # Masing-masing hanya redirect ke dynamic view dengan kode_tabel yang sesuai.
    path('kriteria-1/1a1/',              views.halaman_tabel_dinamis, {'kode_tabel': '1a1'}, name='tabel_1a1'),
    path('kriteria-1/spmi/',             views.halaman_tabel_dinamis, {'kode_tabel': '1b'},  name='tabel_1b'),
    path('kriteria-2/kurikulum/',        views.halaman_tabel_dinamis, {'kode_tabel': '2b1'}, name='tabel_2b1'),
    path('kriteria-2/pemetaan-cpl/',     views.halaman_tabel_dinamis, {'kode_tabel': '2b2'}, name='tabel_2b2'),
    path('kriteria-2/pemenuhan-cpl/',    views.halaman_tabel_dinamis, {'kode_tabel': '2b3'}, name='tabel_2b3'),
    path('kriteria-2/fleksibilitas/',    views.halaman_tabel_dinamis, {'kode_tabel': '2c'},  name='tabel_2c'),
    path('kriteria-2/rekognisi/',        views.halaman_tabel_dinamis, {'kode_tabel': '2d'},  name='tabel_2d'),
    path('kriteria-3/dev-dtpr/',         views.halaman_tabel_dinamis, {'kode_tabel': '3a3'}, name='tabel_3a3'),

    # =====================================================
    # VIEWS KHUSUS — Tetap terpisah (logika kompleks)
    # =====================================================
    # Kriteria 1 (multi-model / field merging)
    path('kriteria-1/dana/', views.tabel_1a_dana, name='tabel_1a_dana'),
    path('kriteria-1/beban-dtpr/', views.tabel_1a4, name='tabel_1a4'),
    path('kriteria-1/tendik/', views.tabel_1a5, name='tabel_1a5'),

    # Kriteria 2 (fixed-row updates / multi-model)
    path('kriteria-2/mhs-reguler/', views.tabel_2a1, name='tabel_2a1'),
    path('kriteria-2/asal-mhs/', views.tabel_2a2, name='tabel_2a2'),
    path('kriteria-2/kondisi-mhs/', views.tabel_2a3, name='tabel_2a3'),
    path('kriteria-2/masa-tunggu/', views.tabel_2a4, name='tabel_2b4'),
    path('kriteria-2/bidang-kerja/', views.tabel_2a5, name='tabel_2b5'),
    path('kriteria-2/kepuasan/', views.tabel_2a6, name='tabel_2b6'),

    # Kriteria 3 (multi-model mega page)
    path('kriteria-3/penelitian/', views.tabel_3_penelitian, name='tabel_3_penelitian'),

    # Kriteria 4 (multi-model mega page)
    path('kriteria-4/pkm/', views.tabel_4_pkm, name='tabel_4_pkm'),

    # Kriteria 5 (multi-model + fixed rows)
    path('kriteria-5/sarana/', views.tabel_5_akuntabilitas, name='tabel_5_akuntabilitas'),

    # Kriteria 6 (singleton update_or_create)
    path('kriteria-6/visi-misi/', views.tabel_6_misi, name='tabel_6'),
]