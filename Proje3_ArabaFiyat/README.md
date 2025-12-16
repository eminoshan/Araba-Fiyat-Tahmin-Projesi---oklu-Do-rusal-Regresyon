# Araba Fiyat Tahmin Sistemi

**Ogrenci:** Muhammed Emin Oshan  
**Numara:** 2212729007

## Proje Hakkinda

Bu proje, coklu dogrusal regresyon ile araba fiyatlarini tahmin ediyor. Model Flask ile web arayuzunde sunuluyor.

## Dosyalar

```
app.py                 - Flask uygulamasi
model_egitimi.py       - Model egitim kodu
Proje3_Rapor_NEW.ipynb - Jupyter Notebook
araba_modeli.pkl       - Egitilmis model
araba_fiyatlari.csv    - Veri seti
templates/index.html   - Web arayuzu
```

## Kullanilan Kutuphaneler

- pandas
- numpy
- scikit-learn
- statsmodels
- Flask

## Veri Seti Ozellikleri

| Ozellik | Aciklama |
|---------|----------|
| Yil | Model yili (2010-2023) |
| Kilometre | Kat edilen km |
| Motor_Gucu | HP degeri |
| Hasar_Kaydi | Hasar tutari (TL) |
| Vites | Manuel/Otomatik |
| Renk | Beyaz/Siyah/Gri/Kirmizi |
| Fiyat | Hedef degisken |

## Model Sonuclari

- R2 Skoru: 0.98
- MAE: ~39.000 TL
- MSE: ~2.254.619.321

## Backward Elimination

Baslangic ozellikleri: Yil, Kilometre, Motor_Gucu, Hasar_Kaydi, Vites_Kod, Renk_Gri, Renk_Kirmizi, Renk_Siyah

Elenen ozellikler (p > 0.05):
- Renk_Gri (p=0.59)
- Renk_Kirmizi (p=0.36)
- Renk_Siyah (p=0.07)

Kalan ozellikler: Yil, Kilometre, Motor_Gucu, Hasar_Kaydi, Vites_Kod

## Calistirma

1. Kutuphaneleri yukle:
```
pip install pandas numpy scikit-learn statsmodels flask
```

2. Modeli egit:
```
python model_egitimi.py
```

3. Flask uygulamasini baslat:
```
python app.py
```

4. Tarayicida ac:
```
http://localhost:5000
```

## Ornek Tahmin

Giris:
- Yil: 2020
- Kilometre: 50.000
- Motor Gucu: 150 HP
- Hasar Kaydi: 0 TL
- Vites: Otomatik

Cikti: ~1.575.000 TL
