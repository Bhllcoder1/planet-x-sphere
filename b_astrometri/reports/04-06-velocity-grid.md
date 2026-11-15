# 04-06 — Seyrek hız ızgarası ve konsensüs iyileştirmesi

Kaynak: `b_astrometri/movers/linker.py`. Görev: https://app.clickup.com/t/z8qu5ddjx8

## Uygulanan dilim

Önceki tam iki-nokta hipotezleri artık deterministik bir hız kafesine oy verir. Kafes bileşen adımı `min(1 px, residual_tol_px) / (sqrt(2) × T_saat)` olarak tanımlanır; dolayısıyla komşu çapraz hücrelerin hız farkı × toplam zaman en çok 1 pikseldir. Yalnız tespit çiftlerinin desteklediği hücreler, çiftin ilk tespitine bağlı konumla değerlendirilir. **Bütün hız alanı taranmıyor**; çıktı bunu `full_velocity_grid_searched=False` ile açıkça bildirir.

Aynı hücre/başlangıç tespitindeki yinelenen hipotezler birleştirilir; saklanan ilk çiftin `seed_pair_refs` ve gerçek çift hızı korunur. Yuvarlanmış hız izin verilen hız halkasının dışına taşarsa sınırdaki çift sessizce kaybolmaz: o çiftin gerçek hızı kullanılır ve `exact_boundary_pair` olarak işaretlenir. Son doğrusal uyumun hızı ayrıca min/max sınırlarından geçirilir.

Her hipotez kare başına en yakın tek tespitten konsensüs oluşturur. En çok beş konsensüs/least-squares yeniden uyum turu aykırı eşleri çıkarır ve diğer karelerdeki eşleri tekrar arar. Bu deterministik iki-nokta konsensüs yöntemidir; rastgele örnekleme yapıldığı iddia edilmez. Üç veya daha çok tespitli izde maksimum artık seçilen toleranstan küçük olmalıdır. İki tespit düşük güvenli aday olarak kalır. Üç kareden az geçişte bağlama kapalıdır.

`max_hypotheses=100000` bilimsel eşik değil, ayarlanabilir hesap bütçesidir. Katalog eşleşmesi olmayan tespit sayısından hesaplanan muhafazakâr çift sayısı bütçeyi aşarsa, ikinci dereceden statik taramadan önce `search_budget_exceeded` / `search_complete=False` döner. Izgara kabalaştırılmaz, tespit listesi kesilmez ve kısmi arama tamamlandı diye sunulmaz. Bütçe artırılması daha fazla CPU/bellek maliyeti doğurabilir.

`detection_refs` korunur. Statik çıkarılan tespitler nedenleriyle, kalan ama bağlanamayan tespitler kimlikleriyle raporlanır. Skor `N - 0.1×RMS` mevcut sıralama kuralıdır; kalibre edilmiş olasılık veya fiziksel kabul eşiği değildir. 10,6 px/saat varsayılan üst sınır ana-kuşak örneğinden gelir; hızlı NEO kapsamı doğrulanmadı.

## Önkoşullar ve doğrulama durumu

Girdi x/y değerleri bütün karelerde **aynı tangent düzlemi piksel sisteminde** olmalıdır. Kare-yerel piksel koordinatları burada WCS ile taşınmaz. Kanonik geçiş listesi, gerçek tespit katalogları ve WCS düzeltmesi hâlâ üretim entegrasyonu önkoşullarıdır.

Kullanıcının “şimdi test yok” talimatı nedeniyle **bu değişiklik için test eklenmedi ve çalıştırılmadı**; yalnız kaynak akışı statik olarak gözden geçirildi. Gerçek asteroit izi, `<1 px` gerçek veri artığı ve iz çizimi üretilmedi. Bu dilim 04-06'nın tamamlandığı anlamına gelmez.
