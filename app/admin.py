import math

import quest
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import current_user, logout_user
from flask import redirect, request
from app import app, db, Admin, dao
from app.models import RoleEnum, TuyenBay, User, SanBay, SanBayTrungGian,HangGhe,GiaVe, ChuyenBay, HangGheChuyenBay, Ghe, ThongTinVe,HoaDon
from sqlalchemy import event
from sqlalchemy.orm import Session

class MyAdmin(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.count_chuyenbays())

admin = Admin(app=app, name='HỆ THỐNG ĐẶT VÉ MÁY BAY', template_mode='bootstrap4', index_view=MyAdmin())


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.ADMIN

class AuthenticatedEmployee(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == RoleEnum.EMPLOYEE


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class UserView(AuthenticatedAdmin):
    column_display_pk = True
    can_view_details = False
    edit_modal = False
    can_create = False
    can_edit = False
    column_list = ('id', 'name', 'username', 'password', 'role')
class TuyenBayView(AuthenticatedAdmin):
    column_list = ('id','name', 'diemdi','diemden','quangduong', 'sanbaytrunggians', 'ngaybay')
    can_export = True
    column_searchable_list = ['name']
    column_filters = ['giave', 'name']
    column_editable_list = [ 'giave', 'sanbaytrunggians']
    details_modal = True
    edit_modal = True
    can_view_details = True
    form_create_rules = [
        'name',
        'diemdi',
        'diemden',
        'quangduong',
        'sanbaytrunggians',
        'ngaybay'
    ]

    # Tùy chỉnh trường chuyenbay để không hiển thị trong mẫu tạo mới
    form_excluded_columns = ['chuyenbay']

class TimChuyenBayView(AuthenticatedEmployee):
    @expose('/index')
    def index(seft):
        num = dao.count_chuyenbay()
        return seft.render('index.html', data=dao.load_chuyenbay(), pages=math.ceil(num / app.config['PAGE_SIZE']))



class ThongKeView(BaseView):
    @expose("/")
    def index(self):
        thang=request.args.get("thang")
        return self.render('admin/thongke.html', stats=dao.thongketheothang(thang), stats1=dao.tongluotbayvatongtien(thang))
class SanBayTrungGianView(AuthenticatedEmployee):
    column_list = ('tuyenbay_id','tuyenbay','sanbay', 'ghichu','time')
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
class ChuyenBayView(AuthenticatedEmployee):
    column_list = ('id','name','tinhtrang','ngaybay','tuyenbay','maybay',)
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
    column_editable_list = ['tinhtrang']
    form_create_rules = [
        'tuyenbay',
        'name',
        'ngaybay',
        'image',
        'maybay'
    ]
    # Tùy chỉnh trường chuyenbay để không hiển thị trong mẫu tạo mới
    form_excluded_columns = ['thongtinve', 'hangghechuyenbay', 'ghe', 'tinhtrang']
class SanBayView(AuthenticatedAdmin):
    column_list = ('id','name', 'quocgia')
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
class HangGheChuyenBayView(AuthenticatedEmployee):
    column_list = ('chuyenbay_id','chuyenbay','hangghe', 'soluongghe')
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
    # def on_model_change(self, form, model, is_created):
    #     soluongghe = model.soluongghe
    #
    #     # Tạo các ghế tương ứng với soluongghe
    #     for h in range(soluongghe):
    #         new_ghe = Ghe(name= str(model.hangghe_id)+'0'+str(h), hangghe_id=model.hangghe_id, chuyenbay_id=model.chuyenbay_id,
    #                      tinhtrang=True)
    #         db.session.add(new_ghe)

    @event.listens_for(HangGheChuyenBay, 'after_insert')
    def create_ghe_after_insert(mapper, connection, target):
        session = Session(bind=connection)
        hangghe_id = target.hangghe_id
        chuyenbay_id = target.chuyenbay_id
        soluongghe = target.soluongghe
        for h in range(soluongghe):
            new_ghe = Ghe(name= str(hangghe_id)+'0'+str(h), hangghe_id=hangghe_id, chuyenbay_id=chuyenbay_id, tinhtrang=True)
            session.add(new_ghe)
        session.commit()
class GiaVeView(AuthenticatedAdmin):
    column_list = ('hangghe', 'tuyenbay_id','tuyenbay', 'giave','')
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True

class HangGheView(AuthenticatedAdmin):
    column_list = ('id', 'name')
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
class ThongTinVeView(AuthenticatedAdmin):
    column_list = ('id', 'thongtintaikhoan','chuyenbay','chuyenbay.ngaybay','chuyenbay.tuyenbay_id','ghe.hangghe_id','ghe')
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
class HoaDonView(AuthenticatedAdmin):
    column_list = ('id', 'ngaythanhtoan','tongtien')
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    can_create = True
class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(UserView(User, db.session))
admin.add_view(TuyenBayView(TuyenBay, db.session))
admin.add_view(SanBayTrungGianView(SanBayTrungGian, db.session))
admin.add_view(SanBayView(SanBay, db.session))
admin.add_view(GiaVeView(GiaVe, db.session))
# admin.add_view(HangGheView(HangGhe, db.session))
admin.add_view(ChuyenBayView(ChuyenBay, db.session))
admin.add_view(HangGheChuyenBayView(HangGheChuyenBay, db.session))
admin.add_view(ThongTinVeView(ThongTinVe, db.session))
admin.add_view(HoaDonView(HoaDon, db.session))
admin.add_view(ThongKeView(name='Thống kê báo cáo'))
admin.add_view(LogoutView(name="Đăng xuất"))


# admin.add_view(TimChuyenBayView(name='Tim Chuyen Bay'))