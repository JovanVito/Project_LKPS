from django.shortcuts import render, redirect
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json

@api_view(['POST'])
def fetch_data_lppm(request):
    """
    Endpoint untuk menerima sinkronisasi data dari sistem LPPM.
    Data yang dikirim harus berupa JSON.
    """
    try:
        # Mengambil data JSON yang dikirim oleh sistem LPPM
        data_masuk = request.data
        
        # Contoh Logika: Jika LPPM mengirim data penelitian
        # Kita bisa memprosesnya di sini sebelum disimpan ke database LKPS
        # print(f"Data diterima dari LPPM: {data_masuk}")

        # Memberikan feedback sukses ke sistem LPPM
        return Response({
            "status": "success",
            "message": "Data LPPM berhasil diterima oleh sistem LKPS Universitas Pradita",
            "received_count": len(data_masuk) if isinstance(data_masuk, list) else 1
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    
# --- CORE VIEWS ---
def logout_user(request):
    logout(request)
    return redirect('dashboard')

def dashboard(request):
    return render(request, 'lkps_app/dashboard.html')

def program_studi(request):
    return render(request, 'lkps_app/program_studi.html')

def manajemen_user(request):
    return render(request, 'lkps_app/manajemen_user.html')

def sampul(request):
    return render(request, 'lkps_app/sampul.html')

# --- KRITERIA 1: TATA PAMONG ---
def tabel_1a1(request):
    return render(request, 'lkps_app/tabel_1a1.html')

def tabel_1a_dana(request): # Mencakup 1.A.2 & 1.A.3
    return render(request, 'lkps_app/tabel_1a_dana.html')

def tabel_1a4(request):
    return render(request, 'lkps_app/tabel_1a4.html')

def tabel_1a5(request):
    return render(request, 'lkps_app/tabel_1a5.html')

def tabel_1b(request):
    return render(request, 'lkps_app/tabel_1b.html')

# --- KRITERIA 2: MAHASISWA & PENDIDIKAN ---
def tabel_2a1(request):
    return render(request, 'lkps_app/tabel_2a1.html')

def tabel_2a2(request):
    return render(request, 'lkps_app/tabel_2a2.html')

def tabel_2a3(request):
    return render(request, 'lkps_app/tabel_2a3.html')

def tabel_2b1(request):
    return render(request, 'lkps_app/tabel_2b1.html')

def tabel_2b2(request):
    return render(request, 'lkps_app/tabel_2b2.html')

def tabel_2b3(request):
    return render(request, 'lkps_app/tabel_2b3.html')

def tabel_2b4(request):
    return render(request, 'lkps_app/tabel_2b4.html')

def tabel_2b5(request):
    return render(request, 'lkps_app/tabel_2b5.html')

def tabel_2b6(request):
    return render(request, 'lkps_app/tabel_2b6.html')

def tabel_2c(request):
    return render(request, 'lkps_app/tabel_2c.html')

def tabel_2d(request):
    return render(request, 'lkps_app/tabel_2d.html')

# --- KRITERIA 3, 4, 5, 6 ---
def tabel_3_penelitian(request): # Mencakup 3.A.1 & 3.A.2
    return render(request, 'lkps_app/tabel_3_penelitian.html')

def tabel_3a3(request):
    return render(request, 'lkps_app/tabel_3a3.html')

def tabel_4_pkm(request):
    return render(request, 'lkps_app/tabel_4_pkm.html')

def tabel_5_akuntabilitas(request):
    return render(request, 'lkps_app/tabel_5_akuntabilitas.html')

def tabel_6(request):
    return render(request, 'lkps_app/tabel_6.html')