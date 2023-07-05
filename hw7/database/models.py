from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship("Student", back_populates="group")


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete="CASCADE"))

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete="CASCADE"))
    date = Column(DateTime)
    grade = Column(Integer)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
