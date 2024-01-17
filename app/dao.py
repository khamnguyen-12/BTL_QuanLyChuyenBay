import json, os
from app.models import *
import hashlib
from flask_login import current_user
from sqlalchemy import func

# def load_chuyenbay():
#     non_class_ChuyenBay = db.session.query(TuyenBay, ChuyenBay, GiaVe).select_from(ChuyenBay).join(TuyenBay).join(
#     GiaVe).all()
#     return non_class_ChuyenBay

def load_chuyenbay(kw=None):
    products = db.session.query(TuyenBay, ChuyenBay, GiaVe).select_from(ChuyenBay).join(TuyenBay).join(
        GiaVe).all()

    if kw:
        kw_lower = kw.lower()
        products = [p for p in products if kw_lower in p[1].name.lower()]

    return products


def huy_ve(id):
    p = ThongTinVe.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()


def load_tuyenbay():
    return TuyenBay.query.all()
def load_thongtintaikhoan():
    return ThongTinTaiKhoan.query.all()
def load_hangghe():
    return HangGhe.query.all()

def load_cb():
    return ChuyenBay.query.all()

def load_ve():
    return ThongTinVe.query.all()
def load_ghe():
    return Ghe.query.all()
def up_ghe():
    choose_chair = (db.session.query(ChuyenBay, Ghe,HangGhe,HangGheChuyenBay).select_from(ChuyenBay).join(HangGheChuyenBay).
                    join(HangGhe).join(Ghe, (Ghe.chuyenbay_id == ChuyenBay.id) & (Ghe.hangghe_id == HangGhe.id)).all())
    return choose_chair

def add_ve(cb_id,ghe_id):

    infve = ThongTinVe(thongtintaikhoan_id=current_user.id, chuyenbay_id=cb_id, ghe_id=ghe_id)
    db.session.add(infve)
    db.session.commit()

def get_user_by_id(user_id):
    return User.query.get(user_id)
def add_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User( username=username, password=password)
    db.session.add(u)
    db.session.commit()
def add_thongtin(user_id,name,diachi,sdt,mail,cmnd):
    info = ThongTinTaiKhoan(user_id=user_id,name=name, diachi=diachi, sdt=sdt, email=mail, cmnd=cmnd)
    db.session.add(info)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()
def count_chuyenbay():
    return ChuyenBay.query.count()

def count_chuyenbays():
    query = (
        db.session.query(TuyenBay.id, TuyenBay.name, func.count(ChuyenBay.id).label('chuyenbay_count'))
        .outerjoin(ChuyenBay, ChuyenBay.tuyenbay_id == TuyenBay.id)
        .group_by(TuyenBay.id, TuyenBay.name)
    )

    result = query.all()
    return result
def thongketheothang(thang):
    query = db.session.query(TuyenBay.id,TuyenBay.name,func.count(ChuyenBay.id),func.sum(HoaDon.tongtien)) \
                        .join(ThongTinVe, ThongTinVe.id == HoaDon.ve_id)\
                        .join(Ghe, Ghe.id == ThongTinVe.ghe_id)\
                        .join(ChuyenBay, ChuyenBay.id == ThongTinVe.chuyenbay_id) \
                        .filter(ChuyenBay.tuyenbay_id == TuyenBay.id, func.month(ChuyenBay.ngaybay) == thang)\
                        .group_by(TuyenBay.id, TuyenBay.name)
    result = query.all()
    return result
def tongluotbayvatongtien(thang):
    query = (
        db.session.query(
            func.count(ChuyenBay.id),
            func.sum(HoaDon.tongtien))
            .join(ThongTinVe, ThongTinVe.id == HoaDon.ve_id)
            .join(Ghe, Ghe.id == ThongTinVe.ghe_id)
            .join(ChuyenBay, ChuyenBay.id == ThongTinVe.chuyenbay_id)
            .filter(ChuyenBay.tuyenbay_id == TuyenBay.id, func.month(ChuyenBay.ngaybay) == thang)
    )
    result = query.first()
    return result

def load_infor():
    v = ThongTinVe.query.filter_by(thongtintaikhoan_id=current_user.id).first()
    return v
