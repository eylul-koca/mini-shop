# 🛒 Eticaret — Flask E-Ticaret Uygulaması

> Python & Flask ile geliştirilmiş, tam işlevsel bir e-ticaret web uygulaması.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🌐 Canlı Demo

👉 **[https://eticaret-sslx.onrender.com](https://eticaret-sslx.onrender.com)**

> Admin girişi: `admin` / `admin123`

---

## 📸 Ekran Görüntüleri

| Ana Sayfa | Admin Panel |
|-----------|------------|
| ![Ana Sayfa](screenshots/home.png) | ![Admin](screenshots/admin.png) |

---

## ✨ Özellikler

### 👤 Kullanıcı Tarafı
- 🏠 Ürün listeleme sayfası
- 🔍 Anlık ürün arama
- 📄 Ürün detay sayfası
- 🛒 Sepete ekleme & güncelleme & silme
- 🔐 Kayıt ol / Giriş yap / Çıkış yap

### ⚙️ Admin Paneli
- 📦 Ürün ekleme, düzenleme, silme
- 📊 İstatistik kartları (toplam ürün, kullanıcı, stok)
- 🏷️ Stok durumu takibi

### 🛠️ Teknik
- 🔑 Session tabanlı kimlik doğrulama
- 🔒 Şifre hash'leme (Werkzeug)
- 🗄️ SQLite veritabanı (SQLAlchemy ORM)
- 📱 Responsive tasarım (mobil uyumlu)
- ⚡ Flash mesaj sistemi

---

## 🏗️ Proje Yapısı

```
flask/
├── app.py                  # Ana uygulama & route'lar
├── requirements.txt        # Bağımlılıklar
├── render.yaml             # Render.com deploy ayarları
├── instance/
│   └── database.db         # SQLite veritabanı
├── static/
│   ├── css/
│   │   └── style.css       # Tüm stiller
│   └── js/
│       └── main.js         # JavaScript fonksiyonları
└── templates/
    ├── base.html           # Ana şablon
    ├── index.html          # Ana sayfa
    ├── product.html        # Ürün detay
    ├── cart.html           # Sepet
    ├── login.html          # Giriş
    ├── register.html       # Kayıt
    └── admin/
        ├── dashboard.html  # Admin paneli
        ├── add_product.html
        └── edit_product.html
```

---

## 🚀 Yerel Kurulum

### Gereksinimler
- Python 3.11+
- pip

### Adımlar

```bash
# 1. Repoyu klonla
git clone https://github.com/eylul-koca/eticaret.git
cd eticaret

# 2. Sanal ortam oluştur
python -m venv venv

# 3. Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. Uygulamayı çalıştır
python app.py
```

Tarayıcıda aç: **http://127.0.0.1:5000**

---

## 🗄️ Veritabanı Modelleri

| Model | Alanlar |
|-------|---------|
| `User` | id, username, password (hash), is_admin |
| `Product` | id, name, description, price, stock, image_url |
| `CartItem` | id, user_id, product_id, quantity |

---

## 🔌 API Endpoint'leri

| Method | URL | Açıklama |
|--------|-----|----------|
| GET | `/` | Ana sayfa — ürün listesi |
| GET | `/product/<id>` | Ürün detay sayfası |
| POST | `/cart/add/<id>` | Sepete ürün ekle |
| GET | `/cart` | Sepeti görüntüle |
| POST | `/cart/update/<id>` | Sepet miktarını güncelle |
| GET | `/cart/remove/<id>` | Sepetten ürün kaldır |
| GET/POST | `/login` | Giriş yap |
| GET/POST | `/register` | Kayıt ol |
| GET | `/logout` | Çıkış yap |
| GET | `/admin` | Admin dashboard |
| GET/POST | `/admin/product/add` | Ürün ekle |
| GET/POST | `/admin/product/edit/<id>` | Ürün düzenle |
| POST | `/admin/product/delete/<id>` | Ürün sil |

---

## 🛠️ Kullanılan Teknolojiler

| Teknoloji | Versiyon | Kullanım Amacı |
|-----------|----------|----------------|
| Python | 3.11 | Backend dili |
| Flask | 3.0 | Web framework |
| SQLAlchemy | 3.1 | ORM / Veritabanı |
| Werkzeug | 3.0 | Şifre güvenliği |
| Jinja2 | 3.1 | HTML şablonlama |
| SQLite | — | Veritabanı |
| HTML/CSS/JS | — | Frontend |
| Gunicorn | 21.2 | Production sunucu |
| Render.com | — | Cloud deployment |

---

## 🔮 Gelecek Özellikler

- [ ] Sipariş geçmişi sayfası
- [ ] Ürün kategorileri & filtreleme
- [ ] Ürün yorumları & puanlama sistemi
- [ ] REST API (JSON response)
- [ ] Kullanıcı profil sayfası
- [ ] Gerçek ödeme entegrasyonu (Stripe/iyzico)

---

## 👩‍💻 Geliştirici

**Eylül Koca**

[![GitHub](https://img.shields.io/badge/GitHub-eylul--koca-black?style=flat-square&logo=github)](https://github.com/eylul-koca)

---

## 📄 Lisans

Bu proje MIT lisansı ile lisanslanmıştır.