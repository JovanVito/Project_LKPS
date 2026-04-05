import json
from django.conf import settings
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError 
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
from .models import (
    IdentitasPengusul, TimPenyusun, ProgramStudi, ProfilPengguna,
    Tabel_1A1, Tabel_1A2_Sumber, Tabel_1A3_Penggunaan, Tabel_1A4, Tabel_1A5,
    Tabel_2A_Mahasiswa, Tabel_2A2_Asal, Tabel_2A3_Kondisi, 
    Tabel_2B1_MK, Tabel_2B2_CPL, Tabel_2B3_Pemenuhan, Tabel_2B4_MasaTunggu, Tabel_2B5_BidangKerja, Tabel_2B6_Kepuasan, Tabel_2B_Summary,
    Tabel_3_Summary,Tabel_3A1_Sarana,Tabel_3A2_Penelitian,Tabel_3C1_Kerjasama,Tabel_3C2_Publikasi,Tabel_3C3_HKI, 
    Tabel_4A1_Sarana, Tabel_4A2_PkM, Tabel_4C1_Kerjasama, Tabel_4C2_Diseminasi, Tabel_4C3_HKI, Tabel_4_Summary, Tabel_5_1_TataKelola, Tabel_5_2_Sarana, Tabel_6_Misi
)

#Export ke Docx
def export_lkps_word(request):
    try:
        # PENGGUNAAN PATH MODERN
        template_path = str(settings.BASE_DIR / 'static' / 'lkps_app' / 'word_templates' / 'Master_Format_LKPS.docx')
        
        # Buka template Word
        doc = DocxTemplate(template_path)

        # Ambil data identitas terpisah agar bisa kita cek logonya
        identitas_data = IdentitasPengusul.objects.first()

        # 3. Bungkus semua data agar bisa dibaca oleh file Word
        context = {
            'identitas': identitas_data or {},
            'tim_penyusun': TimPenyusun.objects.all(),
            # Kriteria 1
            't1a1': Tabel_1A1.objects.all(),
            't1a2': Tabel_1A2_Sumber.objects.all(),
            't1a3': Tabel_1A3_Penggunaan.objects.all(),
            't1a4': Tabel_1A4.objects.all(),
            't1a5': Tabel_1A5.objects.all(),
            # Kriteria 2
            't2a1': Tabel_2A_Mahasiswa.objects.all().order_by('id'),
            't2a2': Tabel_2A2_Asal.objects.all().order_by('id'),
            't2a3': Tabel_2A3_Kondisi.objects.all().order_by('id'),
            't2b1': Tabel_2B1_MK.objects.all(),
            't2b2': Tabel_2B2_CPL.objects.all(),
            't2b3': Tabel_2B3_Pemenuhan.objects.all(),
            't2b4': Tabel_2B4_MasaTunggu.objects.all().order_by('id'),
            't2b5': Tabel_2B5_BidangKerja.objects.all().order_by('id'),
            't2b6': Tabel_2B6_Kepuasan.objects.all(),
            'sum2': Tabel_2B_Summary.objects.first(),
            # Kriteria 3
            't3a1': Tabel_3A1_Sarana.objects.all(),
            't3a2': Tabel_3A2_Penelitian.objects.all(),
            't3c1': Tabel_3C1_Kerjasama.objects.all(),
            't3c2': Tabel_3C2_Publikasi.objects.all(),
            't3c3': Tabel_3C3_HKI.objects.all(),
            'sum3': Tabel_3_Summary.objects.first(),
            # Kriteria 4
            't4a1': Tabel_4A1_Sarana.objects.all(),
            't4a2': Tabel_4A2_PkM.objects.all(),
            't4c1': Tabel_4C1_Kerjasama.objects.all(),
            't4c2': Tabel_4C2_Diseminasi.objects.all(),
            't4c3': Tabel_4C3_HKI.objects.all(),
            'sum4': Tabel_4_Summary.objects.first(),
            # Kriteria 5 & 6
            't5_1': Tabel_5_1_TataKelola.objects.all(),
            't5_2': Tabel_5_2_Sarana.objects.all(),
            't6': Tabel_6_Misi.objects.first(),
        }
        
        # --- LOGIKA KHUSUS UNTUK MEMUNCULKAN LOGO GAMBAR ---
        if identitas_data and identitas_data.logo_pt:
            try:
                # Ambil path fisik dari file gambar di komputermu
                image_path = identitas_data.logo_pt.path 
                
                # Ubah menjadi objek gambar Word dengan lebar 40 mm (silakan sesuaikan ukurannya)
                # Kemudian masukkan ke variabel 'logo' (sesuai dengan tag {{ logo }} di template Word)
                context['logo'] = InlineImage(doc, image_path, width=Mm(40))
            except Exception as e:
                print(f"Gagal memuat gambar logo: {e}")
                context['logo'] = '' # Kosongkan jika gambar tidak ditemukan di folder
        else:
            context['logo'] = '' # Kosongkan jika user belum mengupload logo
        # ---------------------------------------------------

        # 4. SUNTIKKAN DATA KE DALAM WORD
        doc.render(context)

        # 5. Siapkan file untuk langsung di-download oleh Browser User
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="Dokumen_LKPS_Final.docx"'
        
        doc.save(response)
        return response

    except Exception as e:
        return HttpResponse(f"Gagal mencetak dokumen: {str(e)}", status=500)
    
# Konfigurasi API Key (Pastikan API Key kamu sudah benar dimasukkan di sini)
GEMINI_API_KEY = "AIzaSyBNTztqmQ978wn3w9f13r04pw3_Nd2ffvg"
genai.configure(api_key=GEMINI_API_KEY)

def chatbot_api(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_message = request.POST.get('message', '')
        
        if not user_message:
            return JsonResponse({'status': 'error', 'message': 'Pesan kosong'})

        try:
            # Kita coba nama resmi versi 1.5 tanpa embel-embel 'latest'
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            system_instruction = """
            Kamu adalah "Leksi", Asisten AI ramah untuk Sistem Borang Akreditasi LKPS di Pradita University. 
            Tugasmu adalah memandu pengguna (seperti Admin Prodi Informatika) yang kebingungan saat mengisi data di aplikasi ini.
            
            Jawablah berdasarkan struktur menu dan tabel yang ADA di aplikasi ini saja:
            
            1. Identitas Laporan: Mengisi data institusi, SK pendirian, dan daftar Tim Penyusun.
            2. Kriteria 1 (Budaya Mutu):
               - Tabel 1.A.1: Pimpinan unit kerja & Tupoksi.
               - Tabel 1.A.2 & 1.A.3: Sumber dan Penggunaan Dana (TS-2 s/d TS).
               - Tabel 1.A.4: Beban Kerja DTPR (SKS pengajaran, penelitian, PkM, tambahan).
               - Tabel 1.A.5: Kualifikasi Tenaga Kependidikan (Tendik) berdasarkan ijazah (S3 sampai SMA).
            3. Kriteria 2 (Pendidikan):
               - Tabel 2.A.1: Data Mahasiswa (Daya tampung, pendaftar, lulus seleksi, mahasiswa baru, dan mahasiswa aktif).
               - Tabel 2.A.2: Keragaman Asal Mahasiswa.
               - Tabel 2.A.3: Kondisi Jumlah Mahasiswa (Aktif, Lulus, DO).
               - Tabel 2.B: Kurikulum (Mata Kuliah & SKS) dan Data Lulusan (IPK, Masa Studi).
            4. Kriteria 3 (Penelitian): Pembiayaan penelitian DTPR.
            5. Kriteria 4 (PkM): Pembiayaan Pengabdian kepada Masyarakat DTPR.
            6. Kriteria 5 (Akuntabilitas): Uraian aspek akuntabilitas.
            7. Kriteria 6 (Misi): Visi, Misi, dan Tujuan program studi.

            Info Penting Aplikasi:
            - Aplikasi ini sudah dilengkapi fitur "Autosave" (Simpan Otomatis). Jika pengguna bertanya cara menyimpan, beritahu bahwa mereka cukup mengetik dan data akan tersimpan otomatis ke cloud dalam 1 detik.
            
            Aturan Menjawab:
            - Jawab dengan santai, sopan, dan sangat ringkas. 
            - Gunakan poin-poin (bullet points) agar mudah dibaca.
            - JANGAN mengarang nama tabel yang tidak disebutkan di atas.
            """
            
            prompt = f"{system_instruction}\n\nPertanyaan: {user_message}"
            response = model.generate_content(prompt)
            
            return JsonResponse({'status': 'success', 'reply': response.text})
            
        except Exception as e:
            # LOGIKA DETEKTIF: Jika masih error, kita suruh Python melacak model yang tersedia
            print("\n" + "="*50)
            print("MENCARI MODEL YANG TERSEDIA DI API KEY KAMU...")
            try:
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                print(f"DAFTAR MODEL YANG BISA DIPAKAI: {available_models}")
                print("="*50 + "\n")
                pesan_error = f"Model tidak cocok. Coba lihat terminal VS Code kamu untuk copy-paste nama model yang benar!"
            except Exception as ex:
                pesan_error = f"Error melacak model: {str(ex)}"
                
            return JsonResponse({'status': 'error', 'message': pesan_error})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
# ==========================================
# AUTH & NAVIGATION
# ==========================================
def db_explorer(request):
    query = request.POST.get('q', '') or request.GET.get('q', '')
    results = []
    headers = []
    error = None

    if query:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                if cursor.description:
                    headers = [col[0] for col in cursor.description]
                    results = cursor.fetchall()
                else:
                    results = [["Query executed successfully (no rows returned)."]]
        except Exception as e:
            error = str(e)

    table_schemas = {}
    filtered_table_names = []  # <-- TAMBAHAN: Tempat menyimpan tabel yang sudah disaring

    with connection.cursor() as cursor:
        all_table_names = connection.introspection.table_names()
        
        for t_name in all_table_names:
            # --- FILTERING LOGIC ---
            # Hanya ambil tabel yang namanya diawali dengan 'lkps_app_'
            # Jika kamu juga ingin menyembunyikan ProfilPengguna, gunakan kode ini:
            # if t_name.startswith('lkps_app_') and t_name != 'lkps_app_profilpengguna':
            
            if t_name.startswith('lkps_app_'):
                filtered_table_names.append(t_name) # Masukkan ke daftar aman
                try:
                    # Ambil deskripsi struktur kolom untuk tiap tabel
                    desc = connection.introspection.get_table_description(cursor, t_name)
                    # Ambil nama kolomnya saja (contoh: 'id', 'nama_prodi', dll)
                    columns = [col.name for col in desc]
                    table_schemas[t_name] = columns
                except Exception:
                    table_schemas[t_name] = []

    return render(request, 'lkps_app/db_explorer.html', {
        'query': query,
        'results': results,
        'headers': headers,
        'error': error,
        'tables': sorted(filtered_table_names), # <-- UBAH: Gunakan daftar yang sudah disaring
        # Kirim peta kolom ke HTML dalam format JSON agar bisa dibaca JavaScript
        'table_schemas_json': json.dumps(table_schemas) 
    })

def login_view(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')
        user = authenticate(request, username=user_name, password=pass_word)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username atau Password salah!")
    return render(request, 'lkps_app/login.html')

def halaman_logout(request):
    auth_logout(request)
    return redirect('login')

def dashboard(request):
    return render(request, 'lkps_app/dashboard.html')

def sampul(request):
    # 1. CEK PROGRAM STUDI (SOLUSI ERROR NOT NULL)
    prodi_default = ProgramStudi.objects.first()
    if not prodi_default:
        prodi_default = ProgramStudi.objects.create(nama_prodi="Prodi Informatika", jenjang_studi="S1", akreditasi="Baik", no_sk="-")

    # 2. AMBIL/BUAT DATA IDENTITAS DENGAN DEFAULT PRODI
    identitas, created = IdentitasPengusul.objects.get_or_create(
        id=1, 
        defaults={'program_studi': prodi_default}
    )

    # 3. LOGIKA AUTOSAVE (POST)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Mapping sudah disesuaikan persis dengan field di models.py
        mapping = {
            'sampul_nama_ps': 'nama_ps_sampul',
            'sampul_nama_pt': 'nama_pt_sampul',
            'sampul_kota': 'kota_sampul',
            'sampul_tahun': 'tahun_sampul',
            'pengusul_pt': 'perguruan_tinggi',
            'pengusul_upps': 'unit_pengelola',
            'pengusul_alamat': 'alamat',
            'pengusul_telepon': 'telepon',
            'pengusul_email_web': 'email_web',
            'pengusul_sk_pt': 'sk_pt',               # DIKOREKSI
            'pengusul_tgl_sk_pt': 'tgl_sk_pt',       # DITAMBAHKAN
            'pengusul_sk_ps': 'sk_ps',               # DIKOREKSI
            'pengusul_tgl_sk_ps': 'tgl_sk_ps',       # DITAMBAHKAN
            
            # CATATAN: Jika 'jenis_program', 'nama_ps', 'pejabat_sk_pt' 
            # benar-benar ada di models.py kamu yang terbaru, silakan ditambahkan lagi ke sini.
        }

        # Update field utama berdasarkan mapping
        for html_name, model_field in mapping.items():
            if html_name in request.POST:
                val = request.POST.get(html_name)
                
                # HANYA ubah ke None jika field-nya adalah Tanggal atau Angka
                # Jika ada field tanggal/angka lain, tambahkan ke dalam list ini
                date_and_int_fields = ['tahun_sampul', 'tgl_sk_pt', 'tgl_sk_ps', 'tahun_mhs_pertama']
                
                if model_field in date_and_int_fields and val == "":
                    val = None
                elif val is None:
                    # Pastikan field teks yang tidak terkirim tetap berupa string kosong
                    val = ""
                    
                setattr(identitas, model_field, val)
        
        # Handle Logo PT jika ada upload
        if 'logo_pt' in request.FILES:
            identitas.logo_pt = request.FILES['logo_pt']
            print(f"File diterima: {request.FILES['logo_pt'].name}")
            
        # WAJIB DI SINI: Simpan semua perubahan teks & logo ke database
        identitas.save() 

        # 4. LOGIKA TIM PENYUSUN (Multi-row)
        namas = request.POST.getlist('penyusun_nama[]')
        nidns = request.POST.getlist('penyusun_nidn[]')
        jabatans = request.POST.getlist('penyusun_jabatan[]')
        tanggals = request.POST.getlist('penyusun_tanggal[]')

        # Hapus data lama dan simpan yang terbaru dari tabel
        identitas.tim_penyusun.all().delete()
        for i in range(len(namas)):
            nama_clean = namas[i].strip() if namas[i] else ""
            
            if nama_clean: 
                TimPenyusun.objects.create(
                    identitas=identitas,
                    nama=nama_clean,
                    nidn=nidns[i] if i < len(nidns) else "",
                    jabatan=jabatans[i] if i < len(jabatans) else "",
                    tanggal_pengisian=tanggals[i] if (i < len(tanggals) and tanggals[i]) else None
                )

        return JsonResponse({'status': 'success'})

    # 5. TAMPILKAN HALAMAN (GET)
    return render(request, 'lkps_app/sampul.html', {
        'data': identitas,
        'tim_penyusun': identitas.tim_penyusun.all()
    })

def program_studi(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # 1. TANGKAP DATA DARI FORM HTML (berdasarkan atribut 'name')
            input_nama = request.POST.get('nama_prodi')
            input_jenjang = request.POST.get('jenjang_prodi')
            input_akreditasi = request.POST.get('status_akreditasi')
            input_sk = request.POST.get('sk_banpt')
            
            # 2. SIMPAN KE DATABASE (Mapping persis dengan nama di models.py)
            ProgramStudi.objects.create(
                nama_prodi = input_nama,
                jenjang_studi = input_jenjang,
                akreditasi = input_akreditasi,
                no_sk = input_sk       
            )
            
            # 3. KIRIM BALASAN SUKSES KE JAVASCRIPT
            return JsonResponse({'status': 'success', 'message': 'Data berhasil disimpan!'})
            
        except Exception as e:
            # KIRIM BALASAN ERROR JIKA GAGAL (Misal: nama prodi sudah ada / duplicate unique)
            return JsonResponse({'status': 'error', 'message': str(e)})


    daftar_prodi = ProgramStudi.objects.all().order_by('id')
    
    return render(request, 'lkps_app/program_studi.html', {
        'daftar_prodi': daftar_prodi
    })

def manajemen_user(request):
    # JIKA ADA REQUEST SIMPAN DATA (DARI JAVASCRIPT / AJAX)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            input_nama = request.POST.get('nama_lengkap')
            input_nidn = request.POST.get('nomor_induk')
            input_email = request.POST.get('email')
            input_password = request.POST.get('password')
            input_role = request.POST.get('role')
            input_prodi = request.POST.get('akses_prodi')

            # 1. Buat Akun Utama (Email & Password akan di-enkripsi otomatis oleh Django)
            user_baru = User.objects.create_user(
                username=input_email, # Kita jadikan email sebagai username login
                email=input_email,
                password=input_password,
                first_name=input_nama # Kita simpan nama lengkap di first_name
            )

            # 2. Buat Profil Tambahannya (NIDN, Role, Prodi)
            ProfilPengguna.objects.create(
                user=user_baru,
                nomor_induk=input_nidn,
                role=input_role,
                akses_prodi=input_prodi
            )

            return JsonResponse({'status': 'success', 'message': 'Akun berhasil dibuat!'})

        except IntegrityError:
            # Error ini muncul jika ada yang mendaftar dengan email yang sama
            return JsonResponse({'status': 'error', 'message': f'Email {input_email} sudah digunakan!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # JIKA HALAMAN HANYA DIBUKA (GET REQUEST)
    # Kita ambil semua profil, lalu bungkus menjadi format yang siap dibaca oleh HTML
    daftar_pengguna = []
    semua_profil = ProfilPengguna.objects.select_related('user').all()
    
    for profil in semua_profil:
        daftar_pengguna.append({
            'nama_lengkap': profil.user.first_name,
            'email': profil.user.email,
            'nomor_induk': profil.nomor_induk,
            'role': profil.role,
            'akses_prodi': profil.akses_prodi,
            'is_active': profil.user.is_active
        })

    return render(request, 'lkps_app/manajemen_user.html', {
        'daftar_pengguna': daftar_pengguna
    })

# ==========================================
# KRITERIA 1: TATA PAMONG & KERJASAMA
# ==========================================

def tabel_1a1(request):
    """View untuk Tabel 1.A.1 Pimpinan & Tupoksi"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        unit = request.POST.getlist('unit_kerja[]')
        nama = request.POST.getlist('nama_ketua[]')
        periode = request.POST.getlist('periode_jabatan[]')
        pendidikan = request.POST.getlist('pendidikan_terakhir[]')
        jabatan = request.POST.getlist('jabatan_fungsional[]')
        tupoksi = request.POST.getlist('tupoksi[]')

        try:
            with transaction.atomic():
                Tabel_1A1.objects.all().delete()
                for i in range(len(unit)):
                    if unit[i].strip():
                        Tabel_1A1.objects.create(
                            unit_kerja=unit[i], nama_ketua=nama[i],
                            periode_jabatan=periode[i], pendidikan_terakhir=pendidikan[i],
                            jabatan_fungsional=jabatan[i], tupoksi=tupoksi[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    data = Tabel_1A1.objects.all().order_by('id')
    return render(request, 'lkps_app/tabel_1a1.html', {'data': data})

def tabel_1a_dana(request):
    """View untuk Tabel 1.A.2 & 1.A.3 (Sumber & Penggunaan)"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        s_dana = request.POST.getlist('sumber_dana[]')
        s_ts2 = request.POST.getlist('sumber_ts2[]')
        s_ts1 = request.POST.getlist('sumber_ts1[]')
        s_ts = request.POST.getlist('sumber_ts[]')
        s_link = request.POST.getlist('link_sumber[]')

        g_dana = request.POST.getlist('guna_dana[]')
        g_ts2 = request.POST.getlist('guna_ts2[]')
        g_ts1 = request.POST.getlist('guna_ts1[]')
        g_ts = request.POST.getlist('guna_ts[]')
        g_link = request.POST.getlist('link_guna[]')

        try:
            with transaction.atomic():
                Tabel_1A2_Sumber.objects.all().delete()
                for i in range(len(s_dana)):
                    if s_dana[i].strip():
                        Tabel_1A2_Sumber.objects.create(
                            sumber_dana=s_dana[i], ts_2=s_ts2[i] or 0,
                            ts_1=s_ts1[i] or 0, ts=s_ts[i] or 0, link_bukti=s_link[i]
                        )
                Tabel_1A3_Penggunaan.objects.all().delete()
                for i in range(len(g_dana)):
                    if g_dana[i].strip():
                        Tabel_1A3_Penggunaan.objects.create(
                            penggunaan=g_dana[i], ts_2=g_ts2[i] or 0,
                            ts_1=g_ts1[i] or 0, ts=g_ts[i] or 0, link_bukti=g_link[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    ctx = {
        'data_sumber': Tabel_1A2_Sumber.objects.all().order_by('id'),
        'data_penggunaan': Tabel_1A3_Penggunaan.objects.all().order_by('id')
    }
    return render(request, 'lkps_app/tabel_1a_dana.html', ctx)

def tabel_1a4(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        nama = request.POST.getlist('nama_dtpr[]')
        ps_s = request.POST.getlist('sks_pengajaran_ps_sendiri[]')
        ps_l = request.POST.getlist('sks_pengajaran_ps_lain[]')
        pt_l = request.POST.getlist('sks_pengajaran_pt_lain[]')
        pen = request.POST.getlist('sks_penelitian[]')
        pkm = request.POST.getlist('sks_pengabdian[]')
        m_s = request.POST.getlist('sks_manajemen_pt_sendiri[]')
        m_l = request.POST.getlist('sks_manajemen_pt_lain[]')

        try:
            with transaction.atomic():
                Tabel_1A4.objects.all().delete()
                for i in range(len(nama)):
                    if nama[i].strip():
                        # Konversi ke float untuk menghindari error string
                        Tabel_1A4.objects.create(
                            nama_dosen=nama[i],
                            sks_ps_sendiri=float(ps_s[i] or 0),
                            sks_ps_lain=float(ps_l[i] or 0),
                            sks_pt_lain=float(pt_l[i] or 0),
                            sks_penelitian=float(pen[i] or 0),
                            sks_pkm=float(pkm[i] or 0),
                            sks_tambahan=float(m_s[i] or 0) + float(m_l[i] or 0)
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'lkps_app/tabel_1a4.html', {'data': Tabel_1A4.objects.all()})
def tabel_1a5(request):
    """View untuk Tabel 1.A.5 Tenaga Kependidikan"""
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        jenis = request.POST.getlist('jenis_tendik[]')
        s3 = request.POST.getlist('jml_s3[]')
        s2 = request.POST.getlist('jml_s2[]')
        s1 = request.POST.getlist('jml_s1[]')
        d4 = request.POST.getlist('jml_d4[]')
        d3 = request.POST.getlist('jml_d3[]')
        d2 = request.POST.getlist('jml_d2[]')
        d1 = request.POST.getlist('jml_d1[]')
        sma = request.POST.getlist('jml_sma[]')
        unit = request.POST.getlist('unit_kerja[]')

        try:
            with transaction.atomic():
                Tabel_1A5.objects.all().delete()
                for i in range(len(jenis)):
                    if jenis[i].strip():
                        # WAJIB: Gunakan int() agar tidak terjadi error concate string
                        Tabel_1A5.objects.create(
                            jenis_tenaga=jenis[i], 
                            s3=int(s3[i] or 0), 
                            s2=int(s2[i] or 0),
                            # S1 dan D4 digabung sesuai struktur models.py kamu
                            s1=int(s1[i] or 0) + int(d4[i] or 0), 
                            d3=int(d3[i] or 0),
                            # D2 dan D1 digabung
                            d2_d1=int(d2[i] or 0) + int(d1[i] or 0),
                            sma_smk=int(sma[i] or 0), 
                            unit_kerja=unit[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return render(request, 'lkps_app/tabel_1a5.html', {'data': Tabel_1A5.objects.all()})

# ==========================================
# KRITERIA 2: MAHASISWA & LULUSAN
# ==========================================

def tabel_2a_mahasiswa(request):
    # --- PRE-SEEDING UNTUK 3 TABEL AGAR SELALU ADA DI DATABASE ---
    for y in ['TS-3', 'TS-2', 'TS-1', 'TS']:
        Tabel_2A_Mahasiswa.objects.get_or_create(tahun_akademik=y)
    
    kategori_asal = ["Kota/Kab sama dengan PS", "Kota/Kabupaten Lain", "Provinsi Lain", "Negara Lain", "Afirmasi", "Berkebutuhan Khusus"]
    for asal in kategori_asal:
        Tabel_2A2_Asal.objects.get_or_create(asal_mahasiswa=asal)
        
    kategori_kondisi = ["Mahasiswa Aktif pada saat TS", "Lulus pada saat TS", "Mengundurkan Diri/DO pada saat TS"]
    for kondisi in kategori_kondisi:
        Tabel_2A3_Kondisi.objects.get_or_create(status=kondisi)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                # --- UPDATE 2.A.1 ---
                thn = request.POST.getlist('tahun_akademik[]')
                daya = request.POST.getlist('daya_tampung[]')
                p_reg = request.POST.getlist('pendaftar_reg[]')
                p_afi = request.POST.getlist('pendaftar_afi[]')
                p_khu = request.POST.getlist('pendaftar_khu[]')
                l_reg = request.POST.getlist('lulus_reg[]')
                l_afi = request.POST.getlist('lulus_afi[]')
                l_khu = request.POST.getlist('lulus_khu[]')
                l_rpl = request.POST.getlist('lulus_rpl[]')
                m_reg = request.POST.getlist('maba_reg[]')
                m_afi = request.POST.getlist('maba_afi[]')
                m_khu = request.POST.getlist('maba_khu[]')
                m_rpl = request.POST.getlist('maba_rpl[]')
                a_reg = request.POST.getlist('aktif_reg[]')
                a_afi = request.POST.getlist('aktif_afi[]')
                a_khu = request.POST.getlist('aktif_khu[]')
                a_rpl = request.POST.getlist('aktif_rpl[]')

                for i in range(len(thn)):
                    obj = Tabel_2A_Mahasiswa.objects.get(tahun_akademik=thn[i])
                    obj.daya_tampung = int(daya[i] or 0)
                    obj.pendaftar = int(p_reg[i] or 0) + int(p_afi[i] or 0) + int(p_khu[i] or 0)
                    obj.lulus_seleksi = int(l_reg[i] or 0) + int(l_afi[i] or 0) + int(l_khu[i] or 0) + int(l_rpl[i] or 0)
                    obj.mhs_baru_reguler = int(m_reg[i] or 0) + int(m_afi[i] or 0) + int(m_khu[i] or 0)
                    obj.mhs_baru_transfer = int(m_rpl[i] or 0)
                    obj.total_mhs_reguler = int(a_reg[i] or 0) + int(a_afi[i] or 0) + int(a_khu[i] or 0)
                    obj.total_mhs_transfer = int(a_rpl[i] or 0)
                    obj.save()

                # --- UPDATE 2.A.2 ---
                kat_asal = request.POST.getlist('asal_kategori[]')
                asal_ts2 = request.POST.getlist('asal_ts2[]')
                asal_ts1 = request.POST.getlist('asal_ts1[]')
                asal_ts = request.POST.getlist('asal_ts[]')
                link_asal = request.POST.getlist('link_asal[]')

                for i in range(len(kat_asal)):
                    obj_asal = Tabel_2A2_Asal.objects.get(asal_mahasiswa=kat_asal[i])
                    obj_asal.ts_2 = int(asal_ts2[i] or 0)
                    obj_asal.ts_1 = int(asal_ts1[i] or 0)
                    obj_asal.ts = int(asal_ts[i] or 0)
                    obj_asal.link_bukti = link_asal[i]
                    obj_asal.save()

                # --- UPDATE 2.A.3 ---
                kat_kon = request.POST.getlist('kondisi_kategori[]')
                kon_ts2 = request.POST.getlist('kondisi_ts2[]')
                kon_ts1 = request.POST.getlist('kondisi_ts1[]')
                kon_ts = request.POST.getlist('kondisi_ts[]')

                for i in range(len(kat_kon)):
                    obj_kon = Tabel_2A3_Kondisi.objects.get(status=kat_kon[i])
                    obj_kon.ts_2 = int(kon_ts2[i] or 0)
                    obj_kon.ts_1 = int(kon_ts1[i] or 0)
                    obj_kon.ts = int(kon_ts[i] or 0)
                    obj_kon.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # Render data ke template
    return render(request, 'lkps_app/tabel_2a_mahasiswa.html', {
        'data_2a1': Tabel_2A_Mahasiswa.objects.all().order_by('id'),
        'data_2a2': Tabel_2A2_Asal.objects.all().order_by('id'),
        'data_2a3': Tabel_2A3_Kondisi.objects.all().order_by('id')
    })


def tabel_2b_kurikulum(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                # --- PROSES TABEL 2.B.1 (MK & PL) ---
                Tabel_2B1_MK.objects.all().delete()
                mk_nama = request.POST.getlist('nama_mk[]')
                mk_sks = request.POST.getlist('sks_mk[]')
                mk_smt = request.POST.getlist('smt_mk[]')
                # Trik Hidden Input: Data checkbox sekarang pasti konsisten panjangnya
                mk_pl1 = request.POST.getlist('pl1[]')
                mk_pl2 = request.POST.getlist('pl2[]')
                mk_pl3 = request.POST.getlist('pl3[]')
                mk_pl4 = request.POST.getlist('pl4[]')

                for i in range(len(mk_nama)):
                    if mk_nama[i].strip():
                        Tabel_2B1_MK.objects.create(
                            nama_mk=mk_nama[i],
                            sks=int(mk_sks[i] or 0),
                            semester=int(mk_smt[i] or 0),
                            pl1=(mk_pl1[i] == '1'),
                            pl2=(mk_pl2[i] == '1'),
                            pl3=(mk_pl3[i] == '1'),
                            pl4=(mk_pl4[i] == '1')
                        )

                # --- PROSES TABEL 2.B.2 (CPL) ---
                Tabel_2B2_CPL.objects.all().delete()
                cpl_kode = request.POST.getlist('kode_cpl[]')
                cpl_pl1 = request.POST.getlist('map_pl1[]')
                cpl_pl2 = request.POST.getlist('map_pl2[]')
                cpl_pl3 = request.POST.getlist('map_pl3[]')
                cpl_pl4 = request.POST.getlist('map_pl4[]')

                for i in range(len(cpl_kode)):
                    if cpl_kode[i].strip():
                        Tabel_2B2_CPL.objects.create(
                            kode_cpl=cpl_kode[i],
                            pl1=(cpl_pl1[i] == '1'),
                            pl2=(cpl_pl2[i] == '1'),
                            pl3=(cpl_pl3[i] == '1'),
                            pl4=(cpl_pl4[i] == '1')
                        )

                # --- PROSES TABEL 2.B.3 (PEMENUHAN) ---
                Tabel_2B3_Pemenuhan.objects.all().delete()
                pem_cpl = request.POST.getlist('pem_cpl[]')
                pem_cpmk = request.POST.getlist('pem_cpmk[]')
                pem_smt1 = request.POST.getlist('pem_smt1[]')
                pem_smt2 = request.POST.getlist('pem_smt2[]')
                pem_smt3 = request.POST.getlist('pem_smt3[]')

                for i in range(len(pem_cpl)):
                    if pem_cpl[i].strip() or pem_cpmk[i].strip():
                        Tabel_2B3_Pemenuhan.objects.create(
                            cpl=pem_cpl[i],
                            cpmk=pem_cpmk[i],
                            smt1=pem_smt1[i],
                            smt2=pem_smt2[i],
                            smt3=pem_smt3[i]
                        )
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # GET: Tampilkan data ke HTML
    ctx = {
        'data_mk': Tabel_2B1_MK.objects.all(),
        'data_cpl': Tabel_2B2_CPL.objects.all(),
        'data_pemenuhan': Tabel_2B3_Pemenuhan.objects.all(),
    }
    return render(request, 'lkps_app/tabel_2b_kurikulum.html', ctx)


def tabel_2b_lulusan(request):
    # --- 1. PRE-SEEDING DATA ---
    years = ['TS-2', 'TS-1', 'TS']
    for y in years:
        Tabel_2B4_MasaTunggu.objects.get_or_create(tahun_lulus=y)
        Tabel_2B5_BidangKerja.objects.get_or_create(tahun_lulus=y)

    kemampuans = [
        "Kerjasama Tim", "Keahlian di Bidang Prodi", "Kemampuan Berbahasa Asing (Inggris)", 
        "Kemampuan Berkomunikasi", "Pengembangan Diri", "Kepemimpinan", "Etos Kerja"
    ]
    for k in kemampuans:
        Tabel_2B6_Kepuasan.objects.get_or_create(jenis_kemampuan=k)

    Tabel_2B_Summary.objects.get_or_create(id=1)

    # --- 2. LOGIKA AUTOSAVE ---
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                # Update 2.B.4
                thn4 = request.POST.getlist('tahun_lulus_4[]')
                lul4 = request.POST.getlist('tunggu_lulusan[]')
                ter4 = request.POST.getlist('tunggu_terlacak[]')
                waktu4 = request.POST.getlist('tunggu_bulan[]')
                for i in range(len(thn4)):
                    obj = Tabel_2B4_MasaTunggu.objects.get(tahun_lulus=thn4[i])
                    obj.jml_lulusan = int(lul4[i] or 0)
                    obj.jml_terlacak = int(ter4[i] or 0)
                    obj.waktu_tunggu = float(waktu4[i] or 0)
                    obj.save()

                # Update 2.B.5
                thn5 = request.POST.getlist('tahun_lulus_5[]')
                lul5 = request.POST.getlist('bidang_lulusan[]')
                ter5 = request.POST.getlist('bidang_terlacak[]')
                info = request.POST.getlist('bidang_info[]')
                non = request.POST.getlist('bidang_non[]')
                multi = request.POST.getlist('bidang_multi[]')
                nas = request.POST.getlist('bidang_nas[]')
                wira = request.POST.getlist('bidang_wira[]')
                for i in range(len(thn5)):
                    obj = Tabel_2B5_BidangKerja.objects.get(tahun_lulus=thn5[i])
                    obj.jml_lulusan = int(lul5[i] or 0)
                    obj.jml_terlacak = int(ter5[i] or 0)
                    obj.bidang_infokom = int(info[i] or 0)
                    obj.bidang_non_infokom = int(non[i] or 0)
                    obj.tingkat_multinasional = int(multi[i] or 0)
                    obj.tingkat_nasional = int(nas[i] or 0)
                    obj.tingkat_wirausaha = int(wira[i] or 0)
                    obj.save()

                # Update 2.B.6
                kemampuan = request.POST.getlist('kemampuan[]')
                sb = request.POST.getlist('kepuasan_sb[]')
                b = request.POST.getlist('kepuasan_b[]')
                c = request.POST.getlist('kepuasan_c[]')
                k = request.POST.getlist('kepuasan_k[]')
                tl = request.POST.getlist('tindak_lanjut[]')
                for i in range(len(kemampuan)):
                    obj = Tabel_2B6_Kepuasan.objects.get(jenis_kemampuan=kemampuan[i])
                    obj.sangat_baik = float(sb[i] or 0)
                    obj.baik = float(b[i] or 0)
                    obj.cukup = float(c[i] or 0)
                    obj.kurang = float(k[i] or 0)
                    obj.tindak_lanjut = tl[i]
                    obj.save()

                # Update Summary
                summary = Tabel_2B_Summary.objects.get(id=1)
                summary.total_alumni_3thn = int(request.POST.get('total_alumni_3thn') or 0)
                summary.total_responden = int(request.POST.get('total_responden') or 0)
                summary.total_mhs_aktif_ts = int(request.POST.get('total_mhs_aktif_ts') or 0)
                summary.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # --- 3. GET DATA UNTUK HTML ---
    ctx = {
        'data_2b4': Tabel_2B4_MasaTunggu.objects.all().order_by('id'),
        'data_2b5': Tabel_2B5_BidangKerja.objects.all().order_by('id'),
        'data_2b6': Tabel_2B6_Kepuasan.objects.all().order_by('id'),
        'data_summary': Tabel_2B_Summary.objects.get(id=1)
    }
    return render(request, 'lkps_app/tabel_2b_lulusan.html', ctx)
# ==========================================
# KRITERIA 3, 4, 5 & 6
# ==========================================

def tabel_3_penelitian(request):
    Tabel_3_Summary.objects.get_or_create(id=1)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                # 1. Update Tabel 3.A.1 Sarana
                Tabel_3A1_Sarana.objects.all().delete()
                s_nama = request.POST.getlist('nama_prasarana[]')
                s_daya = request.POST.getlist('daya_tampung[]')
                s_luas = request.POST.getlist('luas_ruang[]')
                s_milik = request.POST.getlist('kepemilikan[]')
                s_lisensi = request.POST.getlist('lisensi[]')
                s_perangkat = request.POST.getlist('perangkat[]')
                s_link = request.POST.getlist('link_bukti_prasarana[]')
                for i in range(len(s_nama)):
                    if s_nama[i].strip():
                        Tabel_3A1_Sarana.objects.create(
                            nama_prasarana=s_nama[i], daya_tampung=int(s_daya[i] or 0),
                            luas_ruang=float(s_luas[i] or 0), kepemilikan=s_milik[i],
                            lisensi=s_lisensi[i], perangkat=s_perangkat[i], link_bukti=s_link[i]
                        )

                # 2. Update Tabel 3.A.2 Penelitian
                Tabel_3A2_Penelitian.objects.all().delete()
                p_nama = request.POST.getlist('nama_dtpr_ketua[]')
                p_mhs = request.POST.getlist('jml_mhs_terlibat[]')
                p_judul = request.POST.getlist('judul_penelitian[]')
                p_hibah = request.POST.getlist('jenis_hibah[]')
                p_lni = request.POST.getlist('sumber_lni[]')
                p_durasi = request.POST.getlist('durasi_tahun[]')
                p_ts2 = request.POST.getlist('dana_ts2[]')
                p_ts1 = request.POST.getlist('dana_ts1[]')
                p_ts = request.POST.getlist('dana_ts[]')
                p_link = request.POST.getlist('link_bukti_penelitian[]')
                for i in range(len(p_nama)):
                    if p_nama[i].strip() or p_judul[i].strip():
                        Tabel_3A2_Penelitian.objects.create(
                            nama_dtpr=p_nama[i], jml_mhs=int(p_mhs[i] or 0), judul=p_judul[i],
                            jenis_hibah=p_hibah[i], sumber_lni=p_lni[i], durasi=float(p_durasi[i] or 1),
                            dana_ts2=float(p_ts2[i] or 0), dana_ts1=float(p_ts1[i] or 0),
                            dana_ts=float(p_ts[i] or 0), link_bukti=p_link[i]
                        )

                # 3. Update Tabel 3.C.1 Kerjasama
                Tabel_3C1_Kerjasama.objects.all().delete()
                k_judul = request.POST.getlist('judul_kerjasama[]')
                k_mitra = request.POST.getlist('mitra_kerjasama[]')
                k_lni = request.POST.getlist('sumber_kerjasama_lni[]')
                k_durasi = request.POST.getlist('durasi_kerjasama[]')
                k_ts2 = request.POST.getlist('dana_k_ts2[]')
                k_ts1 = request.POST.getlist('dana_k_ts1[]')
                k_ts = request.POST.getlist('dana_k_ts[]')
                k_link = request.POST.getlist('link_bukti_kerjasama[]')
                for i in range(len(k_judul)):
                    if k_judul[i].strip():
                        Tabel_3C1_Kerjasama.objects.create(
                            judul=k_judul[i], mitra=k_mitra[i], sumber_lni=k_lni[i],
                            durasi=float(k_durasi[i] or 1), dana_ts2=float(k_ts2[i] or 0),
                            dana_ts1=float(k_ts1[i] or 0), dana_ts=float(k_ts[i] or 0), link_bukti=k_link[i]
                        )

                # 4. Update Tabel 3.C.2 Publikasi (Dengan trik hidden input)
                Tabel_3C2_Publikasi.objects.all().delete()
                pub_nama = request.POST.getlist('nama_dtpr_pub[]')
                pub_judul = request.POST.getlist('judul_pub[]')
                pub_jenis = request.POST.getlist('jenis_pub[]')
                pub_ts2 = request.POST.getlist('pub_ts2[]')
                pub_ts1 = request.POST.getlist('pub_ts1[]')
                pub_ts = request.POST.getlist('pub_ts[]')
                for i in range(len(pub_nama)):
                    if pub_nama[i].strip():
                        Tabel_3C2_Publikasi.objects.create(
                            nama_dtpr=pub_nama[i], judul=pub_judul[i], jenis_pub=pub_jenis[i],
                            ts2=(pub_ts2[i] == '1'), ts1=(pub_ts1[i] == '1'), ts=(pub_ts[i] == '1')
                        )

                # 5. Update Tabel 3.C.3 HKI (Dengan trik hidden input)
                Tabel_3C3_HKI.objects.all().delete()
                hki_judul = request.POST.getlist('judul_hki[]')
                hki_jenis = request.POST.getlist('jenis_hki[]')
                hki_nama = request.POST.getlist('nama_dtpr_hki[]')
                hki_ts2 = request.POST.getlist('hki_ts2[]')
                hki_ts1 = request.POST.getlist('hki_ts1[]')
                hki_ts = request.POST.getlist('hki_ts[]')
                for i in range(len(hki_judul)):
                    if hki_judul[i].strip():
                        Tabel_3C3_HKI.objects.create(
                            judul=hki_judul[i], jenis_hki=hki_jenis[i], nama_dtpr=hki_nama[i],
                            ts2=(hki_ts2[i] == '1'), ts1=(hki_ts1[i] == '1'), ts=(hki_ts[i] == '1')
                        )

                # 6. Update Summary
                summary = Tabel_3_Summary.objects.get(id=1)
                summary.link_roadmap = request.POST.get('link_roadmap_penelitian')
                summary.total_jenis_hibah = int(request.POST.get('total_jenis_hibah') or 0)
                summary.total_mitra = int(request.POST.get('total_mitra') or 0)
                summary.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # GET Request: Kirim semua data ke HTML
    ctx = {
        'data_3a1': Tabel_3A1_Sarana.objects.all(),
        'data_3a2': Tabel_3A2_Penelitian.objects.all(),
        'data_3c1': Tabel_3C1_Kerjasama.objects.all(),
        'data_3c2': Tabel_3C2_Publikasi.objects.all(),
        'data_3c3': Tabel_3C3_HKI.objects.all(),
        'summary': Tabel_3_Summary.objects.get(id=1),
    }
    return render(request, 'lkps_app/tabel_3_penelitian.html', ctx)
def tabel_4_pkm(request):
    Tabel_4_Summary.objects.get_or_create(id=1)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                # 1. Update Tabel 4.A.1 Sarana
                Tabel_4A1_Sarana.objects.all().delete()
                s_nama = request.POST.getlist('nama_prasarana_pkm[]')
                s_daya = request.POST.getlist('daya_tampung_pkm[]')
                s_luas = request.POST.getlist('luas_ruang_pkm[]')
                s_milik = request.POST.getlist('kepemilikan_pkm[]')
                s_lisensi = request.POST.getlist('lisensi_pkm[]')
                s_perangkat = request.POST.getlist('perangkat_pkm[]')
                s_link = request.POST.getlist('link_bukti_prasarana_pkm[]')
                for i in range(len(s_nama)):
                    if s_nama[i].strip():
                        Tabel_4A1_Sarana.objects.create(
                            nama_prasarana=s_nama[i], daya_tampung=int(s_daya[i] or 0),
                            luas_ruang=float(s_luas[i] or 0), kepemilikan=s_milik[i],
                            lisensi=s_lisensi[i], perangkat=s_perangkat[i], link_bukti=s_link[i]
                        )

                # 2. Update Tabel 4.A.2 PkM
                Tabel_4A2_PkM.objects.all().delete()
                p_nama = request.POST.getlist('nama_dtpr_pkm[]')
                p_judul = request.POST.getlist('judul_kegiatan_pkm[]')
                p_mhs = request.POST.getlist('jml_mhs_pkm[]')
                p_hibah = request.POST.getlist('jenis_hibah_pkm[]')
                p_lni = request.POST.getlist('sumber_dana_pkm[]')
                p_durasi = request.POST.getlist('durasi_pkm[]')
                p_ts2 = request.POST.getlist('dana_pkm_ts2[]')
                p_ts1 = request.POST.getlist('dana_pkm_ts1[]')
                p_ts = request.POST.getlist('dana_pkm_ts[]')
                p_link = request.POST.getlist('link_bukti_dana_pkm[]')
                for i in range(len(p_nama)):
                    if p_nama[i].strip() or p_judul[i].strip():
                        Tabel_4A2_PkM.objects.create(
                            nama_dtpr=p_nama[i], judul=p_judul[i], jml_mhs=int(p_mhs[i] or 0),
                            jenis_hibah=p_hibah[i], sumber_lni=p_lni[i], durasi=float(p_durasi[i] or 1),
                            dana_ts2=float(p_ts2[i] or 0), dana_ts1=float(p_ts1[i] or 0),
                            dana_ts=float(p_ts[i] or 0), link_bukti=p_link[i]
                        )

                # 3. Update Tabel 4.C.1 Kerjasama
                Tabel_4C1_Kerjasama.objects.all().delete()
                k_judul = request.POST.getlist('judul_kerjasama_pkm[]')
                k_mitra = request.POST.getlist('mitra_kerjasama_pkm[]')
                k_lni = request.POST.getlist('sumber_kerja_pkm[]')
                k_durasi = request.POST.getlist('durasi_kerja_pkm[]')
                k_ts2 = request.POST.getlist('dana_kpkm_ts2[]')
                k_ts1 = request.POST.getlist('dana_kpkm_ts1[]')
                k_ts = request.POST.getlist('dana_kpkm_ts[]')
                k_link = request.POST.getlist('link_bukti_kerja_pkm[]')
                for i in range(len(k_judul)):
                    if k_judul[i].strip():
                        Tabel_4C1_Kerjasama.objects.create(
                            judul=k_judul[i], mitra=k_mitra[i], sumber_lni=k_lni[i],
                            durasi=float(k_durasi[i] or 1), dana_ts2=float(k_ts2[i] or 0),
                            dana_ts1=float(k_ts1[i] or 0), dana_ts=float(k_ts[i] or 0), link_bukti=k_link[i]
                        )

                # 4. Update Tabel 4.C.2 Diseminasi (hidden input checkbox)
                Tabel_4C2_Diseminasi.objects.all().delete()
                d_nama = request.POST.getlist('nama_dtpr_disem[]')
                d_judul = request.POST.getlist('judul_disem[]')
                d_lni = request.POST.getlist('lni_disem[]')
                d_ts2 = request.POST.getlist('disem_ts2[]')
                d_ts1 = request.POST.getlist('disem_ts1[]')
                d_ts = request.POST.getlist('disem_ts[]')
                d_link = request.POST.getlist('link_bukti_disem[]')
                for i in range(len(d_nama)):
                    if d_nama[i].strip():
                        Tabel_4C2_Diseminasi.objects.create(
                            nama_dtpr=d_nama[i], judul=d_judul[i], lni=d_lni[i],
                            ts2=(d_ts2[i] == '1'), ts1=(d_ts1[i] == '1'), ts=(d_ts[i] == '1'), link_bukti=d_link[i]
                        )

                # 5. Update Tabel 4.C.3 HKI PkM (hidden input checkbox)
                Tabel_4C3_HKI.objects.all().delete()
                h_judul = request.POST.getlist('judul_hki_pkm[]')
                h_jenis = request.POST.getlist('jenis_hki_pkm[]')
                h_nama = request.POST.getlist('nama_dtpr_hki_pkm[]')
                h_ts2 = request.POST.getlist('hkipkm_ts2[]')
                h_ts1 = request.POST.getlist('hkipkm_ts1[]')
                h_ts = request.POST.getlist('hkipkm_ts[]')
                h_link = request.POST.getlist('link_bukti_hki_pkm[]')
                for i in range(len(h_judul)):
                    if h_judul[i].strip():
                        Tabel_4C3_HKI.objects.create(
                            judul=h_judul[i], jenis_hki=h_jenis[i], nama_dtpr=h_nama[i],
                            ts2=(h_ts2[i] == '1'), ts1=(h_ts1[i] == '1'), ts=(h_ts[i] == '1'), link_bukti=h_link[i]
                        )

                # 6. Update Summary
                summary = Tabel_4_Summary.objects.get(id=1)
                summary.link_roadmap = request.POST.get('link_roadmap_pkm')
                summary.total_jenis_hibah = int(request.POST.get('total_jenis_hibah_pkm') or 0)
                summary.jml_disem_hasil = int(request.POST.get('jml_disem_hasil') or 0)
                summary.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # GET Request: Kirim semua data ke HTML
    ctx = {
        'data_4a1': Tabel_4A1_Sarana.objects.all(),
        'data_4a2': Tabel_4A2_PkM.objects.all(),
        'data_4c1': Tabel_4C1_Kerjasama.objects.all(),
        'data_4c2': Tabel_4C2_Diseminasi.objects.all(),
        'data_4c3': Tabel_4C3_HKI.objects.all(),
        'summary':  Tabel_4_Summary.objects.get(id=1),
    }
    return render(request, 'lkps_app/tabel_4_pkm.html', ctx)

def tabel_5_akuntabilitas(request):
    # PRE-SEEDING: Memastikan 5 baris standar selalu ada
    jenis_default = ["Pendidikan", "Keuangan", "SDM", "Sarana Prasarana", "Sistem Penjaminan Mutu"]
    for jenis in jenis_default:
        Tabel_5_1_TataKelola.objects.get_or_create(jenis_tata_kelola=jenis)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                # 1. Simpan Tabel 5.1 Tata Kelola
                Tabel_5_1_TataKelola.objects.all().delete()
                jenis_tk = request.POST.getlist('jenis_tata_kelola[]')
                nama_sis = request.POST.getlist('nama_sistem_info[]')
                akses = request.POST.getlist('akses_sistem[]')
                unit = request.POST.getlist('unit_pengelola_sistem[]')
                link_tk = request.POST.getlist('link_bukti_sistem[]')
                
                for i in range(len(jenis_tk)):
                    if jenis_tk[i].strip() or nama_sis[i].strip():
                        Tabel_5_1_TataKelola.objects.create(
                            jenis_tata_kelola=jenis_tk[i], nama_sistem=nama_sis[i],
                            akses=akses[i], unit_pengelola=unit[i], link_bukti=link_tk[i]
                        )

                # 2. Simpan Tabel 5.2 Sarana
                Tabel_5_2_Sarana.objects.all().delete()
                nama_pra = request.POST.getlist('nama_prasarana_pend[]')
                daya = request.POST.getlist('daya_tampung_pend[]')
                luas = request.POST.getlist('luas_ruang_pend[]')
                milik = request.POST.getlist('kepemilikan_pend[]')
                lisensi = request.POST.getlist('lisensi_pend[]')
                perangkat = request.POST.getlist('perangkat_pend[]')
                link_pra = request.POST.getlist('link_bukti_prasarana_pend[]')

                for i in range(len(nama_pra)):
                    if nama_pra[i].strip():
                        Tabel_5_2_Sarana.objects.create(
                            nama_prasarana=nama_pra[i], daya_tampung=int(daya[i] or 0),
                            luas_ruang=float(luas[i] or 0), kepemilikan=milik[i],
                            lisensi=lisensi[i], perangkat=perangkat[i], link_bukti=link_pra[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    ctx = {
        'data_5_1': Tabel_5_1_TataKelola.objects.all(),
        'data_5_2': Tabel_5_2_Sarana.objects.all()
    }
    return render(request, 'lkps_app/tabel_5_akuntabilitas.html', ctx)

def tabel_6_misi(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            Tabel_6_Misi.objects.update_or_create(
                id=1, 
                defaults={
                    'visi_pt': request.POST.get('visi_pt'),
                    'visi_upps': request.POST.get('visi_upps'),
                    'visi_ps': request.POST.get('visi_ps'),
                    'misi_pt': request.POST.get('misi_pt'),
                    'misi_upps': request.POST.get('misi_upps')
                }
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    data, created = Tabel_6_Misi.objects.get_or_create(id=1)
    return render(request, 'lkps_app/tabel_6_misi.html', {'data': data})