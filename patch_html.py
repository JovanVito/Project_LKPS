import re

# 1. Tabel 1B HTML
with open('lkps_app/templates/lkps_app/tabel_1b.html', 'r', encoding='utf-8') as f: text = f.read()
replacements = {
    'placeholder="Nama Unit"': 'name="nama_unit[]" placeholder="Nama Unit"',
    'placeholder="SK/Dokumen"': 'name="dokumen[]" placeholder="SK/Dokumen"',
    '<td><input type="number" class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>': '<td><input type="number" name="jml_auditor_cert[]" class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>',
    'placeholder="Link PT"': 'name="link_pt[]" placeholder="Link PT"',
    'placeholder="Link UPPS"': 'name="link_upps[]" placeholder="Link UPPS"',
}
# careful with identical number inputs, let's just do regex
import re
text = text.replace('placeholder="Nama Unit"', 'name="nama_unit[]" placeholder="Nama Unit"')
text = text.replace('placeholder="SK/Dokumen"', 'name="dokumen[]" placeholder="SK/Dokumen"')
text = text.replace('placeholder="Link PT"', 'name="link_pt[]" placeholder="Link PT"')
text = text.replace('placeholder="Link UPPS"', 'name="link_upps[]" placeholder="Link UPPS"')

# the 3 number inputs: jml_auditor_cert, jml_auditor_non, frekuensi_audit
# find all matches of the number input and replace sequentially
import re
number_input = r'<td><input type="number" class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>'
names = ['name="jml_auditor_cert[]"', 'name="jml_auditor_non[]"', 'name="frekuensi_audit[]"']
def repl(match):
    if hasattr(repl, "count"):
        repl.count += 1
    else:
        repl.count = 0
    if repl.count < len(names):
        return f'<td><input type="number" {names[repl.count]} class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>'
    return match.group(0)

text = re.sub(re.escape(number_input), repl, text)
with open('lkps_app/templates/lkps_app/tabel_1b.html', 'w', encoding='utf-8') as f: f.write(text)

# 2. Tabel 2C
with open('lkps_app/templates/lkps_app/tabel_2c.html', 'r', encoding='utf-8') as f: text = f.read()
text = text.replace('value="Micro-credential"', 'name="bentuk_pembelajaran[]" value="Micro-credential"')
text = text.replace('placeholder="URL Bukti"', 'name="link_bukti[]" placeholder="URL Bukti"')
names = ['name="ts_2[]"', 'name="ts_1[]"', 'name="ts[]"']
def repl2(match):
    if not hasattr(repl2, "count"): repl2.count = -1
    repl2.count += 1
    if repl2.count < len(names):
        return f'<td><input type="number" {names[repl2.count]} class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>'
    return match.group(0)
text = re.sub(re.escape(number_input), repl2, text)
with open('lkps_app/templates/lkps_app/tabel_2c.html', 'w', encoding='utf-8') as f: f.write(text)

# 3. Tabel 2D
with open('lkps_app/templates/lkps_app/tabel_2d.html', 'r', encoding='utf-8') as f: text = f.read()
text = text.replace('<select class="form-control form-control-sm', '<select name="sumber[]" class="form-control form-control-sm') # wait, what was it?
text = text.replace('select class="form-select', 'select name="sumber[]" class="form-select')
text = text.replace('placeholder="Contoh: Sertifikasi"', 'name="jenis_pengakuan[]" placeholder="Contoh: Sertifikasi"')
text = text.replace('placeholder="URL Bukti"', 'name="link_bukti[]" placeholder="URL Bukti"')
def repl3(match):
    if not hasattr(repl3, "count"): repl3.count = -1
    repl3.count += 1
    if repl3.count < len(names):
        return f'<td><input type="number" {names[repl3.count]} class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>'
    return match.group(0)
text = re.sub(re.escape(number_input), repl3, text)
with open('lkps_app/templates/lkps_app/tabel_2d.html', 'w', encoding='utf-8') as f: f.write(text)

# 4. Tabel 3A3
with open('lkps_app/templates/lkps_app/tabel_3a3.html', 'r', encoding='utf-8') as f: text = f.read()
text = text.replace('placeholder="Jenis Pengembangan"', 'name="jenis_pengembangan[]" placeholder="Jenis Pengembangan"')
text = text.replace('placeholder="Nama Dosen"', 'name="nama_dosen[]" placeholder="Nama Dosen"')
text = text.replace('placeholder="URL Bukti"', 'name="link_bukti[]" placeholder="URL Bukti"')
def repl4(match):
    if not hasattr(repl4, "count"): repl4.count = -1
    repl4.count += 1
    if repl4.count < len(names):
        return f'<td><input type="number" {names[repl4.count]} class="form-control form-control-sm border-0 bg-transparent auto-save-input text-center" placeholder="0"></td>'
    return match.group(0)
text = re.sub(re.escape(number_input), repl4, text)
with open('lkps_app/templates/lkps_app/tabel_3a3.html', 'w', encoding='utf-8') as f: f.write(text)

print("HTML patched successfully")

