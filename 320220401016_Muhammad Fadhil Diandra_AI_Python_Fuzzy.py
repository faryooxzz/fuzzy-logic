import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Baca data dari file CSV dengan delimiter koma
flpath=r"C:\Users\fadhi\Downloads\Tugas Fuzzy\Tingkat kecerdasan mahasiswa.xlsx"
data = pd.read_excel(flpath)
print(data.shape)

# Definisikan variabel input
IQ = ctrl.Antecedent(np.arange(80, 141, 1), 'IQ')
EQ = ctrl.Antecedent(np.arange(100, 161, 1), 'EQ')
SQ = ctrl.Antecedent(np.arange(10, 51, 1), 'SQ')

# Definisikan variabel output
tingkat_kecerdasan = ctrl.Consequent(np.arange(0, 101, 1), 'tingkat_kecerdasan')

# Definisikan fungsi keanggotaan untuk variabel input dan output
IQ.automf(3)
EQ.automf(3)
SQ.automf(3)

tingkat_kecerdasan['kurang_pintar'] = fuzz.trimf(tingkat_kecerdasan.universe, [0, 0, 60])
tingkat_kecerdasan['sedang'] = fuzz.trimf(tingkat_kecerdasan.universe, [40, 50, 80])
tingkat_kecerdasan['pintar'] = fuzz.trimf(tingkat_kecerdasan.universe, [70, 100, 100])

# Aturan fuzzy
rule1 = ctrl.Rule(IQ['poor'] | EQ['poor'] | SQ['poor'], tingkat_kecerdasan['kurang_pintar'])
rule2 = ctrl.Rule(IQ['average'] | EQ['average'] | SQ['average'], tingkat_kecerdasan['sedang'])
rule3 = ctrl.Rule(IQ['good'] | EQ['good'] | SQ['good'], tingkat_kecerdasan['pintar'])

# Buat sistem kontrol fuzzy
tingkat_kecerdasan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tingkat_kecerdasan_simulasi = ctrl.ControlSystemSimulation(tingkat_kecerdasan_ctrl)

# Inisialisasi list untuk menyimpan hasil
hasil_tingkat_kecerdasan = []

# Iterasi melalui setiap record dalam data
for index, row in data.iterrows():
    # Masukkan nilai variabel input dari data yang dibaca
    tingkat_kecerdasan_simulasi.input['IQ'] = row['IQ']
    tingkat_kecerdasan_simulasi.input['EQ'] = row['EQ']
    tingkat_kecerdasan_simulasi.input['SQ'] = row['SQ']

    # Hitung nilai variabel output
    tingkat_kecerdasan_simulasi.compute()

    # Simpan hasil
    hasil_tingkat_kecerdasan.append(tingkat_kecerdasan_simulasi.output['tingkat_kecerdasan'])

# Tambahkan hasil ke data frame
data['tingkat_kecerdasan'] = hasil_tingkat_kecerdasan

# Simpan ke file Excel
data.to_excel('hasil_kecerdasan_mahasiswa.xlsx', index=False)
