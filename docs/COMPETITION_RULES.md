# Yarışma Kuralları ve Uyumluluk Belgesi

**Proje:** Planet-X Sphere — SPHEREx Veri Keşif Aracı  
**Hackathon:** NASA Space Apps Challenge  
**Tarih:** 2026-11-15  
**Versiyon:** 1.0  
**Durum:** `[ASSUMPTION]` — Resmi NASA Space Apps kural metni mevcut değil; bu belge iyi huylu varsayımlarla taslak olarak yazılmıştır. Resmi kurallar için [nasa.gov/spaceapps](https://www.nasa.gov/spaceapps) kontrolü önerilir.

---

## 1. İzin Verilen Veri Kaynakları

Aşağıdaki veri kaynakları projede kullanılmaktadır. Tamamı kamuya açık veya açık lisanslıdır.

| Kaynak | Açıklama | Erişim Türü | Durum |
|--------|----------|-------------|-------|
| **NASA IRSA / SPHEREx** | SPHEREx görev katalogları ve görüntüleri | Anonim S3, ücretsiz | `[V]` |
| **IRSA TAP Servisi** | IVOA TAP protokolü ile katalog sorguları | Herkese açık REST/TAP | `[V]` |
| **NASA/IPAC Extragalactic Database (NED)** | Galaksi dışı nesne kataloğu | Kamuya açık API | `[V]` |
| **SIMBAD** | Astronomik nesne kimlik kataloğu (CDS, Strasbourg) | Kamuya açık | `[V]` |
| **SkyBoT** | Güneş Sistemi hareketli cisim servisi (IMCCE) | Kamuya açık | `[V]` |
| **Gaia DR3** | ESA Gaia üçüncü veri yayımı; astrometri ve fotometri | Kamuya açık | `[V]` |
| **unWISE / WISE** | NASA WISE kızılötesi gökyüzü araştırması | Kamuya açık | `[V]` |
| **OpenStreetMap** | Harita kiremit servisi (gökyüzü koordinat arayüzü için) | MIT lisansı | `[V]` |

> **Not `[V]`:** Erişim testleri proje geliştirme sürecinde doğrulanmıştır.  
> **Not `[NV]`:** TAP/ADQL sorgu yanıt formatı tam kapsamda test edilmemiştir; kenar durumlar doğrulama beklemektedir.

---

## 2. İzin Verilmeyen Kullanımlar

Aşağıdaki kategoriler NASA Space Apps kuralları ve açık kaynak uyumluluğu çerçevesinde **yasaktır**:

### 2.1 Lisanslı veya Ücretli Veriler
- `[ASSUMPTION]` Ücretli üçüncü taraf astronomi API'leri (örn. ticari gökyüzü kataloğu abonelikleri) kullanılamaz.
- Hackathon kapsamı dışında erişim kısıtlaması bulunan veri setleri dahil edilemez.

### 2.2 Özel veya Paylaşılamayan Veri Setleri
- `[ASSUMPTION]` Yalnızca belirli kurumlara açık, kamuya erişilemeyen iç veri setleri kullanılamaz.
- Proje sunumunda ve kod tabanında referans verilen tüm veri kaynaklarının bağlantı veya DOI bilgisi paylaşılmalıdır.

### 2.3 Telif Hakkı İhlali
- Lisans bilgisi belirsiz üçüncü taraf görseller, haritalar veya yazılım bileşenleri eklenemez.
- Başka ekiplerin veya bireylerin yayımlanmış kodları kaynak gösterilmeksizin kullanılamaz.

---

## 3. Kaynak Atıfları

### 3.1 Veri Kaynakları

**SPHEREx Görevi**  
> SPHEREx verileri NASA/JPL-Caltech tarafından sağlanmaktadır.  
> Küçük cisim tespiti ve katalog aramaları NASA/IPAC Infrared Science Archive (IRSA) üzerinden gerçekleştirilmektedir.  
> `[V]` Resmi atıf: *"This work makes use of data from the SPHEREx mission, provided by NASA/JPL-Caltech and made available through the NASA/IPAC Infrared Science Archive (IRSA)."*

**Diğer Kataloglar**  
- CDS/SIMBAD: *"This research has made use of the SIMBAD database, operated at CDS, Strasbourg, France."* `[V]`
- NED: *"This research has made use of the NASA/IPAC Extragalactic Database (NED), which is funded by NASA and operated by the California Institute of Technology."* `[V]`
- Gaia DR3: *"This work has made use of data from the European Space Agency (ESA) mission Gaia."* `[V]`
- SkyBoT: *"This research made use of the SkyBoT service (IMCCE, Paris Observatory)."* `[V]`

### 3.2 Yazılım Bağımlılıkları

| Kütüphane / Araç | Lisans | Kullanım Amacı |
|-----------------|--------|----------------|
| **astropy** | BSD-3-Clause | Astronomik koordinat hesaplama, FITS okuma |
| **numpy** | BSD-3-Clause | Sayısal hesaplama |
| **FastAPI** | MIT | Backend REST API sunucusu |
| **Caddy** | Apache-2.0 | Ters proxy ve TLS yönetimi |
| **Uvicorn** | BSD-3-Clause | ASGI sunucusu |
| **Pydantic** | MIT | Veri doğrulama |
| **httpx / aiohttp** | BSD-3-Clause / Apache-2.0 | Asenkron HTTP istemcisi |
| **Leaflet.js** | BSD-2-Clause | Harita görüntüleme (tarayıcı tarafı) |
| **OpenStreetMap kiremitleri** | ODbL | Harita arkaplanı |

> `[NV]` Bağımlılık lisans listesi son paket sürümleri için tam doğrulama beklemektedir; `pip-licenses` veya `license-checker` çalıştırılarak teyit edilmelidir.

---

## 4. Gizlilik ve Telif Hakkı

### 4.1 Kullanıcı Hesapları
- `[V]` Sistemde **10 sabit kullanıcı hesabı** tanımlıdır; bunlar yalnızca hackathon demosu ve jüri değerlendirmesi içindir.
- `[ASSUMPTION]` Bu hesaplar genel kullanıma açılmayacaktır; proje kamuya açık bir kimlik doğrulama sistemi barındırmamaktadır.

### 4.2 Kullanıcı Verilerinin İşlenmesi
- `[V]` Oturum ve arama geçmişi yalnızca bellek içinde (in-memory) veya istemci tarafında (yerel depolama) tutulmaktadır.
- `[V]` Kullanıcı verileri herhangi bir üçüncü taraf servisine gönderilmemektedir.
- `[ASSUMPTION]` Kullanıcı girişi (koordinat, nesne adı) yalnızca ilgili kamuya açık astronomi API'lerine iletilir; başka amaçla saklanmaz.
- Proje GDPR veya KVKK yükümlülüğü doğuracak kişisel veri toplamamaktadır.

### 4.3 Kod Lisansı
- `[ASSUMPTION]` Proje kodu açık kaynak uyumlu bir lisans altında yayımlanacaktır: **MIT** veya **Apache 2.0** (ekip kararına bağlı).
- Üçüncü taraf bileşenler kendi lisansları kapsamında kalmaya devam eder (bkz. Bölüm 3.2).

### 4.4 SPHEREx Verilerinin Telif Hakkı Durumu
- `[V]` SPHEREx verileri NASA tarafından üretilmiş olup **ABD kamu malı** (US Government Work) kapsamındadır.
- Ticari kullanım dahil yeniden dağıtım serbesttir; kaynak atfı iyi uygulama olarak önerilir (bkz. Bölüm 3.1).

---

## 5. Proje İçi Dürüstlük Kuralları

### 5.1 Etiket Sistemi

Projede üretilen tüm bulgular, iddialar ve varsayımlar aşağıdaki etiketlerle işaretlenir:

| Etiket | Anlamı |
|--------|--------|
| `[V]` | **Doğrulandı** — Kod, test veya resmi belge ile doğrulanmıştır |
| `[NV]` | **Doğrulanmadı** — Makul görünmektedir; ancak henüz test edilmemiştir |
| `[ASSUMPTION]` | **Varsayım** — Resmi kaynak mevcut değil; mantıksal çıkarım veya iyi huylu tahmindir |

> Tüm ekip üyeleri (`A`, `B`, `C`, `D` alanları) belge ve kod yorumlarında bu etiket kuralına uymakla yükümlüdür.

### 5.2 Doğrulanmamış Sonuçların İşaretlenmesi
- API yanıtından türetilen her sonuç, doğrulama tamamlanana kadar `[NV]` olarak işaretlenir.
- Kullanıcı arayüzünde gösterilen ve kesin olarak doğrulanamayan değerler görsel olarak ayırt edilir (örn. gri renk, belirsizlik simgesi).

### 5.3 Hareketli Cisim (Mover) Tespiti
- `[ASSUMPTION]` ePSF (Effective Point Spread Function) doğrulaması tamamlanmadan tespit edilen cisimler **"aday (candidate)"** olarak sınıflandırılır; **"tespit (detection)"** değildir.
- Kullanıcı arayüzünde bu ayrım açıkça belirtilir: *"Bu nesne aday statüsündedir; bağımsız doğrulama önerilir."*
- Yanlış pozitif riskini azaltmak için SkyBoT çapraz eşleştirme sonucu her adayın yanında gösterilir.

### 5.4 Ekip Sorumlulukları

| Alan | Sorumlu | Kapsam |
|------|---------|--------|
| **A** | Veri alımı ve API entegrasyonu | Kaynak atıfları, lisans kontrolü |
| **B** | Backend (FastAPI, Caddy) | Güvenlik, hata yönetimi |
| **C** | Ön yüz (görsel arayüz) | Kullanıcı gizliliği, `[NV]` gösterimi |
| **D** | Bilim doğrulaması (astrofizik) | `[V]` / `[NV]` / `[ASSUMPTION]` etiketlemesi |

---

## 6. Referanslar

- NASA Space Apps Challenge resmi kurallar: <https://www.nasa.gov/spaceapps> `[ASSUMPTION]`
- SPHEREx görev sayfası: <https://spherex.caltech.edu>
- NASA IRSA: <https://irsa.ipac.caltech.edu>
- Astropy proje: <https://www.astropy.org>
- SIMBAD: <https://simbad.cds.unistra.fr>
- NED: <https://ned.ipac.caltech.edu>
- SkyBoT: <https://vo.imcce.fr/webservices/skybot/>
- Gaia DR3: <https://www.cosmos.esa.int/web/gaia/dr3>

---

*Bu belge `[ASSUMPTION]` etiketiyle açıklandığı üzere resmi NASA Space Apps kural metnine dayanmamaktadır. Yarışma başlamadan önce resmi kural sayfası incelenmeli ve bu belge gerekiyorsa güncellenmelidir.*
