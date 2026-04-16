# lkps_app/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# ==========================================
# MODEL MASTER (Tabel Referensi)
# ==========================================

class ProgramStudi(models.Model):
    nama_prodi = models.CharField(max_length=100, unique=True)
    jenjang_studi = models.CharField(max_length=100)
    akreditasi = models.CharField(max_length=50)
    no_sk = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nama_prodi} ({self.jenjang_studi})"

    class Meta:
        verbose_name = "Program Studi"
        verbose_name_plural = "Program Studi"

class ProfilPengguna(models.Model):
    # Menyambungkan tabel ini dengan tabel User bawaan Django (One-to-One)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nomor_induk = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50)
    akses_prodi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} - {self.role}"

    class Meta:
        verbose_name = "Profil Pengguna"
        verbose_name_plural = "Profil Pengguna"

# ==========================================
# MODEL DATA LKPS
# ==========================================

# Class abstrak agar kita tidak perlu menulis ulang kolom waktu_resmi di setiap tabel
class TimeStampedModel(models.Model):
    """
    Class abstrak yang menyediakan field waktu_resmi otomatis
    sesuai requirements Excel.
    """
    waktu_resmi = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True) # Waktu dibuat
    updated_at = models.DateTimeField(auto_now=True)     # Waktu terakhir diupdate (auto-save)

    class Meta:
        abstract = True


# ==========================================
# IDENTITAS & TIM PENYUSUN
# ==========================================

class IdentitasPengusul(TimeStampedModel):
    program_studi = models.OneToOneField(ProgramStudi, on_delete=models.CASCADE, related_name='identitas_pengusul')
    logo_pt = models.ImageField(upload_to='logo/', null=True, blank=True)

    # Field Halaman Muka
    nama_ps_sampul = models.CharField(max_length=200, blank=True)
    nama_pt_sampul = models.CharField(max_length=200, blank=True)
    kota_sampul = models.CharField(max_length=100, blank=True)
    tahun_sampul = models.IntegerField(default=2026)
    
    # Field Identitas Pengusul
    unit_pengelola = models.CharField(max_length=200, blank=True)
    perguruan_tinggi = models.CharField(max_length=200, blank=True)
    alamat = models.TextField(blank=True)
    telepon = models.CharField(max_length=50, blank=True)
    email_web = models.CharField(max_length=200, blank=True)
    sk_pt = models.CharField(max_length=100, blank=True)
    tgl_sk_pt = models.DateField(null=True, blank=True)
    sk_ps = models.CharField(max_length=100, blank=True)
    tgl_sk_ps = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.perguruan_tinggi or 'Identitas'} - {self.unit_pengelola or 'UPPS'}"

    class Meta:
        verbose_name = "Identitas Pengusul"
        verbose_name_plural = "Identitas Pengusul"

class TimPenyusun(models.Model):
    identitas = models.ForeignKey(IdentitasPengusul, on_delete=models.CASCADE, related_name='tim_penyusun')
    nama = models.CharField(max_length=200, blank=True)
    nidn = models.CharField(max_length=50, blank=True)
    jabatan = models.CharField(max_length=100, blank=True)
    tanggal_pengisian = models.DateField(null=True, blank=True)
    # UBAH KE ImageField agar bisa diatur ukurannya nanti di laporan
    tanda_tangan = models.ImageField(upload_to='ttd_penyusun/', null=True, blank=True)

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"

    class Meta:
        verbose_name = "Tim Penyusun"
        verbose_name_plural = "Tim Penyusun"


# ==========================================
# KRITERIA 1: TATA PAMONG & KERJASAMA
# ==========================================

class Tabel_1A1(models.Model):
    unit_kerja = models.CharField(max_length=255)
    nama_ketua = models.CharField(max_length=255)
    periode_jabatan = models.CharField(max_length=100)
    pendidikan_terakhir = models.CharField(max_length=50)
    jabatan_fungsional = models.CharField(max_length=100)
    tupoksi = models.TextField() # Untuk deskripsi tugas yang panjang

    def __str__(self):
        return f"{self.unit_kerja} - {self.nama_ketua}"

    class Meta:
        verbose_name = "1.A.1 Pimpinan & Tupoksi"
        verbose_name_plural = "1.A.1 Pimpinan & Tupoksi"

class Tabel_1A2_Sumber(models.Model):
    sumber_dana = models.CharField(max_length=255)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.sumber_dana

    class Meta:
        verbose_name = "1.A.2 Sumber Pendanaan"
        verbose_name_plural = "1.A.2 Sumber Pendanaan"

class Tabel_1A3_Penggunaan(models.Model):
    penggunaan = models.CharField(max_length=255)
    ts_2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts_1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.penggunaan

    class Meta:
        verbose_name = "1.A.3 Penggunaan Dana"
        verbose_name_plural = "1.A.3 Penggunaan Dana"

class Tabel_1A4(models.Model):
    nama_dosen = models.CharField(max_length=255)
    sks_ps_sendiri = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_ps_lain = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_pt_lain = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_penelitian = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_pkm = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sks_tambahan = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.nama_dosen

    class Meta:
        verbose_name = "1.A.4 Beban Kerja DTPR"
        verbose_name_plural = "1.A.4 Beban Kerja DTPR"

class Tabel_1A5(models.Model):
    jenis_tenaga = models.CharField(max_length=255)
    s3 = models.IntegerField(default=0)
    s2 = models.IntegerField(default=0)
    s1 = models.IntegerField(default=0)
    d3 = models.IntegerField(default=0)
    d2_d1 = models.IntegerField(default=0)
    sma_smk = models.IntegerField(default=0)
    unit_kerja = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.jenis_tenaga} - {self.unit_kerja}"

    class Meta:
        verbose_name = "1.A.5 Tenaga Kependidikan"
        verbose_name_plural = "1.A.5 Tenaga Kependidikan"

class Tabel_1B_SPMI(models.Model):
    nama_unit = models.CharField(max_length=255)
    dokumen = models.CharField(max_length=255)
    jml_auditor_cert = models.IntegerField(default=0)
    jml_auditor_non = models.IntegerField(default=0)
    frekuensi_audit = models.IntegerField(default=0)
    link_pt = models.URLField(blank=True, null=True)
    link_upps = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nama_unit

    class Meta:
        verbose_name = "1.B Unit SPMI"
        verbose_name_plural = "1.B Unit SPMI"


# ==========================================
# KRITERIA 2: MAHASISWA & LULUSAN
# ==========================================

class Tabel_2A_Mahasiswa(models.Model):
    tahun_akademik = models.CharField(max_length=20)
    daya_tampung = models.IntegerField(default=0)
    pendaftar = models.IntegerField(default=0)
    lulus_seleksi = models.IntegerField(default=0)
    mhs_baru_reguler = models.IntegerField(default=0)
    mhs_baru_transfer = models.IntegerField(default=0)
    total_mhs_reguler = models.IntegerField(default=0)
    total_mhs_transfer = models.IntegerField(default=0)

    def __str__(self):
        return f"Mahasiswa {self.tahun_akademik}"

    class Meta:
        verbose_name = "2.A.1 Data Mahasiswa"
        verbose_name_plural = "2.A.1 Data Mahasiswa"

class Tabel_2A2_Asal(models.Model):
    asal_mahasiswa = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.asal_mahasiswa

    class Meta:
        verbose_name = "2.A.2 Keragaman Asal"
        verbose_name_plural = "2.A.2 Keragaman Asal"

class Tabel_2A3_Kondisi(models.Model):
    status = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = "2.A.3 Kondisi Jumlah"
        verbose_name_plural = "2.A.3 Kondisi Jumlah"

class Tabel_2B1_MK(models.Model):
    nama_mk = models.CharField(max_length=255)
    sks = models.IntegerField(default=0)
    semester = models.IntegerField(default=0)
    pl1 = models.BooleanField(default=False)
    pl2 = models.BooleanField(default=False)
    pl3 = models.BooleanField(default=False)
    pl4 = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama_mk} ({self.sks} SKS)"

    class Meta:
        verbose_name = "2.B.1 Isi Kurikulum"
        verbose_name_plural = "2.B.1 Isi Kurikulum"

class Tabel_2B2_CPL(models.Model):
    kode_cpl = models.CharField(max_length=100)
    pl1 = models.BooleanField(default=False)
    pl2 = models.BooleanField(default=False)
    pl3 = models.BooleanField(default=False)
    pl4 = models.BooleanField(default=False)

    def __str__(self):
        return self.kode_cpl

    class Meta:
        verbose_name = "2.B.2 Pemetaan CPL"
        verbose_name_plural = "2.B.2 Pemetaan CPL"

class Tabel_2B3_Pemenuhan(models.Model):
    cpl = models.CharField(max_length=100)
    cpmk = models.CharField(max_length=100)
    smt1 = models.CharField(max_length=100, blank=True)
    smt2 = models.CharField(max_length=100, blank=True)
    smt3 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.cpl} - {self.cpmk}"

    class Meta:
        verbose_name = "2.B.3 Pemenuhan CPL"
        verbose_name_plural = "2.B.3 Pemenuhan CPL"

class Tabel_2B4_MasaTunggu(models.Model):
    tahun_lulus = models.CharField(max_length=20)
    jml_lulusan = models.IntegerField(default=0)
    jml_terlacak = models.IntegerField(default=0)
    waktu_tunggu = models.DecimalField(max_digits=5, decimal_places=1, default=0)

    def __str__(self):
        return f"Lulusan {self.tahun_lulus}"

    class Meta:
        verbose_name = "2.B.4 Masa Tunggu"
        verbose_name_plural = "2.B.4 Masa Tunggu"

class Tabel_2B5_BidangKerja(models.Model):
    tahun_lulus = models.CharField(max_length=20)
    jml_lulusan = models.IntegerField(default=0)
    jml_terlacak = models.IntegerField(default=0)
    bidang_infokom = models.IntegerField(default=0)
    bidang_non_infokom = models.IntegerField(default=0)
    tingkat_multinasional = models.IntegerField(default=0)
    tingkat_nasional = models.IntegerField(default=0)
    tingkat_wirausaha = models.IntegerField(default=0)

    def __str__(self):
        return f"Bidang Kerja {self.tahun_lulus}"

    class Meta:
        verbose_name = "2.B.5 Bidang Kerja"
        verbose_name_plural = "2.B.5 Bidang Kerja"

class Tabel_2B6_Kepuasan(models.Model):
    jenis_kemampuan = models.CharField(max_length=255)
    sangat_baik = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    baik = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    cukup = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    kurang = models.DecimalField(max_digits=5, decimal_places=1, default=0)
    tindak_lanjut = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.jenis_kemampuan

    class Meta:
        verbose_name = "2.B.6 Kepuasan Pengguna"
        verbose_name_plural = "2.B.6 Kepuasan Pengguna"

class Tabel_2B_Summary(models.Model):
    total_alumni_3thn = models.IntegerField(default=0)
    total_responden = models.IntegerField(default=0)
    total_mhs_aktif_ts = models.IntegerField(default=0)

    def __str__(self):
        return f"Ringkasan: {self.total_alumni_3thn} alumni, {self.total_responden} responden"

    class Meta:
        verbose_name = "2.B Ringkasan Lulusan"
        verbose_name_plural = "2.B Ringkasan Lulusan"

class Tabel_2C_Fleksibilitas(models.Model):
    bentuk_pembelajaran = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.bentuk_pembelajaran

    class Meta:
        verbose_name = "2.C Fleksibilitas Kurikulum"
        verbose_name_plural = "2.C Fleksibilitas Kurikulum"

class Tabel_2D_Rekognisi(models.Model):
    sumber = models.CharField(max_length=255)
    jenis_pengakuan = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.sumber} - {self.jenis_pengakuan}"

    class Meta:
        verbose_name = "2.D Rekognisi DTPR"
        verbose_name_plural = "2.D Rekognisi DTPR"


# ==========================================
# KRITERIA 3: PENELITIAN & SARPAS
# ==========================================

class Tabel_3A1_Sarana(models.Model):
    nama_prasarana = models.CharField(max_length=255)
    daya_tampung = models.IntegerField(default=0)
    luas_ruang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kepemilikan = models.CharField(max_length=50) # M / W
    lisensi = models.CharField(max_length=50) # L / P / Tidak Berlisensi
    perangkat = models.TextField(blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nama_prasarana

    class Meta:
        verbose_name = "3.A.1 Sarana Penelitian"
        verbose_name_plural = "3.A.1 Sarana Penelitian"

class Tabel_3A2_Penelitian(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    jml_mhs = models.IntegerField(default=0)
    judul = models.TextField()
    jenis_hibah = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama_dtpr} - {self.judul[:50]}"

    class Meta:
        verbose_name = "3.A.2 Kegiatan Penelitian"
        verbose_name_plural = "3.A.2 Kegiatan Penelitian"

class Tabel_3A3_Pengembangan_DTPR(models.Model):
    jenis_pengembangan = models.CharField(max_length=255)
    nama_dosen = models.CharField(max_length=255)
    ts_2 = models.IntegerField(default=0)
    ts_1 = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama_dosen} - {self.jenis_pengembangan}"

    class Meta:
        verbose_name = "3.A.3 Pengembangan DTPR"
        verbose_name_plural = "3.A.3 Pengembangan DTPR"

class Tabel_3C1_Kerjasama(models.Model):
    judul = models.TextField()
    mitra = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.mitra} - {self.judul[:50]}"

    class Meta:
        verbose_name = "3.C.1 Kerjasama Penelitian"
        verbose_name_plural = "3.C.1 Kerjasama Penelitian"

class Tabel_3C2_Publikasi(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    judul = models.TextField()
    jenis_pub = models.CharField(max_length=50)
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama_dtpr} - {self.judul[:50]}"

    class Meta:
        verbose_name = "3.C.2 Publikasi Ilmiah"
        verbose_name_plural = "3.C.2 Publikasi Ilmiah"

class Tabel_3C3_HKI(models.Model):
    judul = models.TextField()
    jenis_hki = models.CharField(max_length=255)
    nama_dtpr = models.CharField(max_length=255)
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.judul[:50]} ({self.jenis_hki})"

    class Meta:
        verbose_name = "3.C.3 HKI Penelitian"
        verbose_name_plural = "3.C.3 HKI Penelitian"

class Tabel_3_Summary(models.Model):
    link_roadmap = models.URLField(blank=True, null=True)
    total_jenis_hibah = models.IntegerField(default=0)
    total_mitra = models.IntegerField(default=0)

    def __str__(self):
        return f"Ringkasan Penelitian (ID: {self.pk})"

    class Meta:
        verbose_name = "3 Ringkasan Penelitian"
        verbose_name_plural = "3 Ringkasan Penelitian"


# ==========================================
# KRITERIA 4: PENGABDIAN KEPADA MASYARAKAT (PkM)
# ==========================================

class Tabel_4A1_Sarana(models.Model):
    nama_prasarana = models.CharField(max_length=255)
    daya_tampung = models.IntegerField(default=0)
    luas_ruang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kepemilikan = models.CharField(max_length=50) # M / W
    lisensi = models.CharField(max_length=50) # L / P / T
    perangkat = models.TextField(blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nama_prasarana

    class Meta:
        verbose_name = "4.A.1 Sarana PkM"
        verbose_name_plural = "4.A.1 Sarana PkM"

class Tabel_4A2_PkM(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    judul = models.TextField()
    jml_mhs = models.IntegerField(default=0)
    jenis_hibah = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama_dtpr} - {self.judul[:50]}"

    class Meta:
        verbose_name = "4.A.2 Kegiatan PkM"
        verbose_name_plural = "4.A.2 Kegiatan PkM"

class Tabel_4C1_Kerjasama(models.Model):
    judul = models.TextField()
    mitra = models.CharField(max_length=255)
    sumber_lni = models.CharField(max_length=10) # L/N/I
    durasi = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    dana_ts2 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts1 = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dana_ts = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.mitra} - {self.judul[:50]}"

    class Meta:
        verbose_name = "4.C.1 Kerjasama PkM"
        verbose_name_plural = "4.C.1 Kerjasama PkM"

class Tabel_4C2_Diseminasi(models.Model):
    nama_dtpr = models.CharField(max_length=255)
    judul = models.TextField()
    lni = models.CharField(max_length=10) # L/N/I
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nama_dtpr} - {self.judul[:50]}"

    class Meta:
        verbose_name = "4.C.2 Diseminasi PkM"
        verbose_name_plural = "4.C.2 Diseminasi PkM"

class Tabel_4C3_HKI(models.Model):
    judul = models.TextField()
    jenis_hki = models.CharField(max_length=255)
    nama_dtpr = models.CharField(max_length=255)
    ts2 = models.BooleanField(default=False)
    ts1 = models.BooleanField(default=False)
    ts = models.BooleanField(default=False)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.judul[:50]} ({self.jenis_hki})"

    class Meta:
        verbose_name = "4.C.3 HKI PkM"
        verbose_name_plural = "4.C.3 HKI PkM"

class Tabel_4_Summary(models.Model):
    link_roadmap = models.URLField(blank=True, null=True)
    total_jenis_hibah = models.IntegerField(default=0)
    jml_disem_hasil = models.IntegerField(default=0)

    def __str__(self):
        return f"Ringkasan PkM (ID: {self.pk})"

    class Meta:
        verbose_name = "4 Ringkasan PkM"
        verbose_name_plural = "4 Ringkasan PkM"


# ==========================================
# KRITERIA 5: AKUNTABILITAS (TATA KELOLA & SARPAS)
# ==========================================

class Tabel_5_1_TataKelola(models.Model):
    jenis_tata_kelola = models.CharField(max_length=255)
    nama_sistem = models.CharField(max_length=255, blank=True, null=True)
    akses = models.CharField(max_length=50, blank=True, null=True) # Internet / Lokal
    unit_pengelola = models.CharField(max_length=255, blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.jenis_tata_kelola} - {self.nama_sistem or '-'}"

    class Meta:
        verbose_name = "5.1 Tata Kelola & SI"
        verbose_name_plural = "5.1 Tata Kelola & SI"

class Tabel_5_2_Sarana(models.Model):
    nama_prasarana = models.CharField(max_length=255)
    daya_tampung = models.IntegerField(default=0)
    luas_ruang = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    kepemilikan = models.CharField(max_length=50) # M / W
    lisensi = models.CharField(max_length=50) # L / P / Tidak berlisensi
    perangkat = models.TextField(blank=True, null=True)
    link_bukti = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nama_prasarana

    class Meta:
        verbose_name = "5.2 Sarana Pendidikan"
        verbose_name_plural = "5.2 Sarana Pendidikan"


# ==========================================
# KRITERIA 6: VISI MISI
# ==========================================

class Tabel_6_Misi(models.Model):
    visi_pt = models.TextField(blank=True, null=True)
    visi_upps = models.TextField(blank=True, null=True)
    visi_ps = models.TextField(blank=True, null=True)
    misi_pt = models.TextField(blank=True, null=True)
    misi_upps = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visi & Misi (ID: {self.pk})"

    class Meta:
        verbose_name = "6 Visi & Misi"
        verbose_name_plural = "6 Visi & Misi"
