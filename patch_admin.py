import os

new_admin_str = """
# --- PENDAFTARAN TABEL BARU DARI FRONTEND MERGE ---

from .models import (
    Tabel_1B_SPMI, Tabel_2C_Fleksibilitas, Tabel_2D_Rekognisi, Tabel_3A3_Pengembangan_DTPR,
    TimPenyusun
)

@admin.register(Tabel_1B_SPMI)
class Tabel_1BAdmin(admin.ModelAdmin):
    list_display = ('nama_unit', 'dokumen', 'frekuensi_audit')

@admin.register(Tabel_2C_Fleksibilitas)
class Tabel_2CAdmin(admin.ModelAdmin):
    list_display = ('bentuk_pembelajaran', 'ts')

@admin.register(Tabel_2D_Rekognisi)
class Tabel_2DAdmin(admin.ModelAdmin):
    list_display = ('sumber', 'jenis_pengakuan', 'ts')

@admin.register(Tabel_3A3_Pengembangan_DTPR)
class Tabel_3A3Admin(admin.ModelAdmin):
    list_display = ('nama_dosen', 'jenis_pengembangan', 'ts')

@admin.register(TimPenyusun)
class TimPenyusunAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nidn', 'jabatan')

@admin.register(Tabel_4_Summary)
class Tabel_4_SummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_jenis_hibah', 'jml_disem_hasil')
"""

with open('lkps_app/admin.py', 'a', encoding='utf-8') as f:
    f.write("\n" + new_admin_str)

print("Admin patched successfully")
