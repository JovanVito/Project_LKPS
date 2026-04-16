import os
from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate docxtpl Jinja2 tags for all models in lkps_app'

    def handle(self, *args, **kwargs):
        app_config = apps.get_app_config('lkps_app')
        models = app_config.get_models()
        
        output_path = os.path.join(settings.BASE_DIR, 'word_tags_siap_paste.txt')
        
        output_lines = []
        output_lines.append("="*70)
        output_lines.append("         JINJA TAGS (DOCXTPL) UNTUK MASTER_FORMAT_LKPS.DOCX         ")
        output_lines.append(" PENTING: Gunakan awalan {% tr for ... %} dan akhiran {% endtr %}   ")
        output_lines.append("          agar baris tabel Word berhasil ter-looping secara baris.  ")
        output_lines.append("="*70 + "\n")

        for model in models:
            model_name = model.__name__
            # Menggunakan format alias yg gampang dibaca secara seragam
            alias = f"t_{model_name}"
            
            output_lines.append("=========================================")
            output_lines.append(f"MODEL: {model_name} (Alias Context: {alias})")
            output_lines.append("=========================================")
            
            # Ambil fields konkrit, abaikan id dan timestamp
            ignore_fields = ['id', 'created_at', 'updated_at', 'waktu_resmi']
            fields = []
            
            for f in model._meta.get_fields():
                if f.name in ignore_fields:
                    continue
                # Skip reverse relations yang tidak ada secara konkrit di database tabel ini
                if f.auto_created and not f.concrete:
                    continue
                
                # Deteksi jika itu Foreign Key
                field_label = f.name
                if f.is_relation and f.many_to_one:
                    field_label = f"{f.name}_id  <-- (Perhatian: Ini Foreign Key)"
                
                fields.append(field_label)
                
            if not fields:
                output_lines.append("Model ini tidak memiliki kolom yang bisa di-loop.\n\n")
                continue
                
            # Logika pembagian Kolom (Kiri, Tengah, Kanan) spt permintaan pengguna
            first_field = fields[0]
            last_field = fields[-1]
            middle_fields = fields[1:-1]
            
            output_lines.append("KOTAK KIRI (Kolom 1):")
            # WARNING: We use {% tr for %} instead of {% for %} because docxtpl
            # requires 'tr' to duplicate Word Table Rows. If they use {% for %},
            # it will throw XML block errors or mess up the layout.
            output_lines.append(f"{{% tr for r in {alias} %}}")
            # Kita pecah spasi untuk mengambil nama method field aslinya saja agar valid
            output_lines.append(f"{{{{ r.{first_field.split()[0]} }}}}\n")
            
            output_lines.append("KOTAK TENGAH (Kolom 2 s/d N-1):")
            if middle_fields:
                for f in middle_fields:
                    nama_variabel = f.split()[0]
                    catatan = f.replace(nama_variabel, "").strip() # Ambil komentar "(Perhatian: Ini Foreign key)"
                    line = f"{{{{ r.{nama_variabel} }}}}"
                    if catatan:
                        line += f"  {catatan}"
                    output_lines.append(line)
            else:
                output_lines.append("-")
            output_lines.append("")
            
            output_lines.append("KOTAK KANAN (Kolom Terakhir):")
            if len(fields) > 1:
                nama_variabel = last_field.split()[0]
                catatan = last_field.replace(nama_variabel, "").strip()
                line = f"{{{{ r.{nama_variabel} }}}}"
                if catatan:
                    line += f"  {catatan}"
                output_lines.append(line)
            else:
                output_lines.append("(Seluruhnya ada di Kotak Kiri saja karena tabel cuma 1 kolom)")
                
            output_lines.append("{% endtr %}\n\n")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
            
        self.stdout.write(self.style.SUCCESS(f"BERHASIL! Model-model telah di-scan."))
        self.stdout.write(self.style.SUCCESS(f"File Output siap dipakai: {output_path}"))
