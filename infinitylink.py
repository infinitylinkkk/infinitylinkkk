from time import sleep
import threading
from concurrent.futures import ThreadPoolExecutor, wait
from sms import SendSms
from colorama import Fore, Style, init

# Colorama'yı başlat
init(autoreset=True)

# SMS servislerinin listesi
servisler_sms = [attr for attr in dir(SendSms) if callable(getattr(SendSms, attr)) and not attr.startswith('__')]

# Global değişkenler
stop_flag = False

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
        print(Fore.GREEN + "İşlem durduruldu.")

# SMS Gönderimini Durdur
def stop_sending():
    global stop_flag
    stop_flag = True
    print(Fore.GREEN + "SMS gönderimi durduruldu.")

# Komut Satırı Arayüzü
def start_normal_sms():
    tel_no = input(Fore.GREEN + "Telefon numarası giriniz (10 haneli): ")
    mail = input(Fore.GREEN + "Mail Adresi (Opsiyonel): ")

    if len(tel_no) != 10 or not tel_no.isdigit():
        print(Fore.GREEN + "Hata: Geçersiz telefon numarası. Numara 10 haneli olmalıdır.")
        return

    try:
        kere = int(input(Fore.GREEN + "Kaç Adet (opsiyonel, boş bırakabilirsiniz): ")) if input(Fore.GREEN + "Kaç Adet (opsiyonel, boş bırakabilirsiniz): ") else None
    except ValueError:
        print(Fore.GREEN + "Hata: Geçersiz sayı girdiniz.")
        return

    try:
        aralik = int(input(Fore.GREEN + "Aralık (0 yazın): "))
    except ValueError:
        print(Fore.GREEN + "Hata: Geçersiz aralık değeri.")
        return

    tel_liste = [tel_no]
    threading.Thread(target=send_sms_normal, args=(tel_liste, mail, kere, aralik)).start()

def start_turbo_sms():
    tel_no = input(Fore.GREEN + "Telefon numarası giriniz (10 haneli): ")
    mail = input(Fore.GREEN + "Mail Adresi (Opsiyonel): ")

    if len(tel_no) != 10 or not tel_no.isdigit():
        print(Fore.GREEN + "Hata: Geçersiz telefon numarası. Numara 10 haneli olmalıdır.")
        return

    threading.Thread(target=send_sms_turbo, args=(tel_no, mail)).start()

# Ana Program Döngüsü
def main():
    print(Fore.CYAN + "=" * 35)
    print(Fore.CYAN + "     İ N F İ N İ T Y  L İ N K")
    print(Fore.CYAN + "=" * 35)
    
    while True:
        print(Fore.GREEN + "1. Normal SMS Gönder")
        print(Fore.GREEN + "2. Fast SMS Gönder")
        print(Fore.GREEN + "3. Durdur")
        print(Fore.GREEN + "4. Çıkış")
        choice = input(Fore.RED + "Seçiminizi yapın (1/2/3/4): ")

        if choice == '1':
            start_normal_sms()
        elif choice == '2':
            start_turbo_sms()
        elif choice == '3':
            stop_sending()
        elif choice == '4':
            print(Fore.GREEN + "Program sonlandırılıyor.")
            break
        else:
            print(Fore.GREEN + "Geçersiz seçim. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()