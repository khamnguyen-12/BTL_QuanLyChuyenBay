from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Boolean, Float
from datetime import datetime
from sqlalchemy.orm import relationship
from app import app, db
from flask_login import UserMixin
import enum
import hashlib
from sqlalchemy.exc import IntegrityError

class RoleEnum(enum.Enum):
    ADMIN = "admin"
    PASSENGER = "passenger"
    EMPLOYEE = "employee"
class HinhThucThanhToan(enum.Enum):
    CHUYENKHOAN= "Chuyển khoản"
    TIENMAT = "Tiền mặt"
class BaseModel(db.Model):
    __abstract__=True
    id = Column(Integer, primary_key=True, autoincrement=True)
class MayBay(BaseModel):
    __tablename__= 'maybay'
    name = Column(String(50), nullable=False)
    chuyenbay = relationship('ChuyenBay', backref='maybay', lazy=True)
    def __str__(self):
        return self.name


class TuyenBay(db.Model):
    __tablename__ = 'tuyenbay'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    diemdi_id = Column(Integer, ForeignKey('sanbay.id'), nullable=False)
    diemden_id = Column(Integer, ForeignKey('sanbay.id'), nullable=False)
    quangduong = Column(String(50), nullable=False)
    diemdi = relationship('SanBay', foreign_keys=[diemdi_id], back_populates='tuyenbays_di', lazy=True)
    diemden = relationship('SanBay', foreign_keys=[diemden_id], back_populates='tuyenbays_den', lazy=True)
    sanbaytrunggians = relationship('SanBayTrungGian', backref='tuyenbay')
    giave = relationship('GiaVe', backref='tuyenbay', lazy=True)

    def __str__(self):
        return self.name


class SanBay(db.Model):
    __tablename__ = 'sanbay'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    quocgia = Column(String(50), nullable=False)
    sanbaytrunggians = relationship('SanBayTrungGian', backref='sanbay', lazy=True)
    tuyenbays_di = relationship('TuyenBay', foreign_keys=[TuyenBay.diemdi_id], back_populates='diemdi', lazy=True)
    tuyenbays_den = relationship('TuyenBay', foreign_keys=[TuyenBay.diemden_id], back_populates='diemden', lazy=True)

    def __str__(self):
        return self.name
class SanBayTrungGian(db.Model):
    __tablename__ = 'sanbaytrunggian'
    tuyenbay_id = Column(Integer, ForeignKey('tuyenbay.id'), primary_key=True, nullable=False)
    sanbay_id = Column(Integer, ForeignKey('sanbay.id'), primary_key=True, nullable=False)
    ghichu = Column(String(50), nullable=False)
    time = Column(String(20), default='5h')

    def __str__(self):
        return f"{self.sanbay.name} "

class ChuyenBay(BaseModel):
    __tablename__= 'chuyenbay'
    name = Column(String(50), nullable=False)
    image = Column(String(200))
    tinhtrang = Column(Boolean, default=True)
    ngaybay = Column(DateTime, default=datetime.now())
    tuyenbay_id= Column(Integer, ForeignKey('tuyenbay.id'),nullable=False)
    maybay_id = Column(Integer, ForeignKey('maybay.id'), nullable=False)
    tuyenbay = relationship('TuyenBay', backref='chuyenbay', lazy=False)
    hangghechuyenbay = relationship('HangGheChuyenBay', backref='chuyenbay', lazy=False)
    ghe = relationship('Ghe', backref='chuyenbay', lazy=False)
    def __str__(self):
        return self.name

class GiaVe(db.Model):
    __tablename__ = 'giave'
    hangghe_id = Column(Integer, ForeignKey('hangghe.id'), primary_key=True)
    tuyenbay_id = Column(Integer, ForeignKey('tuyenbay.id'), primary_key=True)
    giave = Column(Float,default=0)
class HangGhe(BaseModel):
    __tablename__ = 'hangghe'
    name = Column(String(50), nullable=False)
    hangghechuyenbay = relationship('HangGheChuyenBay', backref='hangghe')
    giave = relationship('GiaVe', backref='hangghe')
    ghe = relationship('Ghe', backref='hangghe')
    def __str__(self):
        return self.name
class HangGheChuyenBay(db.Model):
    __tablename__ = 'hangghechuyenbay'
    hangghe_id = Column(Integer, ForeignKey('hangghe.id'), primary_key=True, nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey('chuyenbay.id'), primary_key=True, nullable=False)
    soluongghe = Column(Integer, nullable=False)
    def __str__(self):
        return self.hangghe_id.name
class Ghe(BaseModel):
    __tablename__ = 'ghe'
    name = Column(String(50), nullable=False)
    hangghe_id = Column(Integer, ForeignKey('hangghe.id'), nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey('chuyenbay.id'), nullable=False)
    thongtinve = relationship('ThongTinVe', backref='ghe', lazy=True)
    tinhtrang = Column(Boolean, nullable=False)
    def __str__(self):
        return self.name
class ThongTinVe(BaseModel):
    __tablename__= 'thongtinve'
    thongtintaikhoan_id = Column(Integer, ForeignKey('thongtintaikhoan.user_id'), nullable=False)
    chuyenbay_id = Column(Integer, ForeignKey('chuyenbay.id'), nullable=False)
    ghe_id = Column(Integer, ForeignKey('ghe.id'), nullable=False)
    hoadon_id = relationship('HoaDon', backref='thongtinve')
    chuyenbay = relationship('ChuyenBay', backref='thongtinve')

class ThongTinTaiKhoan(db.Model):
    __tablename__ = 'thongtintaikhoan'
    user_id = Column(Integer, ForeignKey('user.id'),primary_key=True )
    name = Column(String(50),nullable=False)
    diachi = Column(String(50),nullable=False)
    cmnd = Column(String(50),nullable=False)
    sdt = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    user = relationship('User', uselist=False, back_populates='thongtintaikhoan')
    thongtinve = relationship('ThongTinVe', backref='thongtintaikhoan')
    def __str__(self):

        return self.name
class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    username = Column(String(50),nullable=False)
    password = Column(String(50),nullable=False)
    image = Column(String(100),nullable=True)
    thongtintaikhoan = relationship('ThongTinTaiKhoan', back_populates='user')
    role = Column(Enum(RoleEnum), default=RoleEnum.PASSENGER)
    def __str__(self):
        return self.username

class HoaDon(BaseModel):
    __tablename__ = 'HoaDon'
    tongtien = Column(Float, default=0)
    hinhthucthanhtoan= Column(Enum(HinhThucThanhToan),nullable=False )
    ngaythanhtoan= Column(DateTime, default=datetime.now())
    ve_id = Column(Integer,ForeignKey('thongtinve.id'), nullable= False)
def addghe(hangghechuyenbay):
    try:
        hangghe_id= hangghechuyenbay.hangghe_id
        chuyenbay_id= hangghechuyenbay.chuyenbay_id
        soluongghe= hangghechuyenbay.soluongghe

        for h in range(soluongghe):
            ghe = Ghe(name= str(hangghe_id)+'0'+str(h), hangghe_id=hangghe_id,chuyenbay_id=chuyenbay_id, tinhtrang=True)
            db.session.add(ghe)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        taikhoan4 = User(username='Kham', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.ADMIN)
        taikhoan5 = User(username='Tien', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.EMPLOYEE)
        taikhoan6 = User(username='Tam', password=str(hashlib.md5("123".encode('utf-8')).hexdigest()),
                             role=RoleEnum.PASSENGER)

        db.session.add_all([taikhoan4,taikhoan5,taikhoan6])
        thongtintaikhoan1 = ThongTinTaiKhoan(name='Nguyễn Việt Khâm', diachi='Nhà Bè', cmnd='123', sdt='0123456789',
                                             email='Kham@123.com',user_id=1)
        thongtintaikhoan2 = ThongTinTaiKhoan(name='Trần Đặng Mỹ Tiên', diachi='Quận 7', cmnd='456', sdt='0123456789',
                                             email='Tiên@123.com', user_id=2)
        thongtintaikhoan3 = ThongTinTaiKhoan(name='Khương Thanh Tâm', diachi='Gò Vấp', cmnd='789', sdt='0123456789',
                                             email='chien@123.com', user_id=3)

        db.session.add_all([thongtintaikhoan1, thongtintaikhoan2, thongtintaikhoan3])
        sb1 = SanBay(name='Sân bay Phù Cát', quocgia='Việt Nam')
        sb2 = SanBay(name='Sân bay Nội Bài', quocgia='Việt Nam')
        sb3 = SanBay(name='Sân bay Pháp', quocgia='Pháp')
        sb4 = SanBay(name='Sân bay Hongkong', quocgia='Trung Quốc')
        sb5 = SanBay(name='Sân bay Tokyo', quocgia='Nhật Bản')
        sb6 = SanBay(name='Sân bay Suvarnabhumi ', quocgia='Thái Lan')
        sb7 = SanBay(name='Sân bay Los Angeles', quocgia='Mỹ')
        sb8 = SanBay(name='Sân bay BangKok', quocgia='Thái Lan')
        sb9 = SanBay(name='Sân bay Đà Nẵng', quocgia='Việt Nam')
        sb10 = SanBay(name='Sân bay Phú Quốc', quocgia='Kiên Giang')
        db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6,sb7,sb8,sb9,sb10])
        sbtg1 = SanBayTrungGian(ghichu='Thời gian dừng:  2 giờ', tuyenbay_id=1, sanbay_id=9)
        sbtg2 = SanBayTrungGian(ghichu='Thời gian dừng: 1h30p', tuyenbay_id=2, sanbay_id=9, time = '4h')
        sbtg3 = SanBayTrungGian(ghichu='Thời gian dừng: 1-3 giờ', tuyenbay_id=3, sanbay_id=6, time ='3h' )
        sbtg4 = SanBayTrungGian(ghichu='Thời gian dừng: 2 giờ', tuyenbay_id=1, sanbay_id=8, time = '3h30')
        sbtg5 = SanBayTrungGian(ghichu='Thời gian dừng: 2 giờ', tuyenbay_id=3, sanbay_id=4)
        db.session.add_all([sbtg1, sbtg2, sbtg3, sbtg4, sbtg5])
        mb1 = MayBay(name='Máy bay Boeing 777')
        mb2 = MayBay(name='Máy bay Boeing 787')
        mb3 = MayBay(name='Máy bay A350')
        mb4 = MayBay(name='Máy bay Airbus A320')
        mb5 = MayBay(name='Máy bay Boeing 787 Dreamliner:')
        mb6 = MayBay(name='Máy bay Boeing 787')
        db.session.add_all([mb1, mb2, mb3, mb4, mb5, mb6])

        tb1 = TuyenBay(name=sb1.name + ' - ' + sb6.name, diemdi_id=1, diemden_id=6, quangduong=100000)
        tb2 = TuyenBay(name=sb2.name + ' - ' + sb7.name, diemdi_id=2, diemden_id=7, quangduong=90000)
        tb3 = TuyenBay(name=sb3.name + ' - ' + sb8.name, diemdi_id=3, diemden_id=8, quangduong=300000)
        tb4 = TuyenBay(name=sb4.name + ' - ' + sb10.name, diemdi_id=4, diemden_id=9, quangduong=50000)
        tb5 = TuyenBay(name=sb5.name + ' - ' + sb4.name, diemdi_id=5, diemden_id=10, quangduong=50000)
        # tb6 = TuyenBay(name=sb3.name + ' - ' + sb10.name, diemdi_id=1, diemden_id=10, quangduong=50000)
        # tb7 = TuyenBay(name=sb3.name + ' - ' + sb10.name, diemdi_id=1, diemden_id=10, quangduong=50000)
        db.session.add_all([tb1, tb2, tb3, tb4, tb5])


        hangghe1 = HangGhe(name='Hạng 1')
        hangghe2 = HangGhe(name='Hạng 2')
        db.session.add_all([hangghe1, hangghe2])

        gv1 = GiaVe(giave=2000000, hangghe_id=1, tuyenbay_id=1)
        gv2 = GiaVe(giave=3000000, hangghe_id=2, tuyenbay_id=1)
        gv3 = GiaVe(giave=500000, hangghe_id=1, tuyenbay_id=2)
        gv4 = GiaVe(giave=700000, hangghe_id=2, tuyenbay_id=2)
        gv5 = GiaVe(giave=1000000, hangghe_id=1, tuyenbay_id=3)
        gv6 = GiaVe(giave=1200000, hangghe_id=2, tuyenbay_id=3)
        gv7 = GiaVe(giave=4000000, hangghe_id=1, tuyenbay_id=4)
        gv8 = GiaVe(giave=5000000, hangghe_id=2, tuyenbay_id=4)
        db.session.add_all([gv1, gv2, gv3, gv4, gv5,gv6,gv7,gv8])

        ngay=datetime(2024,2,12,12,40,00)
        ngay1 = datetime(2024, 2, 2, 10, 00, 00)
        ngay2 = datetime(2024, 1, 22, 10, 00, 00)
        ngay3 = datetime(2024, 1, 17, 10, 00, 00)
        ngay4 = datetime(2024, 1, 22, 10, 00, 00)

        cb1 = ChuyenBay(tuyenbay_id=1, maybay_id=1, ngaybay=ngay1, tinhtrang=True,
                        image="https://cdn.justfly.vn/1000x750/media/202304/19/1681869605-san-bay-suvarnabhumi.jpg", name='Chuyến bay Phù Cát - Suvarnabhumi')
        cb2 = ChuyenBay(tuyenbay_id=2, maybay_id=2,ngaybay=ngay2, tinhtrang=True,
                        image="https://owa.bestprice.vn/images/destinations/uploads/san-bay-quoc-te-chengdu-tianfu-6178bc6ca4410.png", name='Chuyến bay Nội Bài - Los Angeles')
        cb3 = ChuyenBay(tuyenbay_id=3, maybay_id=3, ngaybay=ngay1, tinhtrang=True,
                        image="https://owa.bestprice.vn/images/destinations/uploads/san-bay-quoc-te-chengdu-tianfu-6178bc6ca4410.png", name='Chuyến bay Pháp - BangKok')
        cb4 = ChuyenBay(tuyenbay_id=4, maybay_id=4, ngaybay=ngay1, tinhtrang=True,
                        image="https://cdn.justfly.vn/1000x750/media/202304/19/1681869605-san-bay-suvarnabhumi.jpg", name='Chuyến bay Hongkong - Sân bay Phú Quốc')
        cb5 = ChuyenBay(tuyenbay_id=1, maybay_id=5, ngaybay=ngay2, tinhtrang=True,
                        image="https://eva-air.com.vn/wp-content/uploads/2023/09/San-bay-quoc-te-Los-Angeles.webp", name='Chuyến bay Phù Cát - Suvarnabhumi')
        cb6 = ChuyenBay(tuyenbay_id=2, maybay_id=6, ngaybay=ngay2, tinhtrang=True,
                        image="https://eva-air.com.vn/wp-content/uploads/2023/09/San-bay-quoc-te-Los-Angeles.webp", name='Chuyến bay Nội Bài - Los Angeles')
        cb7 = ChuyenBay(tuyenbay_id=3, maybay_id=1, ngaybay=ngay2, tinhtrang=True,
                        image="https://www.dulichhoanmy.com/wp-content/uploads/2022/10/ben-trong-san-bay-lax.jpg", name='Chuyến bay Pháp - BangKok')
        cb8 = ChuyenBay(tuyenbay_id=5, maybay_id=4, ngaybay=ngay2, tinhtrang=True,
                        image="https://owa.bestprice.vn/images/destinations/uploads/san-bay-quoc-te-chengdu-tianfu-6178bc6ca4410.png", name='Chuyến bay Tokyo - Hongkong')
        db.session.add_all([cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8])


        h1= HangGheChuyenBay(hangghe_id=1, chuyenbay_id=1, soluongghe=5)
        h2= HangGheChuyenBay(hangghe_id=2, chuyenbay_id=1, soluongghe=5)
        h3= HangGheChuyenBay(hangghe_id=1, chuyenbay_id=2, soluongghe=6)
        h4= HangGheChuyenBay(hangghe_id=2, chuyenbay_id=2, soluongghe=6)
        h5 = HangGheChuyenBay(hangghe_id=1, chuyenbay_id=3, soluongghe=4)
        h6 = HangGheChuyenBay(hangghe_id=2, chuyenbay_id=3, soluongghe=4)
        h7 = HangGheChuyenBay(hangghe_id=1, chuyenbay_id=4, soluongghe=5)
        h8 = HangGheChuyenBay(hangghe_id=2, chuyenbay_id=4, soluongghe=5)
        h9 = HangGheChuyenBay(hangghe_id=1, chuyenbay_id=5, soluongghe=7)
        h10 = HangGheChuyenBay(hangghe_id=2, chuyenbay_id=5, soluongghe=7)
        h11 = HangGheChuyenBay(hangghe_id=1, chuyenbay_id=6, soluongghe=6)
        h12 = HangGheChuyenBay(hangghe_id=2, chuyenbay_id=6, soluongghe=6)
        h13 = HangGheChuyenBay(hangghe_id=1, chuyenbay_id=7, soluongghe=7)
        h14 = HangGheChuyenBay(hangghe_id=2, chuyenbay_id=7, soluongghe=7)
        h15 = HangGheChuyenBay(hangghe_id=1, chuyenbay_id=8, soluongghe=5)
        h16 = HangGheChuyenBay(hangghe_id=2, chuyenbay_id=8, soluongghe=5)
        db.session.add_all([h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12, h13, h14, h15, h16])
        addghe(h1)
        addghe(h2)
        addghe(h3)
        addghe(h4)
        addghe(h5)
        addghe(h6)
        addghe(h7)
        addghe(h8)
        addghe(h9)
        addghe(h10)
        addghe(h11)
        addghe(h12)
        addghe(h13)
        addghe(h14)
        addghe(h15)
        addghe(h16)
        tt1 = ThongTinVe(thongtintaikhoan_id=1, chuyenbay_id=1, ghe_id=1)
        tt2 = ThongTinVe(thongtintaikhoan_id=1, chuyenbay_id=1, ghe_id=2)
        tt3 = ThongTinVe(thongtintaikhoan_id=2, chuyenbay_id=2, ghe_id=11)
        tt4 = ThongTinVe(thongtintaikhoan_id=3, chuyenbay_id=3, ghe_id=23)
        tt5 = ThongTinVe(thongtintaikhoan_id=1, chuyenbay_id=7, ghe_id=78)
        tt6 = ThongTinVe(thongtintaikhoan_id=2, chuyenbay_id=8, ghe_id=85)
        db.session.add_all([tt1,tt2,tt3,tt4,tt5,tt6])
        hd1 = HoaDon(ve_id=1, hinhthucthanhtoan=HinhThucThanhToan.CHUYENKHOAN, tongtien=2000000)
        hd2 = HoaDon(ve_id=2, hinhthucthanhtoan=HinhThucThanhToan.CHUYENKHOAN, tongtien=2000000)
        hd3 = HoaDon(ve_id=3, hinhthucthanhtoan=HinhThucThanhToan.CHUYENKHOAN, tongtien=500000)
        hd4 = HoaDon(ve_id=4, hinhthucthanhtoan=HinhThucThanhToan.CHUYENKHOAN, tongtien=1000000)
        hd5 = HoaDon(ve_id=5, hinhthucthanhtoan=HinhThucThanhToan.TIENMAT, tongtien=1200000)
        hd6 = HoaDon(ve_id=6, hinhthucthanhtoan=HinhThucThanhToan.CHUYENKHOAN, tongtien=4000000)
        db.session.add_all([hd1, hd2, hd3, hd4, hd5, hd6])
        db.session.commit()
       