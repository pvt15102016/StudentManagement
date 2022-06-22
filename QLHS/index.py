import math
from flask import render_template, request, redirect, url_for, session, jsonify
from QLHS import app, login, utils
from QLHS.models import Gender
from QLHS.admin import *
from flask_login import login_user, logout_user, login_required
import hashlib
import cloudinary.uploader


@app.route('/')
def index():
    logout_user()
    return render_template('login.html')


@app.route('/admin')
def admin():
    return redirect('/admin')


@app.route('/teacher/<int:user_id>')
def teacher(user_id):
    user = utils.get_user_by_id(user_id=user_id)
    teacher = utils.get_teacher_by_user_id(user_id=user_id)
    return render_template('teacher.html', user=user, subjects=utils.get_list_subject(), teacher=teacher)


@app.route('/employee/<int:user_id>')
def employee(user_id):
    user = utils.get_user_by_id(user_id=user_id)
    return render_template('employee.html', user=user)


@app.route('/user-login', methods=['get', 'post'])
def user_login():
    msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user and user.user_role == UserRole.TEACHER:
            login_user(user=user)
            tc = utils.get_teacher_by_user_id(user_id=user.id)
            return render_template('teacher.html', user=user, teacher=tc, subjects=utils.get_list_subject())
        elif user and user.user_role == UserRole.EMPLOYEE:
            login_user(user=user)
            return render_template('employee.html', user=user)
        else:
            msg = 'Tên đăng nhập hoặc mật khẩu chưa chính xác!!!'

    return render_template('login.html', msg=msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_login'))


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/change-password/<int:user_id>', methods=['post', 'get'])
def change_password(user_id):
    msg = ''
    user = utils.get_user_by_id(user_id)
    if request.method.__eq__('POST'):
        pw = str(request.form.get('pw'))
        password = str(hashlib.md5(pw.strip().encode('utf-8')).hexdigest())
        new_pw = request.form.get('new_pw')
        confirm_pw = request.form.get('confirm_pw')
        if user.password.__eq__(password):
            if new_pw.__eq__(confirm_pw):
                utils.change_password(user_id=user.id, new_pw=new_pw)
                msg = 'Đổi mật khẩu thành công!!!'
            else:
                msg = 'Mật khẩu nhập lại chưa chính xác'
        else:
            msg = 'Mật khẩu không chính xác :))!!!'

    return render_template('change_password.html', msg=msg, user=user)


@app.route('/admin-login', methods=['post', 'get'])
def admin_login():
    msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_login(username=username, password=password)
        if user and user.user_role == UserRole.ADMIN:
            login_user(user=user)
            return redirect('/admin')
        else:
            msg = 'Tên đăng nhập hoặc mật khẩu chưa chính xác!!!'
    return render_template('admin_login.html', msg=msg)


@app.route('/employee/<int:user_id>/add-student', methods=['post', 'get'])
def add_student(user_id):
    msg = ''
    user = utils.get_user_by_id(user_id=user_id)
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        sex = request.form.get('gender')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        day_of_birth = request.form.get('day_of_birth')
        gender = None

        if sex.__eq__('male'):
            gender = Gender.MALE
        else:
            gender = Gender.FEMALE

        try:
            if utils.check_age(day_of_birth=day_of_birth):
                utils.add_student(name=name,
                                  gender=gender,
                                  day_of_birth=day_of_birth,
                                  email=email,
                                  phone_number=phone_number,
                                  address=address)
                msg = 'Tiếp nhận học sinh thành công'
            else:
                msg = 'Độ tuổi không hợp lệ!!!'
        except:
            msg = 'Hệ thống có lỗi!!!'

    return render_template('add_student.html', msg=msg, user=user)

@app.route('/lap-danh-sach-lop', methods=['get', 'post'])
def lap_danh_sach():
    list_grade = utils.get_list_grade()
    list_class = utils.get_list_class()
    return render_template('lap_ds_lop.html', list_grade=list_grade, list_class=list_class)

@app.route('/api/update', methods=['put'])
def update():
    data = request.json
    name = data.get('name')
    list_class = utils.get_list_class_by_grade_name(name=name)
    size = list_class.__len__()
    return {
        'list': list_class,
        'size': size
    }

@app.route('/api/load-students', methods=['post'])
def load_students():
    list = utils.load_students()

    return {
        'list': list,
        'size': list.__len__()
    }

@app.route('/api/add-student-to-class', methods=['post'])
def add_student_to_class():
    data = request.json
    student_id = data.get('student_id')
    class_id = data.get('class_id')
    msg = ''
    list_student_in_class = utils.get_list_student_by_class_id(class_id=class_id)
    if class_id:
        if list_student_in_class.__len__() <= 40:
            if utils.check_student(id=student_id, class_id=class_id) is False:
                try:
                    utils.add_student_to_class(id=student_id, class_id=class_id)
                    msg = 'Lưu thành công!!!'
                except:
                    msg = 'Hệ thống có lỗi!!!'
            else:
                msg = 'Học sinh này đã tồn tại trong danh sách lớp ' + utils.get_class_by_id(class_id).name
        else:
            msg = 'Danh sách của lớp đã đủ sỉ số!!!'
    else:
        msg = 'Hãy chọn lớp!!!'

    return {
        'msg': msg
    }

@app.route('/teacher/<int:user_id>/list-student', methods=['post', 'get'])
def load_list_student(user_id):
    teacher = utils.get_teacher_by_user_id(user_id=user_id)
    list_students = utils.get_list_student_by_teacher_id(teacher.id)
    lop = utils.get_class_by_id(teacher.class_id)

    return render_template('xem_ds_hs.html', list_students=list_students, lop=lop, number=list_students.__len__(), Gender=Gender, teacher=teacher)

@app.route('/teacher/<int:user_id>/xem-diem/<int:subject_id>/hoc-ky/<int:id_hocKy>', methods=['post', 'get'])
def load_mark(subject_id, user_id, id_hocKy):
    teacher = utils.get_teacher_by_user_id(user_id=user_id)
    lop = utils.get_class_by_id_teacher(teacher_id=teacher.id)
    subject = utils.get_subject_by_id(subject_id)
    msg = ''
    list_hocKy = utils.get_HocKy()
    list = None
    try:
        list = utils.get_list_mark_by_subject_id_in_class(subject_id=subject_id, class_id=lop.id, id_hoc_ky=id_hocKy)
    except:
        msg = 'Hệ thống có lỗi'
    size = 0
    if list:
        size = list.__len__()
    hocKy = utils.get_hoc_ky_by_id(id=id_hocKy)
    return render_template('xem_diem.html',
                           msg=msg,
                           list=list,
                           size=size,
                           lop=lop,
                           subject=subject,
                           list_hocKy=list_hocKy,
                           hocKy=hocKy,
                           nam=utils.get_Nam(hocKy.nam_id))

# @app.route('/api/load-mark', methods=['post'])
# def load_mark_api():
#     data = request.json
#     subject_id = data.get('subject_id')
#     class_id = data.get('class_id')
#     id_hocKy = data.get('id_hocKy')
#     msg = ''
#     try:
#         list = utils.get_list_mark_by_subject_id_in_class(subject_id=subject_id, class_id=class_id, id_hoc_ky=id_hocKy)
#     except:
#         msg = 'Hệ thống có lỗi'
#
#     return {
#         'msg': msg,
#         'list': list,
#         'size': list.__len__(),
#         'hocKy': id_hocKy,
#         'subject_id': subject_id,
#     }

@app.route('/nhap-diem/id_subject/<int:subject_id>/id_student/<int:student_id>/id_hocKy/<int:id_hocKy>', methods=['post', 'get'])
def nhap_diem(subject_id, student_id, id_hocKy):
    student = utils.get_student_by_id(id=student_id)
    lop = utils.get_class_by_id(id=student.class_id)
    subject = utils.get_subject_by_id(id=subject_id)

    return render_template('nhap_diem.html',
                           subject=subject,
                           id_hocKy=id_hocKy,
                           student=student)

@app.route('/save//<int:student_id><int:subject_id>/<int:id_hocKy>', methods=['post', 'get'])
def save(subject_id, student_id, id_hocKy):
    msg = ''
    if request.method.__eq__('POST'):
        diem15Phut = request.form.get('diem15Phut')
        diem1Tiet = request.form.get('diem1Tiet')
        diemThi = request.form.get('diemThi')
        if (diem15Phut and (float(diem15Phut) < 0 or float(diem15Phut) > 10)) or \
                (diem1Tiet and (float(diem1Tiet) < 0 or float(diem1Tiet) > 10)) or \
                (diemThi and (float(diemThi) < 0 or float(diemThi) > 10)):
            msg = 'Điểm không hợp lệ!!!'
        else:
            try:
                utils.update_mark(subject_id=subject_id,
                                  student_id=student_id,
                                  diem15Phut=diem15Phut,
                                  diem1Tiet=diem1Tiet,
                                  diemThi=diemThi,
                                  id_hocKy=id_hocKy)
                msg = 'Lưu thành công!!!'
            except:
                msg = 'Hệ thống có lỗi!!!'

    return render_template('nhap_diem.html',
                           msg=msg,
                           subject=utils.get_subject_by_id(id=subject_id),
                           student=utils.get_student_by_id(id=student_id),
                           id_hocKy=id_hocKy)


@app.route('/xem-diem-trung-binh/<int:class_id>', methods=['get', 'post'])
def load_diem_trung_binh(class_id):
    lop = utils.get_class_by_id(id=class_id)
    list_diem_lop = utils.diem_trung_binh_lop(class_id=class_id)

    return render_template('xem_diem_trung_binh.html', list=list_diem_lop, lop=lop, size=list_diem_lop.__len__())


if (__name__ == '__main__'):
    from QLHS.admin import *
    app.run(debug=True)
