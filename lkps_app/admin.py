from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    ProgramStudi, ProfilPengguna, IdentitasPengusul, TimPenyusun,
    Tabel_1A1, Tabel_1A2_Sumber, Tabel_1A3_Penggunaan, Tabel_1A4, Tabel_1A5, Tabel_1B_SPMI,
    Tabel_2A_Mahasiswa, Tabel_2A2_Asal, Tabel_2A3_Kondisi,
    Tabel_2B1_MK, Tabel_2B2_CPL, Tabel_2B3_Pemenuhan, Tabel_2B4_MasaTunggu, Tabel_2B5_BidangKerja, Tabel_2B6_Kepuasan, Tabel_2B_Summary,
    Tabel_2C_Fleksibilitas, Tabel_2D_Rekognisi,
    Tabel_3A1_Sarana, Tabel_3A2_Penelitian, Tabel_3A3_Pengembangan_DTPR, Tabel_3C1_Kerjasama, Tabel_3C2_Publikasi, Tabel_3C3_HKI, Tabel_3_Summary,
    Tabel_4A1_Sarana, Tabel_4A2_PkM, Tabel_4C1_Kerjasama, Tabel_4C2_Diseminasi, Tabel_4C3_HKI, Tabel_4_Summary,
    Tabel_5_1_TataKelola, Tabel_5_2_Sarana, Tabel_6_Misi,
)


# ==========================================
# USER & PROFIL PENGGUNA
# ==========================================

class ProfilPenggunaInline(admin.StackedInline):
    model = ProfilPengguna
    can_delete = False
    verbose_name_plural = 'Profil Tambahan (Role & Akses LKPS)'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfilPenggunaInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# ==========================================
# MASTER DATA
# ==========================================

@admin.register(ProgramStudi)
class ProgramStudiAdmin(admin.ModelAdmin):
    list_display = ('nama_prodi', 'jenjang_studi', 'akreditasi', 'no_sk')
    search_fields = ('nama_prodi',)
    list_filter = ('jenjang_studi', 'akreditasi')

@admin.register(IdentitasPengusul)
class IdentitasPengusulAdmin(admin.ModelAdmin):
    list_display = ('program_studi', 'unit_pengelola', 'updated_at')

@admin.register(TimPenyusun)
class TimPenyusunAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nidn', 'jabatan')


# ==========================================
# KRITERIA 1: TATA PAMONG & KERJASAMA
# ==========================================

@admin.register(Tabel_1A1)
class Tabel_1A1Admin(admin.ModelAdmin):
    list_display = ('unit_kerja', 'nama_ketua', 'periode_jabatan', 'pendidikan_terakhir', 'jabatan_fungsional')
    search_fields = ('unit_kerja', 'nama_ketua')
    list_filter = ('pendidikan_terakhir', 'jabatan_fungsional')

@admin.register(Tabel_1A2_Sumber)
class Tabel_1A2Admin(admin.ModelAdmin):
    list_display = ('sumber_dana', 'ts_2', 'ts_1', 'ts')

@admin.register(Tabel_1A3_Penggunaan)
class Tabel_1A3Admin(admin.ModelAdmin):
    list_display = ('penggunaan', 'ts_2', 'ts_1', 'ts')

@admin.register(Tabel_1A4)
class Tabel_1A4Admin(admin.ModelAdmin):
    list_display = ('nama_dosen', 'sks_ps_sendiri', 'sks_penelitian', 'sks_pkm', 'sks_tambahan')
    search_fields = ('nama_dosen',)

@admin.register(Tabel_1A5)
class Tabel_1A5Admin(admin.ModelAdmin):
    list_display = ('jenis_tenaga', 'unit_kerja', 's3', 's2', 's1', 'd3')
    search_fields = ('jenis_tenaga', 'unit_kerja')
    list_filter = ('unit_kerja',)

@admin.register(Tabel_1B_SPMI)
class Tabel_1BAdmin(admin.ModelAdmin):
    list_display = ('nama_unit', 'dokumen', 'frekuensi_audit')


# ==========================================
# KRITERIA 2: MAHASISWA & LULUSAN
# ==========================================

@admin.register(Tabel_2A_Mahasiswa)
class Tabel_2A_MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('tahun_akademik', 'daya_tampung', 'pendaftar', 'total_mhs_reguler')
    search_fields = ('tahun_akademik',)
    list_filter = ('tahun_akademik',)

@admin.register(Tabel_2A2_Asal)
class Tabel_2A2_AsalAdmin(admin.ModelAdmin):
    list_display = ('asal_mahasiswa', 'ts_2', 'ts_1', 'ts')
    search_fields = ('asal_mahasiswa',)

@admin.register(Tabel_2A3_Kondisi)
class Tabel_2A3_KondisiAdmin(admin.ModelAdmin):
    list_display = ('status', 'ts_2', 'ts_1', 'ts')
    search_fields = ('status',)

@admin.register(Tabel_2B1_MK)
class Tabel_2B1_MKAdmin(admin.ModelAdmin):
    list_display = ('nama_mk', 'sks', 'semester', 'pl1', 'pl2', 'pl3', 'pl4')
    search_fields = ('nama_mk',)

@admin.register(Tabel_2B2_CPL)
class Tabel_2B2_CPLAdmin(admin.ModelAdmin):
    list_display = ('kode_cpl', 'pl1', 'pl2', 'pl3', 'pl4')
    search_fields = ('kode_cpl',)

@admin.register(Tabel_2B3_Pemenuhan)
class Tabel_2B3_PemenuhanAdmin(admin.ModelAdmin):
    list_display = ('cpl', 'cpmk', 'smt1', 'smt2', 'smt3')
    search_fields = ('cpl', 'cpmk')

@admin.register(Tabel_2B4_MasaTunggu)
class Tabel_2B4Admin(admin.ModelAdmin):
    list_display = ('tahun_lulus', 'jml_lulusan', 'jml_terlacak', 'waktu_tunggu')

@admin.register(Tabel_2B5_BidangKerja)
class Tabel_2B5Admin(admin.ModelAdmin):
    list_display = ('tahun_lulus', 'jml_lulusan', 'bidang_infokom', 'bidang_non_infokom')

@admin.register(Tabel_2B6_Kepuasan)
class Tabel_2B6Admin(admin.ModelAdmin):
    list_display = ('jenis_kemampuan', 'sangat_baik', 'baik', 'cukup', 'kurang')

@admin.register(Tabel_2B_Summary)
class Tabel_2BSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_alumni_3thn', 'total_responden', 'total_mhs_aktif_ts')

@admin.register(Tabel_2C_Fleksibilitas)
class Tabel_2CAdmin(admin.ModelAdmin):
    list_display = ('bentuk_pembelajaran', 'ts_2', 'ts_1', 'ts')

@admin.register(Tabel_2D_Rekognisi)
class Tabel_2DAdmin(admin.ModelAdmin):
    list_display = ('sumber', 'jenis_pengakuan', 'ts_2', 'ts_1', 'ts')


# ==========================================
# KRITERIA 3: PENELITIAN
# ==========================================

@admin.register(Tabel_3A1_Sarana)
class Tabel_3A1Admin(admin.ModelAdmin):
    list_display = ('nama_prasarana', 'daya_tampung', 'kepemilikan', 'lisensi')

@admin.register(Tabel_3A2_Penelitian)
class Tabel_3A2Admin(admin.ModelAdmin):
    list_display = ('nama_dtpr', 'jenis_hibah', 'sumber_lni', 'dana_ts')

@admin.register(Tabel_3A3_Pengembangan_DTPR)
class Tabel_3A3Admin(admin.ModelAdmin):
    list_display = ('nama_dosen', 'jenis_pengembangan', 'ts_2', 'ts_1', 'ts')

@admin.register(Tabel_3C1_Kerjasama)
class Tabel_3C1Admin(admin.ModelAdmin):
    list_display = ('mitra', 'sumber_lni', 'dana_ts')

@admin.register(Tabel_3C2_Publikasi)
class Tabel_3C2Admin(admin.ModelAdmin):
    list_display = ('nama_dtpr', 'jenis_pub', 'ts2', 'ts1', 'ts')

@admin.register(Tabel_3C3_HKI)
class Tabel_3C3Admin(admin.ModelAdmin):
    list_display = ('judul', 'jenis_hki', 'nama_dtpr')

@admin.register(Tabel_3_Summary)
class Tabel_3SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'link_roadmap', 'total_jenis_hibah', 'total_mitra')


# ==========================================
# KRITERIA 4: PkM
# ==========================================

@admin.register(Tabel_4A1_Sarana)
class Tabel_4A1Admin(admin.ModelAdmin):
    list_display = ('nama_prasarana', 'daya_tampung', 'kepemilikan', 'lisensi')

@admin.register(Tabel_4A2_PkM)
class Tabel_4A2Admin(admin.ModelAdmin):
    list_display = ('nama_dtpr', 'jenis_hibah', 'sumber_lni', 'dana_ts')

@admin.register(Tabel_4C1_Kerjasama)
class Tabel_4C1Admin(admin.ModelAdmin):
    list_display = ('mitra', 'sumber_lni', 'dana_ts')

@admin.register(Tabel_4C2_Diseminasi)
class Tabel_4C2Admin(admin.ModelAdmin):
    list_display = ('nama_dtpr', 'lni', 'ts2', 'ts1', 'ts')

@admin.register(Tabel_4C3_HKI)
class Tabel_4C3Admin(admin.ModelAdmin):
    list_display = ('judul', 'jenis_hki', 'nama_dtpr')

@admin.register(Tabel_4_Summary)
class Tabel_4_SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_jenis_hibah', 'jml_disem_hasil')


# ==========================================
# KRITERIA 5 & 6
# ==========================================

@admin.register(Tabel_5_1_TataKelola)
class Tabel_5_1Admin(admin.ModelAdmin):
    list_display = ('jenis_tata_kelola', 'nama_sistem', 'akses', 'unit_pengelola')
    search_fields = ('jenis_tata_kelola', 'nama_sistem')

@admin.register(Tabel_5_2_Sarana)
class Tabel_5_2Admin(admin.ModelAdmin):
    list_display = ('nama_prasarana', 'daya_tampung', 'kepemilikan', 'lisensi')
    search_fields = ('nama_prasarana',)

@admin.register(Tabel_6_Misi)
class Tabel_6_MisiAdmin(admin.ModelAdmin):
    list_display = ('id', 'tampil_visi_pt')

    def tampil_visi_pt(self, obj):
        if obj.visi_pt:
            return obj.visi_pt[:50] + "..." if len(obj.visi_pt) > 50 else obj.visi_pt
        return "-"
    tampil_visi_pt.short_description = "Visi PT"
