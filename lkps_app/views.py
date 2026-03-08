from django.shortcuts import render, redirect

# ==========================================
# AUTH & MASTER DATA
# ==========================================
def login(request):
    return render(request, 'lkps_app/login.html')

def halaman_logout(request):
    return redirect('login')

def dashboard(request):
    return render(request, 'lkps_app/dashboard.html')

def sampul(request):
    return render(request, 'lkps_app/sampul.html')

def program_studi(request):
    return render(request, 'lkps_app/program_studi.html')

def manajemen_user(request):
    return render(request, 'lkps_app/manajemen_user.html')

# ==========================================
# KRITERIA 1: TATA PAMONG & KERJASAMA
# ==========================================
def tabel_1a1(request):
    return render(request, 'lkps_app/tabel_1a1.html')

def tabel_1a_dana(request):
    return render(request, 'lkps_app/tabel_1a_dana.html')

def tabel_1a4(request):
    return render(request, 'lkps_app/tabel_1a4.html')

def tabel_1a5(request):
    return render(request, 'lkps_app/tabel_1a5.html')

# ==========================================
# KRITERIA 2: MAHASISWA & LULUSAN
# ==========================================
def tabel_2a_mahasiswa(request):
    return render(request, 'lkps_app/tabel_2a_mahasiswa.html')

def tabel_2b_kurikulum(request):
    return render(request, 'lkps_app/tabel_2b_kurikulum.html')

def tabel_2b_lulusan(request):
    return render(request, 'lkps_app/tabel_2b_lulusan.html')

# ==========================================
# KRITERIA 3 - 6: PENELITIAN, PKM, MISI
# ==========================================
def tabel_3_penelitian(request):
    return render(request, 'lkps_app/tabel_3_penelitian.html')

def tabel_4_pkm(request):
    return render(request, 'lkps_app/tabel_4_pkm.html')

def tabel_5_akuntabilitas(request):
    return render(request, 'lkps_app/tabel_5_akuntabilitas.html')

def tabel_6_misi(request):
    return render(request, 'lkps_app/tabel_6_misi.html')