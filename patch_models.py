import os

new_models = """

class Tabel_1B_SPMI(models.Model):
    nama_unit = models.CharField(max_length=255)
    dokumen = models.CharField(max_length=255)
    jml_auditor_cert = models.IntegerField(default=0)
    jml_auditor_non = models.IntegerField(default=0)
    frekuensi_audit = models.IntegerField(default=0)
    link_pt = models.URLField(blank=True, null=True)
    link_upps = models.URLField(blank=True, null=True)

class Tabel_2C_Fleksibilitas(models.Model):
    bentuk_pembelajaran = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_2D_Rekognisi(models.Model):
    sumber = models.CharField(max_length=255)
    jenis_pengakuan = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

class Tabel_3A3_Pengembangan_DTPR(models.Model):
    jenis_pengembangan = models.CharField(max_length=255)
    nama_dosen = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)
"""

with open('lkps_app/models.py', 'a', encoding='utf-8') as f:
    f.write(new_models)
print("Models patched successfully")
