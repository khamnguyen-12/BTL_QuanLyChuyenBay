from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from app import dao, app, login_manager, db
from app.models import RoleEnum, TuyenBay, ChuyenBay, GiaVe, ThongTinVe, HangGhe
import math
from app.models import ThongTinTaiKhoan, Ghe

@app.route('/index')
def index():
    kw = request.args.get("kw")
    num = dao.count_chuyenbay()
    products = dao.load_chuyenbay(kw=kw)
    return render_template('index.html', data=products, kw=kw, pages=math.ceil(num / app.config['PAGE_SIZE']))

@app.route('/')
def visual():
    num = dao.count_chuyenbay()
    return render_template('visual.html', data=dao.load_chuyenbay(), pages=math.ceil(num / app.config['PAGE_SIZE']))
@app.route('/book')
def payment():
    return render_template('book.html')

@app.route('/book/<int:flight_id>/<int:ghe_id>')
@login_required
def book(ghe_id, flight_id):
    # return render_template('book.html')
    # load_data = dao.load_data()

    flights = dao.load_chuyenbay()
    ghes = dao.load_ghe()
    ghe = next((f for f in ghes if f.id == ghe_id), None)
    flight = next((f for f in flights if f[1].id == flight_id and f[2].hangghe_id==ghe.hangghe_id), None)
    if flight:
        return render_template('book.html', flight=flight, ghe=ghe)
    else:
        return "Flight not found"
@app.route('/choose_chair/<int:flight_id>/<int:hangghe_id>')
def choose_chair(flight_id, hangghe_id):
    flights = dao.up_ghe()
    matching_flights = [flight for flight in flights if flight[0].id == flight_id and flight[2].id == hangghe_id and flight[1].tinhtrang ==True ]
    print(matching_flights)
    return render_template('choose_chair.html', matching_flights=matching_flights, data=flights)

@app.route('/pay/<int:flight_id>/<int:ghe_id>')
def pay(flight_id,ghe_id):
    dao.add_ve(flight_id,ghe_id)
    chair = Ghe.query.filter(Ghe.id == ghe_id).first()
    print(chair)
    chair.tinhtrang = False
    db.session.commit()
    chair1 = Ghe.query.filter(Ghe.id == ghe_id).first()
    print(chair1.tinhtrang)
    return render_template('pay.html')
@app.route("/login", methods=['get', 'post'])
def process_user_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect('/' if next is None else next)
    return render_template('login.html')

@app.route('/info-ticket')
def load_ticket():
    tk=dao.load_ve()
    ghe=dao.load_ghe()
    cb=dao.load_cb()
    tb=dao.load_tuyenbay()
    return render_template('info-ticket.html', tk=tk, ghe=ghe, cb=cb,tb=tb)


@app.route('/huy-ve',methods=['post'])
def huy_ve():
    data = request.json
    id = data.get('id')
    dao.huy_ve(id)
    return jsonify({'status':'success'})

@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)
    return redirect('/admin')
@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(
                             username=request.form.get('username'),
                             password=password)

            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi!'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('/register.html', err_msg=err_msg)
@app.route('/thongtin', methods=['get', 'post'])
def add_thongtin():
    if request.method == 'POST':
        user_id = current_user.id
        name = request.form['name']
        diachi = request.form['diachi']
        cmnd = request.form['cmnd']
        sdt = request.form['sdt']
        email = request.form['mail']

        # Kiểm tra xem user_id đã có trong bảng thongtintaikhoan hay chưa
        existing_thongtin = ThongTinTaiKhoan.query.filter_by(user_id=user_id).first()

        if existing_thongtin:
            # Nếu tồn tại, thực hiện cập nhật thông tin
            existing_thongtin.name = name
            existing_thongtin.diachi = diachi
            existing_thongtin.cmnd = cmnd
            existing_thongtin.sdt = sdt
            existing_thongtin.email = email
        else:
            user_id = current_user.id
            new_user_info = ThongTinTaiKhoan(name=name, diachi=diachi, cmnd=cmnd, sdt=sdt, email=email, user_id=user_id)
            db.session.add(new_user_info)
        db.session.commit()
        return redirect('/')
    return render_template('thongtin.html')
@app.route('/logout')
def process_user_logout():
    logout_user()
    return redirect("/")
@login_manager.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)
@app.context_processor
def common_response():
    return {
        'chuyenbay': dao.load_chuyenbay(),
        'tuyenbay':dao.load_tuyenbay()
    }
if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
