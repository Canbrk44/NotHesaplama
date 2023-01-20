# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 16:43:04 2022

@author: Smurf
"""
#------------------NOT_Hesaplama----------------------#
#-----------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfa import *
from Hakkında import *
#------------------Uygulama Yarat----------------------#
#------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

penHakinda=QDialog() #Tasarım Esnasında Seçtiğimiz Pencere Modeli
ui2=Ui_Hakknda()
ui2.setupUi(penHakinda)


#------------------VeriTabanı Yarat----------------------#
#--------------------------------------------------------#
import sqlite3
global curs
global conn

conn=sqlite3.connect('NotHesapla.db')
curs=conn.cursor()
curs.execute('CREATE TABLE IF NOT EXISTS not_hesapla (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,ad_soyad TEXT NOT NULL,Sınıf INTEGER NOT NULL,Blm TEXT NOT NULL,ok_no TEXT NOT NULL UNIQUE,vize_notu TEXT NOT NULL,final_notu TEXT NOT NULL,ortalama FLOAT,harf_notu TEXT,durumu TEXT)')
conn.commit()

#------------------Kayıt Yarat---------------------------#
#--------------------------------------------------------#
def EKLE():
    ad_soyad =ui.line_Adsoyad.text()
    Sınıf = ui.SpinBox_Sinif.value()
    bölüm = ui.Combo_BLM.currentText()
    ok_no = ui.line_OKNO.text()
    vize = ui.line_Vize.text()
    ffinal= ui.line_Final.text()
    ortalama = 0
    ortalama = (int(vize) * 0.40) + (int(ffinal)  * 0.60)
      
    if ortalama<50:
        durum='Kaldı'
    else:
        durum = 'Geçti'
    if ortalama<=100 and ortalama>=85:
        harf_notu='A'
    elif ortalama<=84 and ortalama>=60:
        harf_notu='B'
    elif ortalama<=59 and ortalama>=45:
        harf_notu='C'
    elif ortalama<=44 and ortalama>=35:
        harf_notu='D'
    elif ortalama<=34:
        harf_notu = 'F'
    else:
        harf_notu='Hesaplanamadı!!'
        
   
    curs.execute("INSERT INTO not_hesapla(ad_soyad,Sınıf,Blm,ok_no,vize_notu,final_notu,ortalama,harf_notu,durumu)VALUES(?,?,?,?,?,?,?,?,?)",
                 (ad_soyad,Sınıf,bölüm,ok_no,vize,ffinal,ortalama,harf_notu,durum))
    conn.commit()
    LISTELE()#Anında GÜncelleme Yapabilmek İçin

#--------------------Listele--------------------------------------------#
#-----------------------------------------------------------------------# 
def LISTELE():
    ui.TabloBilgiler.clear()
    ui.TabloBilgiler.setHorizontalHeaderLabels(('ID','Ad Soyad','Sınıf','Bölüm','Okul No','Vize Notu','Final Notu','Ortalama','Harf Notu','Dönem Durumu'))
    ui.TabloBilgiler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM not_hesapla")
    for satirindeks,satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.TabloBilgiler.setItem(satirindeks, sutunIndeks, QTableWidgetItem(str(sutunVeri)))
    ui.line_OKNO.clear()
    ui.line_Adsoyad.clear()
    ui.line_Final.clear()
    ui.line_Vize.clear()
    curs.execute("SELECT COUNT(*) FROM not_hesapla")
    kayit_sayisi=curs.fetchone()
    ui.label_ogsayisi.setText(str(kayit_sayisi[0]))
    curs.execute("SELECT COUNT(*) FROM not_hesapla WHERE durumu = 'Kaldı'")
    kalan_sayisi = curs.fetchone()
    ui.label_KalanOS.setText(str(kalan_sayisi[0]))
    curs.execute("SELECT COUNT(*) FROM not_hesapla WHERE durumu='Geçti'")
    gecen_sayisi=curs.fetchone()
    ui.label_GecenOS.setText(str(gecen_sayisi[0]))
    curs.execute("SELECT AVG(ortalama) FROM not_hesapla")
    ort=curs.fetchone()
    ui.label_snfortalama.setText(str(ort[0]))
    
LISTELE()

#--------------------Kayıt-Sil--------------------------------------------#
#-------------------------------------------------------------------------# 
def SİL():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Silmek İstediğinize Emin misiniz ? ", QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        secili = ui.TabloBilgiler.selectedItems() #Seçili Kaydın Bilgilerini alır
        silinecek=secili[4].text() # Okul Numarası Bilgisine Erişiyoruz Tabloda
        try:
            curs.execute("DELETE FROM not_hesapla WHERE ok_no = '%s'" %(silinecek))
            conn.commit()
            LISTELE()
            ui.statusbar.showMessage("Kayıt Silme İşlemi Başarıyla Gerçekleşti",10000) # altta status barda bilgi verir
        except Exception as HATA:
            ui.statusbar.showMessage("Kayıt Silme İşlemi Tamamlanamadı ! ->"+str(HATA))
    else:
        ui.statusbar.showMessage("Kayıt Silme İşlemi İptal Edildi ",10000)
            
#--------------------Cıkıs------------------------------------------------#
#-------------------------------------------------------------------------# 
def CIKIS():
    cevap = QMessageBox.question(penAna,"CIKIS","Çıkıs Yapmak İstediğinize Emin misiniz ?",
                         QMessageBox.Yes | QMessageBox.No )
    if cevap == QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()
        
#--------------------Arama------------------------------------------------#
#-------------------------------------------------------------------------#
def ARA():
    aranan1=ui.line_OKNO.text()
    aranan2=ui.line_Adsoyad.text()
    curs.execute("SELECT * FROM not_hesapla WHERE ok_no = ? OR ad_soyad = ?",
                 (aranan1,aranan2))
    conn.commit()
    ui.TabloBilgiler.clear()
    for satirindeks,satirdeger in enumerate(curs):
        for sutunindeks,sutundeger in enumerate(satirdeger):
            ui.TabloBilgiler.setItem(satirindeks, sutunindeks, QTableWidgetItem(str(sutundeger)))


#--------------------DOLDUR----------------------------------------------------#
#------------------------------------------------------------------------------#
def DOLDUR():
    secili=ui.TabloBilgiler.selectedItems()
    ui.line_Adsoyad.setText(secili[1].text())
    ui.SpinBox_Sinif.setValue(int(secili[2].text()))
    ui.Combo_BLM.setCurrentText(secili[3].text())
    ui.line_OKNO.setText(secili[4].text())
    ui.line_Vize.setText(secili[5].text())
    ui.line_Final.setText(secili[6].text())
    
#--------------------Arama------------------------------------------------#
#-------------------------------------------------------------------------#
def GUNCELLE():
    cevap=QMessageBox.question(penAna,"KAYIT Güncelle ","Güncellemek İstediğinize Emin misiniz ? ", QMessageBox.Yes | QMessageBox.No)
    if cevap == QMessageBox.Yes:
        try:
            secili=ui.TabloBilgiler.selectedItems()
            Id=int(secili[0].text())
            ad_soyad =ui.line_Adsoyad.text()
            Sınıf = ui.SpinBox_Sinif.value()
            bölüm = ui.Combo_BLM.currentText()
            ok_no = ui.line_OKNO.text()
            vize = ui.line_Vize.text()
            ffinal= ui.line_Final.text()
            curs.execute("UPDATE not_hesapla SET ad_soyad=?,Sınıf=?,Blm=?,ok_no=?,vize_notu=?,final_notu=? WHERE ID=?",
                         (ad_soyad,Sınıf,bölüm,ok_no,vize,ffinal,Id))
            conn.commit()
            LISTELE()
        except Exception as Hata:
            ui.statusbar.showMessage("Hata Meydana Geldi..."+str(Hata))
    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi",10000)

#------------------Hakkında-------------------------------#
#---------------------------------------------------------#
def Hakkinda():
    penHakinda.show()

#------------------Buton Action---------------------------#
#---------------------------------------------------------#
ui.Button_Ekle.clicked.connect(EKLE)
ui.Button_Sil.clicked.connect(SİL)
ui.Button_cks.clicked.connect(CIKIS)
ui.Buton_KaytAra.clicked.connect(ARA)
ui.buton_listele.clicked.connect(LISTELE)
ui.TabloBilgiler.itemSelectionChanged.connect(DOLDUR)#Tabloda seçim yapıldıgında lineeditleri doldurur
ui.Button_Gncelle.clicked.connect(GUNCELLE)
ui.Menu_Hakknda.triggered.connect(Hakkinda) # Menülerde Clickeed Yerine Triggered Kullanılır

   
sys.exit(Uygulama.exec_())