import json
import os
from re import sub

from QLHS import app, db
from QLHS.models import Teacher, Employee, User, UserRole, Student, Lop_hoc, Grade, Hoc, Subject, Hoc_ky, Nam_hoc
from QLHS import app
import hashlib
from datetime import date, datetime


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user_by_username(username):
    return User.query.filter(User.username.__eq__(username)).first()


def check_username(username):
    users = User.query.all()
    for user in users:
        if user.username.__eq__(username):
            return True
    return False


def change_password(user_id, new_pw):
    user = get_user_by_id(user_id)
    user.password = str(hashlib.md5(new_pw.strip().encode('utf-8')).hexdigest())

    db.session.add(user)
    db.session.commit()


def get_person(user_id):
    user = get_user_by_id(user_id)
    if user.user_role.__eq__(UserRole.EMPLOYEE):
        return Employee.query.get(user_id)
    return Teacher.query.get(user_id)


def get_list_employees():
    return Employee.query.filter(Employee.id_user.__eq__(User.id)).all()


def check_age(day_of_birth):
    if day_of_birth:
        year = datetime.strptime(day_of_birth, "%Y-%m-%d").year
        today = date.today()
        age = today.year - year
        if age.__ge__(15) and age.__le__(20):
            return True


def add_student(name, gender, day_of_birth, email, phone_number, address, class_id=None):
    student = Student(name=name, email=email, gender=gender, address=address, day_of_birth=day_of_birth,
                      phone_number=phone_number, class_id=class_id)

    db.session.add(student)
    db.session.commit()


def get_list_class():
    return Lop_hoc.query.all()


def get_class_by_id_teacher(teacher_id):
    teacher = get_teacher_by_id(teacher_id)
    return get_class_by_id(id=teacher_id)


def get_list_grade():
    return Grade.query.all()


def get_list_class_by_grade_name(name):
    list = Lop_hoc.query.join(Grade, Lop_hoc.grade_id == Grade.id) \
        .filter(Grade.name.__eq__(name)) \
        .add_columns(Lop_hoc.name, Lop_hoc.id) \
        .all()
    dict = {}

    i = 1
    for c in list:
        dict[i] = {
            'name': c.name,
            'id': c.id
        }
        i = i + 1
    return dict


def load_students():
    list = Student.query.all()

    dict = {}

    i = 1
    for s in list:
        dict[i] = {
            'id': s.id,
            'name': s.name,
            'day_of_birth': s.day_of_birth.strftime('%d/%m/%Y')
        }
        i = i + 1

    return dict


def check_student(id, class_id):
    list_student_in_class = Student.query.join(Lop_hoc, Student.class_id == Lop_hoc.id) \
        .filter(Lop_hoc.id == class_id) \
        .add_columns(Student.id) \
        .all()

    for s in list_student_in_class:
        if s.id == id:
            return True
    return False


def delete_student(student_id):
    student = get_student_by_id(id=student_id)
    hoc = Hoc.query.filter(Hoc.student_id == student_id).all()
    for h in hoc:
        db.session.delete(h)
    db.session.commit()
    db.session.delete(student)
    db.session.commit()


def get_class_by_id(id):
    return Lop_hoc.query.get(id)


def get_subject_by_id(id):
    return Subject.query.get(id)


def get_list_subject():
    return Subject.query.all()


def add_student_to_class(id, class_id):
    student = Student.query.get(id)

    student.class_id = class_id

    db.session.add(student)
    db.session.commit()


def get_teacher_by_id(id):
    return Teacher.query.get(id)


def get_student_by_id(id):
    return Student.query.get(id)


def get_hoc_ky_by_id(id):
    return Hoc_ky.query.get(id)


def get_teacher_by_user_id(user_id):
    return Teacher.query.filter(Teacher.id_user == user_id).first()


def get_list_student_by_class_id(class_id):
    return Student.query.filter(Student.class_id == class_id).all()


def edit_info_student(student_id, name=None, day_of_birth=None, gender=None, phone_number=None, address=None,
                      email=None):
    student = get_student_by_id(id=student_id)
    if name:
        student.name = name
    if day_of_birth:
        student.day_of_birth = day_of_birth
    if gender:
        student.gender = gender
    if phone_number:
        student.phone_number = phone_number
    if email:
        student.email = email
    if address:
        student.address = address

    db.session.add(student)
    db.session.commit()


def get_Nam(id):
    return Nam_hoc.query.get(id)


def get_HocKy():
    return Hoc_ky.query.all()


def get_grade_by_class_id(class_id):
    lop = get_class_by_id(id=class_id)
    return Grade.query.get(lop.grade_id)


def get_list_student_by_teacher_id(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return Student.query.filter(Student.class_id == teacher.class_id).all()


def get_mark_subject_of_student(student_id, subject_id, id_hocKy):
    return Hoc.query.filter(Hoc.student_id == student_id, Hoc.subject_id == subject_id,
                            Hoc.id_hocKy == id_hocKy).first()


def get_list_mark_by_subject_id_in_class(subject_id, class_id, id_hoc_ky):  # 1 môn
    list_student = Student.query.filter(Student.class_id == class_id).all()

    dict = []
    i = 1
    for st in list_student:
        hoc = get_mark_subject_of_student(student_id=st.id, subject_id=subject_id, id_hocKy=id_hoc_ky)
        if hoc is None:
            hoc = Hoc(student_id=st.id, subject_id=subject_id, diem15Phut=0, diem1Tiet=0, diemThi=0, id_hocKy=id_hoc_ky)
            db.session.add(hoc)
        dict.append({
            'student_id': st.id,
            'stt': i,
            'name': st.name,
            'diem15Phut': hoc.diem15Phut,
            'diem1Tiet': hoc.diem1Tiet,
            'diemThi': hoc.diemThi
        })
        i = i + 1
    db.session.commit()

    return dict

    # list = Hoc.query.filter(Hoc.subject_id == subject_id).all()
    # list_student = get_list_student_by_class_id(class_id=class_id)
    # dict = []
    # i = 1
    # for h in list:
    #     for st in list_student:
    #         if h.student_id == st.id:
    #             dict.append({
    #                 'stt': i,
    #                 'name': st.name,
    #                 'diem15Phut': h.diem15Phut,
    #                 'diem1Tiet': h.diem1Tiet,
    #                 'diemThi': h.diemThi
    #             })
    #             i = i + 1
    #
    # return dict


def update_mark(student_id, subject_id, id_hocKy, diem15Phut, diem1Tiet, diemThi):
    hoc = get_mark_subject_of_student(student_id=student_id, subject_id=subject_id, id_hocKy=id_hocKy)
    if diem15Phut:
        hoc.diem15Phut = diem15Phut
    if diem1Tiet:
        hoc.diem1Tiet = diem1Tiet
    if diemThi:
        hoc.diemThi = diemThi

    db.session.add(hoc)
    db.session.commit()


def diem_trung_binh_mon_hoc_sinh_1HK(student_id, subject_id, id_hocKy):  # 1 môn
    diem = get_mark_subject_of_student(student_id=student_id, subject_id=subject_id, id_hocKy=id_hocKy)
    if diem is None:
        diem = Hoc(student_id=student_id, subject_id=subject_id, diem15Phut=0, diem1Tiet=0, diemThi=0)
    return (diem.diem15Phut + diem.diem1Tiet * 2 + diem.diemThi * 3) / 6


# def diem_trung_binh_mon_ca_nam(student_id, subject_id):
#     diemTB = 0
#     diemTB_hk1 = diem_trung_binh_mon_hoc_sinh_1HK(student_id=student_id, subject_id=subject_id, id_hocKy=1)
#     diemTB_hk2 = diem_trung_binh_mon_hoc_sinh_1HK(student_id=student_id, subject_id=subject_id, id_hocKy=2)
#
#     return (diemTB_hk1 + diemTB_hk2*2) / 3

def diem_TB_HK(student_id, id_hocKy):  # tất cả các môn
    subjects = get_list_subject()

    count = 0
    for s in subjects:
        count += diem_trung_binh_mon_hoc_sinh_1HK(student_id=student_id, subject_id=s.id, id_hocKy=id_hocKy)

    return count / subjects.__len__()

def stats_hk(class_id, id_hocKy):#thống kê
    list_diemTB_hk1 = db.session.query((Hoc.diem15Phut + Hoc.diem1Tiet * 2 + Hoc.diemThi * 3) / 6, Hoc.subject_id,Hoc.student_id, Hoc.id_hocKy, Student.name) \
                                .join(Student, Student.id == Hoc.student_id) \
                                .filter(Hoc.id_hocKy == id_hocKy) \
                                .group_by(Hoc.subject_id, Hoc.student_id).all()

    dau = 0
    rot = 0
    for item in list_diemTB_hk1:
        if item[0] >= 5:
            dau = dau + 1
        else:
            rot = rot + 1

    return {
        'dau': dau,
        'rot': rot
    }

def diem_trung_binh_lop(class_id):
    # Hoc.diem15Phut, Hoc.diem1Tiet, Hoc.diemThi


    list_student = get_list_student_by_class_id(class_id=class_id)

    dict = []
    i = 1

    for st in list_student:
        TB_hk1 = diem_TB_HK(student_id=st.id, id_hocKy=1)
        TB_hk2 = diem_TB_HK(student_id=st.id, id_hocKy=2)
        dict.append({
            'stt': i,
            'name': st.name,
            'DTB_HK1': "{:.1f}".format(TB_hk1),
            'DTB_HK2': "{:.1f}".format(TB_hk2),
            'ca_nam': "{:.1f}".format((TB_hk1 + TB_hk2) / 2),
            'xep_loai': xap_loai(float("{:.1f}".format((TB_hk1 + TB_hk2) / 2)))
        })
        i = i + 1
    return dict


def xap_loai(diem):
    if diem >= 5:
        return 'Đạt'
    else:
        return 'Rớt'


def thong_ke_theo_HK(class_id, id_hocKy):
    list = get_list_student_by_class_id(class_id=class_id)

    so_luong_dat = 0
    for i in list:
        if float("{:.1f}".format(diem_TB_HK(student_id=i.id, id_hocKy=id_hocKy))) >= 5:
            so_luong_dat = so_luong_dat + 1
    so_luong_rot = list.__len__() - so_luong_dat

    return {
        'so_luong_dat': so_luong_dat,
        'so_luong_rot': so_luong_rot
    }


def thong_ke_theo_nam(class_id):
    list = diem_trung_binh_lop(class_id=class_id)

    so_luong_dat = 0
    for i in list:
        if float(i['ca_nam']) >= 5:
            so_luong_dat = so_luong_dat + 1
    so_luong_rot = list.__len__() - so_luong_dat

    return {
        'so_luong_dat': so_luong_dat,
        'so_luong_rot': so_luong_rot
    }
