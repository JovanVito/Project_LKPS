from django.urls import path
from . import views

urlpatterns = [
    # Core
    path('', views.dashboard, name='dashboard'),
    path('prodi/', views.program_studi, name='program_studi'),
    path('users/', views.manajemen_user, name='manajemen_user'),
    path('sampul/', views.sampul, name='sampul'),
    path('logout/', views.logout_user, name='logout'),
    path('api/sync-lppm/', views.fetch_data_lppm, name='api_sync_lppm'),

    # Kriteria 1
    path('kriteria-1/1a1/', views.tabel_1a1, name='tabel_1a1'),
    path('kriteria-1/dana/', views.tabel_1a_dana, name='tabel_1a_dana'),
    path('kriteria-1/beban-dtpr/', views.tabel_1a4, name='tabel_1a4'),
    path('kriteria-1/tendik/', views.tabel_1a5, name='tabel_1a5'),
    path('kriteria-1/spmi/', views.tabel_1b, name='tabel_1b'),

    # Kriteria 2
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

    # Kriteria 3-6
    path('kriteria-3/penelitian/', views.tabel_3_penelitian, name='tabel_3_penelitian'),
    path('kriteria-3/dev-dtpr/', views.tabel_3a3, name='tabel_3a3'),
    path('kriteria-4/pkm/', views.tabel_4_pkm, name='tabel_4_pkm'),
    path('kriteria-5/sarana/', views.tabel_5_akuntabilitas, name='tabel_5_akuntabilitas'),
    path('kriteria-6/visi-misi/', views.tabel_6, name='tabel_6'),
]