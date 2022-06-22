from doctest import debug

from Tools.scripts.var_access_benchmark import B
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.strategy_options import defer

from QLHS import db
from datetime import datetime
from enum import Enum as UserEnum, unique
from flask_login import UserMixin


class BaseModels(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class Gender(UserEnum):
    MALE = 1
    FEMALE = 2


class UserRole(UserEnum):
    ADMIN = 1
    TEACHER = 2
    EMPLOYEE = 3


class User(BaseModels, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), nullable=False)

    def __str__(self):
        return self.username


class Nam_hoc(BaseModels):
    name = Column(String(20), nullable=False)
    classes = relationship('Lop_hoc', backref='nam_hoc', lazy=True)
    hoc_ky = relationship('Hoc_ky', backref='nam_hoc', lazy=True)

    def __str__(self):
        return self.name


class Hoc_ky(BaseModels):
    name = Column(String(50), nullable=False)
    nam_id = Column(Integer, ForeignKey(Nam_hoc.id), nullable=False)

    def __str__(self):
        return self.name

class Hoc(db.Model):
    student_id = Column(Integer, ForeignKey('student.id'), nullable=False, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False, primary_key=True)
    diem15Phut = Column(Float, default=0)
    diem1Tiet = Column(Float, default=0)
    diemThi = Column(Float, default=0)
    id_hocKy = Column(Integer, ForeignKey(Hoc_ky.id), nullable=False, primary_key=True)
    hoc_ky = relationship('Hoc_ky', backref='hoc', lazy=True, uselist=False)




class Subject(BaseModels):
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Grade(BaseModels):
    name = Column(String(50), nullable=False, unique=True)
    classes = relationship('Lop_hoc', backref='grade', lazy=False)

    def __str__(self):
        return self.name


class Lop_hoc(BaseModels):
    name = Column(String(20), nullable=False)
    quantity = Column(Integer, default=40)
    students = relationship('Student', backref='lop_hoc', lazy=False)
    grade_id = Column(Integer, ForeignKey(Grade.id), nullable=False)
    ma_nam_hoc = Column(Integer, ForeignKey(Nam_hoc.id), nullable=False)

    def __str__(self):
        return self.name


class Teacher(BaseModels):
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)  # True: male and False: famale

    address = Column(String(100))
    email = Column(String(50))
    day_of_birth = Column(DateTime)
    class_id = Column(Integer, ForeignKey(Lop_hoc.id))
    lop_hoc = relationship('Lop_hoc', backref='teacher', lazy=False, uselist=False)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship('User', backref='teacher', uselist=False)

    def __str__(self):
        return self.name


class Employee(BaseModels):
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)  # True: male and False: famale

    address = Column(String(100))
    email = Column(String(50))
    day_of_birth = Column(DateTime)
    id_user = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship('User', backref='employee', uselist=False)

    def __str__(self):
        return self.name


class Student(BaseModels):
    name = Column(String(50), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    email = Column(String(50))
    day_of_birth = Column(DateTime)
    phone_number = Column(String(11))
    address = Column(String(100))
    class_id = Column(Integer, ForeignKey(Lop_hoc.id), default=None)
    subjects = relationship('Subject', secondary='hoc', lazy='subquery', backref=backref('student', lazy=True))

    def __str__(self):
        return self.name


# class Student(BaseModels):
#     gender = Column(Boolean, nullable=False)
#     address = Column(String(100))

if __name__ == "__main__":
    db.create_all()
