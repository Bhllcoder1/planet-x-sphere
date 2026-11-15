# Sır Yönetimi — planet-x-sphere

Bu belge, projede API anahtarlarının ve diğer hassas bilgilerin nasıl yönetileceğini tanımlar.

---

## 1. Temel Kural: `.env` Asla Commit Edilmez

**[V]** `.env` dosyası gerçek sırları içerir ve sürüm kontrolüne alınmamalıdır.  
**[V]** `.env.example` dosyası şablondur; gerçek değer içermez ve tracked (izlenen) tutulur.

| Dosya | Git durumu | Açıklama |
|---|---|---|
| `c_sunucu/.env` | **Yoksayılır** | Gerçek sırlar — asla commit etme |
| `c_sunucu/.env.example` | **İzlenir** | Boş şablon — commit edilir |

---

## 2. `.gitignore` Kontrol Listesi

Aşağıdaki kalıplar projenin `.gitignore` dosyasında bulunmalıdır:

```gitignore
# Ortam değişkenleri
.env
.env.local
.env.*.local

# TLS sertifikaları ve özel anahtarlar
*.pem
*.key
*.crt
*.p12
*.pfx

# Seed dosyaları (şifreli olsa bile repoya girmez)
*_seed.json

# IDE ve OS artıkları
.DS_Store
Thumbs.db
```

**[V]** `.env.example` dosyası bu kalıpların hiçbirine uymaz; kasıtlı olarak izlenir.  
**[ASSUMPTION]** `users_seed.json` dosyası bcrypt hash'li parolalar içerdiğinden `*_seed.json` kalıbıyla yoksayılır.

---

## 3. Sır Tarama Komutu

Commit öncesinde veya CI/CD boru hattında aşağıdaki komutu çalıştır:

```bash
git grep -I -n -E "(password|secret|key|token)\s*=" --cached
```

Bu komut:
- `--cached` → yalnızca sahneye alınmış (staged) dosyaları tarar
- `-I` → ikili (binary) dosyaları atlar
- `-n` → satır numarası gösterir
- `-E` → genişletilmiş regex kullanır

Çıktı üretirse commit durdurulmalı ve eşleşen satırlar gözden geçirilmelidir.

**[V]** Bu komut, anahtar kelimeyi içeren yorumları da yakalar; kasıtlı değerler `# NOCOMMIT` etiketiyle işaretlenebilir ve elle doğrulanabilir.

Ek tarama için `trufflehog` veya `gitleaks` araçları da kullanılabilir:

```bash
# gitleaks ile tarama
gitleaks detect --source . --no-git
```

---

## 4. VM'ye Dağıtım Adımları

### 4a. `.env` dosyasını VM'ye kopyala

```bash
# Yerel makineden kiralık VM'ye güvenli kopyalama
scp c_sunucu/.env deploy@<VM_IP>:/opt/planet-x-sphere/c_sunucu/.env
```

**[ASSUMPTION]** Dağıtım kullanıcısı `deploy` ve uygulama dizini `/opt/planet-x-sphere/` olarak varsayılmıştır; ortama göre güncelle.

### 4b. VM'de dosya izinlerini kısıtla

```bash
# Yalnızca sahip kullanıcı okuyabilsin
chmod 600 /opt/planet-x-sphere/c_sunucu/.env
chown deploy:deploy /opt/planet-x-sphere/c_sunucu/.env
```

### 4c. Docker Compose `.env` dosyasını otomatik okur

`docker-compose.yml` ile aynı dizinde bulunan `.env` dosyası Docker Compose tarafından otomatik yüklenir.  
Farklı bir yol kullanılıyorsa `--env-file` bayrağını belirt:

```bash
docker compose --env-file c_sunucu/.env up -d
```

**[V]** `docker-compose.yml` içindeki servisler `${APP_SECRET_KEY}` sözdizimi ile ortam değişkenlerine erişir; Docker imajına gömülmez.

---

## 5. Sır Rotasyonu

### APP_SECRET_KEY Yenileme

`APP_SECRET_KEY`, JWT imzalama ve oturum şifreleme için kullanılır.

```bash
# Yeni rastgele 32 bayt hex anahtar üret
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Adımlar:
1. Yeni anahtarı üret.
2. VM'deki `.env` dosyasını güncelle.
3. Uygulamayı yeniden başlat: `docker compose restart api`
4. **Dikkat:** Mevcut oturumlar geçersiz olur; kullanıcıların yeniden giriş yapması gerekir.

### SESSION anahtarı Yenileme

`SESSION_COOKIE_NAME` değeri değiştirilirse tarayıcıdaki eski çerezler oturumu sonlandırır.  
Yalnızca güvenlik ihlali durumunda değiştir; rutin rotasyon gerekmez.

**[V]** Anahtar rotasyonu planlı bir bakım penceresi gerektirmez; uygulama yeniden başlatma (~2 saniye) yeterlidir.

---

## 6. Özel Uyarılar

### S3 Anonim Erişim

**[V]** `nasa-irsa-spherex` kovası kamuya açık anonim erişime izin verir.  
**[V]** `AWS_ACCESS_KEY_ID` veya `AWS_SECRET_ACCESS_KEY` değişkenleri **gerekli değildir** ve `.env` dosyasına eklenmemelidir.  
S3 istemcisi `botocore.UNSIGNED` yapılandırmasıyla başlatılır:

```python
from botocore import UNSIGNED
from botocore.config import Config
import boto3

s3 = boto3.client(
    "s3",
    region_name="us-east-1",
    config=Config(signature_version=UNSIGNED),
)
```

Anahtar içeren konfigürasyon yanlışlıkla eklendiyse derhal kaldır ve git geçmişini temizle.

### Kullanıcı Parolaları — Seed Dosyası

**[V]** `users_seed.json` içindeki parolalar **bcrypt** ile hash'lenmiştir; düz metin içermez.  
**[ASSUMPTION]** Bununla birlikte seed dosyası kullanıcı adı ve e-posta gibi kişisel veri içerebilir; bu nedenle `*_seed.json` kalıbıyla repoya alınmaz ve ayrıca şifrelenmiş kanallarla (scp/SFTP) aktarılır.

---

*Son güncelleme: görev 06-10*
