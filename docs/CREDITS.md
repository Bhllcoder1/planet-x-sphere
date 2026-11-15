# Atıflar ve Krediler

**Proje:** Planet-X-Sphere — NASA Space Apps SPHEREx 5 Hedef Görüntüleyici  
**Tarih:** 2026-11-15  
**Durum notu:** `[V]` = doğrulandı, `[NV]` = henüz teyit bekleniyor

---

## 1. NASA ve Veri Kaynakları

### SPHEREx — NASA/JPL-Caltech

- **Misyon sahibi:** NASA/JPL-Caltech
- **Arşiv:** NASA/IPAC Infrared Science Archive (IRSA)
- **DR1 S3 kovası:** `nasa-irsa-spherex` (anonim erişim, kimlik doğrulama gerekmez) `[V]`
- **Doğrulama:** `s0_A` ve `s0_B` testlerinde S3 erişimi başarıyla doğrulandı `[V: s0_A, s0_B]`
- **Resmi sayfa:** <https://www.jpl.nasa.gov/missions/spherex>

### IRSA TAP Servisi — Caltech/IPAC

- **Sağlayıcı:** California Institute of Technology / IPAC
- **Uç nokta:** `https://irsa.ipac.caltech.edu/TAP`
- **Kullanım amacı:** SPHEREx katalog sorgulama ve zaman serisi erişimi
- **Resmi sayfa:** <https://irsa.ipac.caltech.edu>

### SkyBoT — IMCCE, Paris Gözlemevi

- **Sağlayıcı:** Institut de Mécanique Céleste et de Calcul des Éphémérides (IMCCE)
- **Kurum:** Paris Gözlemevi, Fransa
- **Kullanım amacı:** Asteroid efemeris ve küçük cisim örtüşme kontrolü
- **Resmi sayfa:** <https://ssp.imcce.fr/webservices/skybot/>

### Gaia DR3 — ESA/Gaia/DPAC

- **Sağlayıcı:** European Space Agency (ESA) / Gaia Data Processing and Analysis Consortium (DPAC)
- **Kullanım amacı:** Referans katalog, WCS (Dünya Koordinat Sistemi) doğrulama
- **Resmi sayfa:** <https://www.cosmos.esa.int/web/gaia/dr3>

### SIMBAD — CDS, Strasbourg

- **Sağlayıcı:** Centre de Données astronomiques de Strasbourg (CDS)
- **Kullanım amacı:** Hedef isim çözümleme ve astronomi nesnesi arama
- **Resmi sayfa:** <https://simbad.u-strasbg.fr/simbad/>

---

## 2. Python Kütüphaneleri

Projede kullanılan başlıca Python bağımlılıkları ve lisansları:

| Kütüphane | Lisans | Kullanım Amacı |
|-----------|--------|----------------|
| `astropy` | BSD-3-Clause | FITS okuma, WCS işleme, koordinat dönüşümleri |
| `numpy` | BSD-3-Clause | Sayısal hesaplama, dizi işlemleri |
| `FastAPI` | MIT | REST API sunucusu |
| `httpx` | BSD-3-Clause | Asenkron HTTP istekleri |
| `pydantic` | MIT | Veri doğrulama ve şema yönetimi |
| `bcrypt` | Apache-2.0 | Parola hashleme |
| `uvicorn` | BSD-3-Clause | ASGI sunucu |

Tam bağımlılık listesi için: `c_sunucu/requirements.txt`

---

## 3. Altyapı

### Caddy

- **Lisans:** Apache-2.0
- **Kullanım amacı:** TLS sertifika yönetimi ve ters proxy (reverse proxy)
- **Resmi sayfa:** <https://caddyserver.com>

### Docker

- **Lisans:** Apache-2.0
- **Kullanım amacı:** Konteyner tabanlı dağıtım ve ortam yönetimi
- **Resmi sayfa:** <https://www.docker.com>

### GitHub

- **Sağlayıcı:** Microsoft / GitHub, Inc.
- **Kullanım amacı:** Kaynak kod barındırma, sürüm kontrolü

---

## 4. İlham ve Referans Alınan Çalışmalar

### WiseView

- **Kaynak:** WISE/unWISE gök cismi gezgini
- **İlham:** Görüntüleyici arayüz tasarımı ve zaman serisi gezinme deneyimi
- **Resmi sayfa:** <http://byw.tools/wiseview>

### astropy.io.fits

- **Kullanım:** FITS dosya okuma ve başlık işleme referans uygulaması
- **Belge:** <https://docs.astropy.org/en/stable/io/fits/>

---

## 5. Ekip

| Üye | Alan | GitHub / İletişim |
|-----|------|-------------------|
| Alan C — Sunucu geliştirme, hesap yönetimi | Backend, API, kimlik doğrulama | newernever |
| Alan A | `[NV]` | `[NV]` |
| Alan B | `[NV]` | `[NV]` |
| Alan D | `[NV]` | `[NV]` |

> Diğer ekip üyelerinin isimleri ve katkı alanları teyit bekleniyor. `[NV]`

---

## 6. Lisans Bilgileri

- **Proje kaynak kodu:** MIT veya Apache-2.0 (henüz kesinleşmedi) `[NV]`
- **SPHEREx verileri:** NASA kamu malı (public domain); NASA veri politikası geçerlidir
- **Gaia DR3 verileri:** ESA; Gaia DPAC lisans koşulları geçerlidir
- **SkyBoT verileri:** IMCCE, akademik ve araştırma amaçlı serbestçe kullanılabilir

---

*Bu dosya Görev 09-09 kapsamında oluşturulmuştur.*
