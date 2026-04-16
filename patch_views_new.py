import os

with open('lkps_app/views.py', 'r', encoding='utf-8') as f:
    text = f.read()

tabel_1b_logic = """def tabel_1b(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                Tabel_1B_SPMI.objects.all().delete()
                n_unit = request.POST.getlist('nama_unit[]')
                dok = request.POST.getlist('dokumen[]')
                j_cert = request.POST.getlist('jml_auditor_cert[]')
                j_non = request.POST.getlist('jml_auditor_non[]')
                frek = request.POST.getlist('frekuensi_audit[]')
                l_pt = request.POST.getlist('link_pt[]')
                l_ups = request.POST.getlist('link_upps[]')
                for i in range(len(n_unit)):
                    if n_unit[i].strip():
                        Tabel_1B_SPMI.objects.create(
                            nama_unit=n_unit[i], dokumen=dok[i],
                            jml_auditor_cert=int(j_cert[i] or 0),
                            jml_auditor_non=int(j_non[i] or 0),
                            frekuensi_audit=int(frek[i] or 0),
                            link_pt=l_pt[i], link_upps=l_ups[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'lkps_app/tabel_1b.html', {'data_1b': Tabel_1B_SPMI.objects.all()})"""

tabel_2c_logic = """def tabel_2c(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                Tabel_2C_Fleksibilitas.objects.all().delete()
                bent = request.POST.getlist('bentuk_pembelajaran[]')
                ts2 = request.POST.getlist('ts_2[]')
                ts1 = request.POST.getlist('ts_1[]')
                ts0 = request.POST.getlist('ts[]')
                link = request.POST.getlist('link_bukti[]')
                for i in range(len(bent)):
                    if bent[i].strip():
                        Tabel_2C_Fleksibilitas.objects.create(
                            bentuk_pembelajaran=bent[i],
                            ts_2=int(ts2[i] or 0), ts_1=int(ts1[i] or 0), ts=int(ts0[i] or 0),
                            link_bukti=link[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'lkps_app/tabel_2c.html', {'data_2c': Tabel_2C_Fleksibilitas.objects.all()})"""

tabel_2d_logic = """def tabel_2d(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                Tabel_2D_Rekognisi.objects.all().delete()
                sumb = request.POST.getlist('sumber[]')
                jnis = request.POST.getlist('jenis_pengakuan[]')
                ts2 = request.POST.getlist('ts_2[]')
                ts1 = request.POST.getlist('ts_1[]')
                ts0 = request.POST.getlist('ts[]')
                link = request.POST.getlist('link_bukti[]')
                for i in range(len(sumb)):
                    if jnis[i].strip():
                        Tabel_2D_Rekognisi.objects.create(
                            sumber=sumb[i], jenis_pengakuan=jnis[i],
                            ts_2=int(ts2[i] or 0), ts_1=int(ts1[i] or 0), ts=int(ts0[i] or 0),
                            link_bukti=link[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'lkps_app/tabel_2d.html', {'data_2d': Tabel_2D_Rekognisi.objects.all()})"""

tabel_3a3_logic = """def tabel_3a3(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            with transaction.atomic():
                Tabel_3A3_Pengembangan_DTPR.objects.all().delete()
                jnis = request.POST.getlist('jenis_pengembangan[]')
                nama = request.POST.getlist('nama_dosen[]')
                ts2 = request.POST.getlist('ts_2[]')
                ts1 = request.POST.getlist('ts_1[]')
                ts0 = request.POST.getlist('ts[]')
                link = request.POST.getlist('link_bukti[]')
                for i in range(len(jnis)):
                    if jnis[i].strip() or nama[i].strip():
                        Tabel_3A3_Pengembangan_DTPR.objects.create(
                            jenis_pengembangan=jnis[i], nama_dosen=nama[i],
                            ts_2=int(ts2[i] or 0), ts_1=int(ts1[i] or 0), ts=int(ts0[i] or 0),
                            link_bukti=link[i]
                        )
            return JsonResponse({'status': 'success'})
        except Exception as e: return JsonResponse({'status': 'error', 'message': str(e)})
    return render(request, 'lkps_app/tabel_3a3.html', {'data_3a3': Tabel_3A3_Pengembangan_DTPR.objects.all()})"""

text = text.replace("def tabel_1b(request):\n    return render(request, 'lkps_app/tabel_1b.html')", tabel_1b_logic)
text = text.replace("def tabel_2c(request):\n    return render(request, 'lkps_app/tabel_2c.html')", tabel_2c_logic)
text = text.replace("def tabel_2d(request):\n    return render(request, 'lkps_app/tabel_2d.html')", tabel_2d_logic)
text = text.replace("def tabel_3a3(request):\n    return render(request, 'lkps_app/tabel_3a3.html')", tabel_3a3_logic)

# ADD IMPORTS TO THE TOP IF NOT EXISTS
import_str = "    Tabel_1B_SPMI, Tabel_2C_Fleksibilitas, Tabel_2D_Rekognisi, Tabel_3A3_Pengembangan_DTPR,\n"
if "Tabel_1B_SPMI" not in text:
    text = text.replace(
        "Tabel_1A1, Tabel_1A2_Sumber, Tabel_1A3_Penggunaan, Tabel_1A4, Tabel_1A5,",
        import_str + "    Tabel_1A1, Tabel_1A2_Sumber, Tabel_1A3_Penggunaan, Tabel_1A4, Tabel_1A5,"
    )

with open('lkps_app/views.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Views patched successfully")
