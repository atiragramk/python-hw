from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UUID, ForeignKey, select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import uuid
import random

from os import getenv

Base = declarative_base()
DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'
names = ['Katlyn', 'Lorri', 'Elaine', 'John', 'Valerie', 'Terri']
subjects = ['English', 'Math', 'History', 'Chemistry', 'Franch', 'Religion']


class Student(Base):
    __tablename__ = 'student'

    id = Column(UUID, primary_key=True)
    name = Column(String)
    age = Column(Integer)

    def __str__(self):
        return f'This is {self.id} student {self.name}. Age: {self.age}'

    def __repr__(self):
        return f'This is {self.id} student {self.name}. Age: {self.age}'


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(UUID, primary_key=True)
    name = Column(String)

    def __str__(self):
        return f'This is {self.id} subject {self.name}.'

    def __repr__(self):
        return f'This is {self.id} subject {self.name}.'


class Student_Subject(Base):
    __tablename__ = 'student_subject'

    id = Column(UUID, primary_key=True, nullable=False)
    student_id = Column('student_id', UUID, ForeignKey(
        'student.id'), nullable=False)
    subject_id = Column('subject_id', UUID, ForeignKey(
        'subject.id'), nullable=False)

    def __str__(self):
        return f'This is {self.id} with students {self.student_id} on subjects {self.subject_id}.'

    def __repr__(self):
        return f'This is {self.id} with students {self.student_id} on subjects {self.subject_id}.'


engine = create_engine(
    DATABASE_URI.format(
        host='localhost',
        database=getenv("DB_NAME"),
        user=getenv("USER"),
        password=getenv("PASSWORD"),
        port=5432,
    )
)

Base.metadata.create_all(engine)


def create_students():
    with Session(engine) as session:
        for el in names:
            student = Student(id=uuid.uuid4(), name=el,
                              age=random.randint(18, 25))
            session.add(student)
        session.commit()


def create_subject():
    with Session(engine) as session:

        for el in subjects:
            subject = Subject(id=uuid.uuid4(), name=el)
            session.add(subject)
        session.commit()


def follow_subject():
    with Session(engine) as session:
        for i in range(10):
            stmt_student = select(Student.id).where(
                Student.name == random.choice(names))
            student_id = session.scalar(stmt_student)
            stmt_subject = select(Subject.id).where(
                Subject.name == random.choice(subjects))
            subject_id = session.scalar(stmt_subject)

            student_subject = Student_Subject(
                id=uuid.uuid4(), student_id=student_id, subject_id=subject_id)
            session.add(student_subject)
        session.commit()


def get_english_students():
    with Session(engine) as session:
        stmt_student = select(Student.name).join(Student_Subject, Student.id == Student_Subject.student_id).join(
            Subject, Student_Subject.subject_id == Subject.id).filter(Subject.name == 'English')
        students_name = session.execute(stmt_student).all()
        for el in students_name:
            print(el[0])
