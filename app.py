from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'minishop-gizli-anahtar-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ──────────────────────────────────────────
# VERİTABANI MODELLERİ
# ──────────────────────────────────────────

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default='')
    price       = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, default=0)
    image_url   = db.Column(db.String(300), default='')

class CartItem(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity   = db.Column(db.Integer, default=1)
    product    = db.relationship('Product')

# ──────────────────────────────────────────
# YARDIMCI FONKSİYONLAR
# ──────────────────────────────────────────

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Bu sayfaya erişmek için giriş yapmalısın.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Bu sayfaya sadece admin girebilir.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# ──────────────────────────────────────────
# KULLANICI ROTALARI
# ──────────────────────────────────────────

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten alınmış!', 'danger')
            return redirect(url_for('register'))

        hashed = generate_password_hash(password)
        user = User(username=username, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Giriş yapabilirsin.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id']  = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash(f'Hoş geldin, {user.username}! 👋', 'success')
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('index'))

# ──────────────────────────────────────────
# SEPET ROTALARI
# ──────────────────────────────────────────

@app.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(i.product.price * i.quantity for i in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    if product.stock <= 0:
        flash('Ürün stokta yok!', 'danger')
        return redirect(url_for('product_detail', product_id=product_id))

    existing = CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()

    if existing:
        existing.quantity += 1
    else:
        item = CartItem(user_id=session['user_id'], product_id=product_id)
        db.session.add(item)

    db.session.commit()
    flash(f'"{product.name}" sepete eklendi! 🛒', 'success')
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != session['user_id']:
        flash('Bu işlem için yetkiniz yok.', 'danger')
        return redirect(url_for('cart'))
    db.session.delete(item)
    db.session.commit()
    flash('Ürün sepetten kaldırıldı.', 'info')
    return redirect(url_for('cart'))

@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    qty  = int(request.form.get('quantity', 1))
    if qty < 1:
        db.session.delete(item)
    else:
        item.quantity = qty
    db.session.commit()
    return redirect(url_for('cart'))

# ──────────────────────────────────────────
# ADMİN ROTALARI
# ──────────────────────────────────────────

@app.route('/admin')
@admin_required
def admin_dashboard():
    products = Product.query.all()
    users    = User.query.all()
    return render_template('admin/dashboard.html', products=products, users=users)

@app.route('/admin/product/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    if request.method == 'POST':
        product = Product(
            name        = request.form['name'].strip(),
            description = request.form['description'].strip(),
            price       = float(request.form['price']),
            stock       = int(request.form['stock']),
            image_url   = request.form['image_url'].strip()
        )
        db.session.add(product)
        db.session.commit()
        flash('Ürün başarıyla eklendi! ✅', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_product.html')

@app.route('/admin/product/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name        = request.form['name'].strip()
        product.description = request.form['description'].strip()
        product.price       = float(request.form['price'])
        product.stock       = int(request.form['stock'])
        product.image_url   = request.form['image_url'].strip()
        db.session.commit()
        flash('Ürün güncellendi! ✅', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/edit_product.html', product=product)

@app.route('/admin/product/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    # Sepetteki ilgili itemları da sil
    CartItem.query.filter_by(product_id=product_id).delete()
    db.session.delete(product)
    db.session.commit()
    flash('Ürün silindi.', 'info')
    return redirect(url_for('admin_dashboard'))

# ──────────────────────────────────────────
# UYGULAMA BAŞLANGICI
# ──────────────────────────────────────────

with app.app_context():
    db.create_all()
    # Eğer admin yoksa oluştur
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username = 'admin',
            password = generate_password_hash('admin123'),
            is_admin = True
        )
        db.session.add(admin)
        db.session.commit()
        print('✅ Admin oluşturuldu: admin / admin123')

if __name__ == '__main__':
    app.run(debug=True)