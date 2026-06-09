from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash  # type: ignore
import json
import os
import uuid
import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'change-this-in-production')

BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'database')
os.makedirs(DB, exist_ok=True)

MENU_FILE = os.path.join(DB, 'menu.json')
ADMIN_FILE = os.path.join(DB, 'admin_data.json')
TABLES_FILE = os.path.join(DB, 'tables_data.json')
TOTAL_TABLES = 15

# ─── Helpers ────────────────────────────────────────────────────────────────

def load_json(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_menu():
    src = os.path.join(BASE, '..', 'SRC', 'Authentication', 'Database', 'menu.json')
    if not os.path.exists(MENU_FILE) and os.path.exists(src):
        import shutil; shutil.copy(src, MENU_FILE)
    return load_json(MENU_FILE, {"Breakfast": [], "Lunch": [], "Dinner": [], "Beverages": []})

def init_tables():
    return {str(i): {"seats": 1 if i <= 3 else 2 if i <= 7 else 4, "bookings": {}} for i in range(1, TOTAL_TABLES + 1)}

def load_tables():
    data = load_json(TABLES_FILE, None)
    if not data:
        data = {"tables": init_tables()}
        save_json(TABLES_FILE, data)
    return data

def orders_file():
    return os.path.join(DB, f"{datetime.date.today()}_orders.json")

def load_orders():
    return load_json(orders_file(), [])

def save_orders(orders):
    save_json(orders_file(), orders)

def login_required(f):
    @wraps(f)
    def dec(*a, **kw):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*a, **kw)
    return dec

def admin_required(f):
    @wraps(f)
    def dec(*a, **kw):
        if session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('dashboard'))
        return f(*a, **kw)
    return dec

# ─── Auth Routes ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'customer':
            name = request.form.get('name', 'Guest').strip() or 'Guest'
            session['user'] = name
            session['role'] = 'customer'
            return redirect(url_for('dashboard'))
        else:
            admin_id = request.form['admin_id']
            password = request.form['password']
            admins = load_json(ADMIN_FILE, {})
            if admin_id in admins and admins[admin_id]['password'] == password:
                session['user'] = admins[admin_id]['name']
                session['admin_id'] = admin_id
                session['role'] = 'admin'
                return redirect(url_for('dashboard'))
            flash('Invalid admin credentials', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        admin_id = 'VS' + str(uuid.uuid4().int)[:3]
        admins = load_json(ADMIN_FILE, {})
        admins[admin_id] = {
            'admin_id': admin_id,
            'name': request.form['name'],
            'age': request.form['age'],
            'worktype': request.form['worktype'],
            'password': request.form['password']
        }
        save_json(ADMIN_FILE, admins)
        flash(f'Admin registered! Your ID: {admin_id}', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ─── Dashboard ──────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    orders = load_orders()
    tables = load_tables()['tables']
    booked = sum(1 for t in tables.values() if t['bookings'])
    menu = load_menu()
    total_items = sum(len(v) for v in menu.values())
    return render_template('dashboard.html', orders=orders, booked=booked,
                           available=TOTAL_TABLES - booked, total_items=total_items)

# ─── Menu Routes ────────────────────────────────────────────────────────────

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html', menu=load_menu())

@app.route('/menu/add', methods=['POST'])
@login_required
@admin_required
def add_menu_item():
    menu = load_menu()
    cat = request.form['category']
    name = request.form['item_name'].strip()
    if request.form.get('has_plates') == 'yes':
        item = {'item_name': name, 'half_plate_price': float(request.form['half_price']),
                'full_plate_price': float(request.form['full_price'])}
    else:
        item = {'item_name': name, 'item_price': float(request.form['item_price'])}
    menu.setdefault(cat, []).append(item)
    save_json(MENU_FILE, menu)
    flash(f'"{name}" added to {cat}', 'success')
    return redirect(url_for('menu'))

@app.route('/menu/delete/<category>/<int:idx>', methods=['POST'])
@login_required
@admin_required
def delete_menu_item(category, idx):
    menu = load_menu()
    if category in menu and 0 <= idx < len(menu[category]):
        removed = menu[category].pop(idx)
        save_json(MENU_FILE, menu)
        flash(f'"{removed["item_name"]}" removed', 'success')
    return redirect(url_for('menu'))

# ─── Order Routes ────────────────────────────────────────────────────────────

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    menu = load_menu()
    if request.method == 'POST':
        orders = load_orders()
        order_id = f"ORD{len(orders)+1:04d}"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_items = request.get_json()
        for item in new_items:
            item['order_id'] = order_id
            item['order_time'] = now
            item['customer'] = session.get('user', 'Guest')
            orders.append(item)
        save_orders(orders)
        return jsonify({'status': 'success', 'order_id': order_id})
    return render_template('order.html', menu=menu)

@app.route('/orders')
@login_required
def view_orders():
    orders = load_orders()
    return render_template('orders.html', orders=orders)

# ─── Billing Route ───────────────────────────────────────────────────────────

@app.route('/bill/<order_id>')
@login_required
def bill(order_id):
    orders = load_orders()
    items = [o for o in orders if o['order_id'] == order_id]
    if not items:
        flash('Order not found', 'danger')
        return redirect(url_for('view_orders'))
    subtotal = sum(i['price'] * i['quantity'] for i in items)
    gst = subtotal * 0.18
    total = subtotal + gst
    return render_template('bill.html', items=items, subtotal=subtotal,
                           gst=gst, total=total, order_id=order_id,
                           now=datetime.datetime.now().strftime("%d %b %Y, %H:%M"))

# ─── Table Routes ────────────────────────────────────────────────────────────

@app.route('/tables')
@login_required
def tables():
    data = load_tables()
    today = str(datetime.date.today())
    return render_template('tables.html', tables=data['tables'], today=today)

@app.route('/tables/book', methods=['POST'])
@login_required
def book_table():
    data = load_tables()
    date = request.form['date']
    time = request.form['time']
    people = int(request.form['people'])
    duration = int(request.form['duration'])

    available = [tid for tid, t in data['tables'].items() if date not in t['bookings'] or time not in t['bookings'][date]]
    
    # Find best combo
    from itertools import combinations
    seats = {tid: data['tables'][tid]['seats'] for tid in available}
    chosen = None
    for size in range(1, len(available) + 1):
        for combo in combinations(available, size):
            if sum(seats[t] for t in combo) >= people:
                chosen = combo
                break
        if chosen:
            break

    if not chosen:
        flash('No tables available for this time slot', 'danger')
        return redirect(url_for('tables'))

    end_dt = datetime.datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M') + datetime.timedelta(hours=duration)
    end_time = end_dt.strftime('%H:%M')
    day = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A')

    for tid in chosen:
        data['tables'][tid]['bookings'].setdefault(date, {})[time] = {
            'duration': duration, 'end_time': end_time, 'day': day,
            'customer': session.get('user', 'Guest')
        }
    save_json(TABLES_FILE, data)
    flash(f'Table(s) {", ".join(chosen)} booked on {day} from {time} for {duration}h', 'success')
    return redirect(url_for('tables'))

@app.route('/tables/release/<table_id>', methods=['POST'])
@login_required
def release_table(table_id):
    data = load_tables()
    data['tables'][table_id]['bookings'] = {}
    save_json(TABLES_FILE, data)
    flash(f'Table {table_id} released', 'success')
    return redirect(url_for('tables'))

@app.route('/tables/cancel', methods=['POST'])
@login_required
def cancel_booking():
    data = load_tables()
    tid = request.form['table_id']
    date = request.form['date']
    time = request.form['time']
    try:
        del data['tables'][tid]['bookings'][date][time]
        if not data['tables'][tid]['bookings'][date]:
            del data['tables'][tid]['bookings'][date]
        save_json(TABLES_FILE, data)
        flash('Booking cancelled', 'success')
    except KeyError:
        flash('Booking not found', 'danger')
    return redirect(url_for('tables'))

if __name__ == '__main__':
    app.run(debug=True)
