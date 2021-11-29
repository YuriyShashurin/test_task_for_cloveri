from app import db
from werkzeug.security import generate_password_hash
import datetime


def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100))

    def __str__(self):
        return self.role_name


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), unique=True)
    password2 = db.Column(db.String(1000))
    authenticated = db.Column(db.Boolean, default=False)
    role = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticate

    def __str__(self):
        return self.username

    def is_authenticated(self):
        return self.authenticate

    def is_active(self):
        return True


class LectureReview(db.Model):
    __tablename__ = 'lecture_review'

    id = db.Column(db.Integer, primary_key=True)
    consumer = db.Column(db.Integer, db.ForeignKey('customerprofileinfo.id'), nullable=False)
    lecturer = db.Column(db.Integer, db.ForeignKey('lecturerprofileinfo.id'), nullable=False)
    lecture = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    grade = db.Column(db.Integer)
    review_text = db.Column(db.String(500))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())


class Lectures(db.Model):
    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True)
    lectures_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500))
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturerprofileinfo.id'), nullable=False)
    reviews = db.relationship('LectureReview', lazy='joined')

    def __str__(self):
        return self.lectures_name


class LecturerProfileInfo(db.Model):
    __tablename__ = 'lecturerprofileinfo'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_photo1 = db.Column(db.String(50))
    experience = db.Column(db.String(100))
    visit_card = db.Column(db.String(100))
    contact_info = db.relationship('LecturerContactInfo', backref='lecturerprofileinfo', lazy=True)
    lectures = db.relationship('Lectures', backref='lecturer', lazy='joined')

    def __str__(self):
        name = self.first_name + self.last_name
        return name


class CustomerProfileInfo(db.Model):
    __tablename__ = 'customerprofileinfo'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    profile_photo1 = db.Column(db.String(50))
    visit_card = db.Column(db.String(100))
    contact_info = db.relationship('ConsumerContactInfo', backref='customerprofileinfo', lazy='joined')

    def __str__(self):
        name = self.first_name + self.last_name
        return name


class OrderStatus(db.Model):
    __tablename__ = 'order_status'

    id = db.Column(db.Integer, primary_key=True)
    tag_of_status = db.Column(db.String(30))

    def __str__(self):
        return self.tag_of_status


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    lecture = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
    consumer = db.Column(db.Integer, db.ForeignKey('customerprofileinfo.id'), nullable=False)
    lecturer = db.Column(db.Integer, db.ForeignKey('lecturerprofileinfo.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    # Подразумевается ChoisesField в order_status, но так как его не поддерживает flask_alchemy
    # то пока сделал ForeignKey на другую табличку
    order_status = db.Column(db.Integer, db.ForeignKey('order_status.id'))
    description = db.Column(db.String(500))

    def __str__(self):
        title = self.lecture + f'({self.lecturer.first_name + self.lecturer.last_name})' + f'на {self.date}'
        return title


class Cities(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(150))
    utc_time = db.Column(db.String(5), default='utc+3')

    def __str__(self):
        return self.city_name


class LecturerContactInfo(db.Model):
    __tablename__ = 'lecturercontactinfo'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.Integer())
    city = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturerprofileinfo.id'), nullable=False)

    def __str__(self):
        title = f'Контакты лектора {self.lecturer_id.last_name}'
        return title


class ConsumerContactInfo(db.Model):
    __tablename__ = 'consumercontactinfo'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company = db.Column(db.String(500))
    phone = db.Column(db.Integer())
    city = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    consumer_id = db.Column(db.Integer, db.ForeignKey('customerprofileinfo.id'), nullable=False)

    def __str__(self):
        title = f'Контакты клиента {self.consumer_id.last_name}'
        return title


class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)
    chat_for_order = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    chat_messages = db.relationship('ChatMessage', backref='chat', lazy='joined')


class ChatMessage(db.Model):
    __tablename__ = 'chatvessage'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.datetime.now())
    text_message = db.Column(db.String(500))
