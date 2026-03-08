from django.urls import path
from . import views

urlpatterns = [
    # Auth & Master
    path('', views.login, name='login'),
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
]