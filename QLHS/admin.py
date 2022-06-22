from QLHS import app, db
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from QLHS.models import Employee, Teacher, User, UserRole, Lop_hoc, Grade, Subject, Nam_hoc
from flask_login import logout_user, current_user
from flask import redirect, request, url_for
import utils
from datetime import datetime

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class EmployeeView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels ={
        'name': 'Họ và tên',
        'day_of_birth': 'Ngày sinh',
        'gender': 'Giới tính',
        'address': 'Địa chỉ',
        'email': 'email'
    }

class TeacherView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Họ và tên',
        'gender': 'Giới tính',
        'day_of_birth': 'Ngày sinh',
        'address': 'Địa chỉ',
        'email': 'email'
    }

class UserView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['username']
    column_labels = {
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'avatar': 'Ảnh đại diện'
    }

class ClassView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã lớp',
        'name': 'Tên lớp',
        'quantity': 'Số lượng',
        'grade': 'Khối'
    }

class GradeView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã khối',
        'name': 'Tên khối'
    }

class SubjectView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã môn học',
        'name': 'Tên môn học'
    }

class NamHocView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['name']
    column_labels = {
        'id': 'Mã năm học',
        'name': 'Năm học'
    }

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/')

class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        list_class = utils.get_list_class()
        lop = request.args.get('lop')
        stats = None
        diem_TB_lop = None
        lop_hoc = None
        if lop:
            class_id = int(lop.split()[1])
            diem_TB_lop = utils.diem_trung_binh_lop(class_id=class_id)
            stats = utils.thong_ke_theo_nam(class_id=class_id)
            lop_hoc = utils.get_class_by_id(id=class_id)

        return self.render('admin/stats.html',
                           list_class=list_class,
                           stats=stats,
                           diem_TB_lop=diem_TB_lop,
                           lop=lop_hoc)

admin = Admin(app=app,
              name="E-commerce Adminstration",
              template_mode='bootstrap4')

admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(EmployeeView(Employee, db.session, name='Nhân viên'))
admin.add_view(TeacherView(Teacher, db.session, name='Giáo viên'))
admin.add_view(SubjectView(Subject, db.session, name='Môn học'))
admin.add_view(ClassView(Lop_hoc, db.session, name='Lớp học'))
admin.add_view(GradeView(Grade, db.session, name='Khối'))
admin.add_view(NamHocView(Nam_hoc, db.session, name='Năm học'))
admin.add_view(StatsView(name="Thống kê"))
admin.add_view(LogoutView(name='Đăng xuất'))