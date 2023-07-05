from faker import Faker
from datetime import date, datetime, timedelta
from random import randint, choice
from sqlalchemy import select
from database.models import Teacher, Student, Subject, Grade, Group, Base
from database.db import session
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def date_range(start: date, end: date) -> list:
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data():
    subjects = ['Вища математика', 'Технічна механіка', 'Економіка підприємства', 'Програмне забезпечення', 'Основи програмування', 'Промислові мережі', 'ТАУ', 'Архітектура ЕОМ']

    groups = ['AВ76', 'ЕП17', 'МР01', 'CA10']

    fake = Faker(locale='uk_UA')
    number_of_teachers = 5
    number_of_students = 50

    def seed_teachers():
        for _ in range(number_of_teachers):
            teacher = Teacher(name=fake.name())
            session.add(teacher)
        session.commit()

    def seed_subjects():
        teacher_ids = session.scalars(select(Teacher.id)).all()
        for subject in subjects:
            session.add(Subject(name=subject, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        for group in groups:
            session.add(Group(name=group))
        session.commit()

    def seed_students():
        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(number_of_students):
            student = Student(name=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        start_date = datetime.strptime("2020-09-01", "%Y-%m-%d")
        end_date = datetime.strptime("2021-05-25", "%Y-%m-%d")
        d_range = date_range(start=start_date, end=end_date)
        subject_ids = session.scalars(select(Subject.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range: 
            random_id_subject = choice(subject_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]
            for student_id in random_ids_student:
                grade = Grade(grade=randint(1, 12), date_of=d, student_id=student_id,subject_id=random_id_subject)
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_subjects()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == '__main__':
    fill_data()
