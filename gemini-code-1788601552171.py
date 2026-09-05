import os
import re

# İlçe koordinat ve geo veritabanı
DISTRICT_DATA = {
    "atasehir": {"name": "Ataşehir", "lat": "40.9833", "lng": "29.1167"},
    "besiktas": {"name": "Beşiktaş", "lat": "41.0422", "lng": "29.0067"},
    "maltepe": {"name": "Maltepe", "lat": "40.9247", "lng": "29.1307"},
    "sisli": {"name": "Şişli", "lat": "41.0602", "lng": "28.9877"},
    "uskudar": {"name": "Üsküdar", "lat": "41.0267", "lng": "29.0167"},
    "cekmekoy": {"name": "Çekmeköy", "lat": "41.0350", "lng": "29.1730"},
}

def update_kedi_oteli(html_content):
    schema_code = """
  <!-- Otomatik Eklenen SEO / GEO Şeması -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "PetService",
    "name": "KediOteli.net - Kedi Oteli ve Evde Bakım Hizmeti",
    "url": "https://www.kedioteli.net/kedi-oteli.html",
    "serviceType": ["Kedi Oteli", "Evde Kedi Bakımı", "Kedi Pansiyonu"],
    "areaServed": [{"@type": "City", "name": "İstanbul"}]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "Kedi oteli mi yoksa evde kedi bakımı mı tercih edilmeli?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Ortam değişikliğinden stres yaşayan kediler için kendi evlerinde kalıp günlük profesyonel ziyaretlerle bakılmaları çok daha konforludur."
        }
      },
      {
        "@type": "Question",
        "name": "Evde kedi bakımı hizmeti nasıl planlanır?",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "Tarih ve hizmet bölgesi paylaşıldıktan sonra kedinizin mama, kum, oyun ve varsa ilaç rutini netleştirilir; planlanan saatlerde periyodik ziyaretler gerçekleştirilir."
        }
      }
    ]
  }
  </script>
</head>"""
    if "KediOteli.net - Kedi Oteli ve Evde Bakım Hizmeti" not in html_content:
        return html_content.replace("</head>", schema_code)
    return html_content

def update_district_page(html_content, key, info):
    if f"geo.placename\" content=\"{info['name']}" in html_content:
        return html_content

    geo_and_schema = f"""
  <!-- Otomatik Eklenen GEO Meta & Schema -->
  <meta name="geo.region" content="TR-34" />
  <meta name="geo.placename" content="{info['name']}, İstanbul" />
  <meta name="geo.position" content="{info['lat']};{info['lng']}" />
  <meta name="ICBM" content="{info['lat']}, {info['lng']}" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "PetService",
    "name": "Kedi Bakımı ve Oteli - {info['name']}",
    "serviceType": "Kedi Bakımı, Kedi Oteli ve Pansiyonu",
    "areaServed": "{info['name']}, İstanbul",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{info['name']}",
      "addressRegion": "İstanbul",
      "addressCountry": "TR"
    }}
  }}
  </script>
</head>"""
    return html_content.replace("</head>", geo_and_schema)

def run():
    files = [f for f in os.listdir(".") if f.endswith(".html")]
    print(f"Toplam {len(files)} HTML dosyası bulundu. Güncelleme başlıyor...")

    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            content = file.read()

        updated_content = content

        if f == "kedi-oteli.html":
            updated_content = update_kedi_oteli(content)
            print(f"[+] Güncellendi: {f}")
        else:
            for district_key, info in DISTRICT_DATA.items():
                if f.startswith(district_key):
                    updated_content = update_district_page(content, district_key, info)
                    print(f"[+] GEO & Şema Eklendi: {f}")
                    break

        if updated_content != content:
            with open(f + ".bak", "w", encoding="utf-8") as bak:
                bak.write(content)
            with open(f, "w", encoding="utf-8") as file:
                file.write(updated_content)

    print("İşlem tamamlandı! Dosyaların orijinal halleri .bak olarak yedeklendi.")

if __name__ == "__main__":
    run()