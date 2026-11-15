# Sunum Kontrol Listesi — Planet-X Sphere

**Proje:** planet-x-sphere  
**Etkinlik:** NASA International Space Apps Challenge  
**Tarih:** 2026-11-15  
**Durum etiketleri:** `[V]` = doğrulandı · `[NV]` = henüz doğrulanmadı · `[ASSUMPTION]` = varsayım

---

## 1. Teknik Tamamlama

### 1.1 Pipeline — Barnard Yıldızı (öncelikli hedef)
- [ ] TAP sorgusu veya L0 veri kaynağı bağlı ve çalışıyor `[NV]`
- [ ] S3 kovası erişilebilir; Barnard karolarının tümü yüklü `[NV]`
- [ ] Görüntüleyicide Barnard'a ait görüntüler hatasız açılıyor `[NV]`

### 1.2 Beş Hedefin Tümü
- [ ] **Barnard** — görüntülenebilir `[NV]`
- [ ] **ε Indi B** — görüntülenebilir `[NV]`
- [ ] **WISE 0855** — görüntülenebilir `[NV]`
- [ ] **RW Aur** — görüntülenebilir `[NV]`
- [ ] **R Dra** — görüntülenebilir `[NV]`

> Kapsam dışı kalan hedefler için görüntüleyicide açık bir "kapsam yok" notu
> gösterildiği doğrulandı `[NV]`.

### 1.3 Kimlik Doğrulama
- [ ] Giriş sayfası açılıyor `[NV]`
- [ ] Geçerli kullanıcı adı/şifre ile oturum açılıyor `[NV]`
- [ ] Geçersiz giriş denemesi reddediliyor `[NV]`
- [ ] Oturum çıkışı çalışıyor `[NV]`

### 1.4 Altyapı — Docker + Caddy
- [ ] `docker compose up` komutu hatasız tamamlanıyor `[NV]`
- [ ] Caddy otomatik TLS sertifikası alıyor; HTTPS aktif `[NV]`
- [ ] HTTP → HTTPS yönlendirmesi çalışıyor `[NV]`
- [ ] Alan adı yapılandırması `{CADDY_DOMAIN}` ile eşleşiyor `[NV]` *(alan adı henüz belirlenmedi)*

### 1.5 Önbellek (Kiralık VM)
- [ ] Önbellek dizini dolu; sık kullanılan karolar disk üzerinde mevcut `[NV]`
- [ ] VM yeniden başlatıldıktan sonra önbellek korunuyor `[ASSUMPTION]`

### 1.6 Testler
- [ ] `pytest` çalışıyor; tüm testler yeşil `[NV]`
- [ ] Test kapsamı ≥ %80 `[NV]`
- [ ] CI/CD boru hattı (yoksa manuel kontrol tamamlandı) `[NV]`

---

## 2. Demo Hazırlığı

### 2.1 Senaryo ve Prova
- [ ] Demo senaryosu yazılı (adım adım tıklama akışı) `[NV]`
- [ ] Senaryo en az bir kez provası yapıldı `[NV]`
- [ ] Yedek demo planı hazır (ekran kaydı veya statik ekran görüntüleri) `[ASSUMPTION]`

### 2.2 Açılış Konuşması
- [ ] 2 dakikalık açılış konuşması metni hazır `[NV]`
- [ ] Konuşma provası yapıldı `[NV]`
- [ ] Jüriye yönelik temel mesaj netleştirildi `[NV]`

### 2.3 Sunum Slaytları
- [ ] Slayt dosyası `docs/slides/09-03` dizininde mevcut `[NV]`
- [ ] Slaytlar proje adı, logo ve takım üyelerini içeriyor `[NV]`
- [ ] Teknik mimari diyagramı eklenmiş `[NV]`
- [ ] Demo URL'si / QR kodu slaytlarda yer alıyor `[NV]`

### 2.4 Jüri Soruları İçin Hazırlık
- [ ] "Neden NASA için önemli?" sorusuna cevap hazır `[NV]`
- [ ] "Ölçeklenebilirlik nasıl sağlanıyor?" sorusuna cevap hazır `[NV]`
- [ ] "Veri kaynakları neler?" sorusuna cevap hazır `[NV]`
- [ ] "Takım rolleri nasıl dağıldı?" sorusuna cevap hazır `[NV]`
- [ ] "Gelecek planları neler?" sorusuna cevap hazır `[NV]`

---

## 3. Belgeleme

- [ ] `README.md` güncel; kurulum ve çalıştırma talimatları doğru `[NV]`
- [ ] `docs/STATUS.md` demo öncesi son durum ile güncellendi `[NV]`
- [ ] `docs/RISKS.md` kapanış koşulları bölümü dolduruldu `[NV]`
- [ ] `CREDITS.md` tüm takım üyelerini, açık kaynak kütüphanelerini ve NASA veri kaynaklarını kapsıyor `[NV]`
- [ ] `COMPETITION_RULES.md` okundu ve takım adına imzalandı / onaylandı `[NV]`

---

## 4. Güvenlik

- [ ] `.env` dosyası `.gitignore` içinde; repo'ya push edilmemiş `[NV]`
- [ ] `git log --all -- .env` komutu ile geçmişe sızmadığı doğrulandı `[NV]`
- [ ] Kullanıcı şifreleri bcrypt ile hash'lenmiş `[NV]`
- [ ] Kaynak kodda gömülü API anahtarı yok `[NV]`
- [ ] S3 kovası anonim okuma ile erişilebilir; gizli kimlik bilgisi kullanılmıyor `[NV]`
- [ ] Rate limiting (giriş ve API uç noktaları için) aktif `[NV]`
- [ ] Hata mesajları hassas bilgi sızdırmıyor `[NV]`

---

## 5. Son Push ve Dağıtım

- [ ] `main` branch güncel; bekleyen pull request yok `[NV]`
- [ ] `git status` temiz (uncommitted değişiklik yok) `[NV]`
- [ ] CI/CD geçiyor; yoksa manuel smoke-test tamamlandı `[NV]`
- [ ] Demo VM üzerinde en son kod çekilerek ayağa kaldırıldı `[NV]`
- [ ] VM üzerinde uçtan uca manuel test yapıldı `[NV]`

---

## 6. Sunum Linki / QR Kodu

- [ ] Demo URL'si jüri öncesinde teyit edildi: `https://{CADDY_DOMAIN}` — *alan adı henüz belirlenmedi* `[NV]`
- [ ] QR kodu oluşturuldu ve basılı materyal/slayta eklendi `[NV]`
- [ ] URL, demo süresince kesintisiz erişilebilir durumda `[NV]`

---

## Notlar

- **Alan C** sunucu ve hesap yönetiminden sorumludur; kiralık VM erişimi ona bağlıdır `[V]`.
- **Son teslim tarihi** henüz belirlenmemiştir; bu kontrol listesi belirlendikten sonra güncellenmelidir `[NV]`.
- Tüm `[NV]` maddeleri en geç demo gününden bir gün önce `[V]` durumuna getirilmelidir `[ASSUMPTION]`.
