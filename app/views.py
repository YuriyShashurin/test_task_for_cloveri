import datetime
from json import dumps

from flask import request, flash, jsonify, redirect
from flask_login import current_user, login_user, logout_user

from app import db, app, login_manager, bcrypt
from app.models import User, Role, CustomerProfileInfo, LecturerProfileInfo, Lectures, LectureReview, Order, \
    OrderStatus, Chat, ChatMessage, Cities, ConsumerContactInfo, LecturerContactInfo


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None


# Create Role for users
@app.route('/create_role', methods=["POST", "GET"])
def dummy_create_role():
    role_name1 = 'Лектор'
    role_name2 = 'Клиент'

    new_role1 = Role(role_name=role_name1)
    new_role2 = Role(role_name=role_name2)
    db.session.add(new_role1)
    db.session.add(new_role2)
    db.session.commit()

    return jsonify(new_role1)


# signup for new users
@app.route('/signup', methods=["POST", "GET"])
def dummy_create_user():
    username1 = 'admin'
    password1 = 'admin'
    role1 = 1
    username2 = 'admin1'
    password2 = 'admin1'
    role2 = 2

    user1 = User(username=username1, role=role1, password2=bcrypt.generate_password_hash(password1).decode('utf-8'),
                 authenticated=False)
    user2 = User(username=username2, role=role2, password2=bcrypt.generate_password_hash(password2).decode('utf-8'),
                 authenticated=False)
    print(user1)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    return jsonify(dumps(user1))


# Login users
@app.route("/login", methods=["GET", "POST"])
def dummy_login():
    password1 = 'admin'
    user = User.query.filter_by(username='admin').first()
    if user:
        if bcrypt.check_password_hash(user.password2, password1):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
        else:
            flash('Введен неправильный логин/пароль')
    data = {
        "username": user.username,
        'auth': user.authenticated,
        'role': user.role,
    }

    return jsonify(data)


# logout users
@app.route('/logout', methods=["GET"])
def logout():
    user = User.query.filter_by(id=current_user.id).first()
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return "Пользователь вышел"


# Create new profile for customer
@app.route('/create_customer_profile', methods=["POST"])
def dummy_create_customer_profile():
    user = 7
    first_name = 'Юрий'
    last_name = 'Шашурин'
    profile_photo = 'dump'
    visit_card = 'Немного о себе'
    new_profile = CustomerProfileInfo(user=user, first_name=first_name, last_name=last_name,
                                      profile_photo1=profile_photo, visit_card=visit_card)
    db.session.add(new_profile)
    db.session.commit()
    data = {
        "user": new_profile.user,
        'first_name': new_profile.first_name,
        'last_name': new_profile.last_name,
        'profile_photo': new_profile.profile_photo1,
        'visit_card': new_profile.visit_card,
        'contact_info': new_profile.contact_info,
    }

    return jsonify(data)


# Create new profile for lecture
@app.route('/create_lecture_profile', methods=["GET", "POST"])
def dummy_create_lecture_profile():
    user = 6
    first_name = 'Юрий'
    last_name = 'Шашурин'
    profile_photo = 'dump'
    visit_card = 'Немного о себе'
    experience = 'Somethind about experience'
    new_profile = LecturerProfileInfo(user=user,
                                      first_name=first_name,
                                      last_name=last_name,
                                      profile_photo1=profile_photo,
                                      experience=experience,
                                      visit_card=visit_card)

    db.session.add(new_profile)
    db.session.commit()
    data = {
        "user": new_profile.user,
        'first_name': new_profile.first_name,
        'last_name': new_profile.last_name,
        'profile_photo': new_profile.profile_photo1,
        'visit_card': new_profile.visit_card,
        'experience': new_profile.experience,
        'contact_info': new_profile.contact_info,
        'lectures': new_profile.lectures,
    }

    return jsonify(data)


# Get or edit profile data for lecture
@app.route('/lecture_profile/<id>', methods=["GET", "PUT"])
def dummy_edit_lecture_profile(id):
    if request.method == 'GET':
        profile = LecturerProfileInfo.query.filter_by(id=id).first()
        lectures = []
        for lecture in profile.lectures:
            lecture_data = {
                "user": lecture.lectures_name,
                'description': lecture.description,
                'lecturer_id': lecture.lecturer_id,
            }
            lectures.append(lecture_data)
        contacts = []
        for contact in profile.contact_info:
            contact_data = {
                "id": contact.id,
                'email': contact.email,
                'phone': contact.phone,
                'city': contact.city,
                'lecturer_id': contact.lecturer_id,
            }
            contacts.append(contact_data)

        data = {
            "user": profile.user,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_photo': profile.profile_photo1,
            'visit_card': profile.visit_card,
            'experience': profile.experience,
            'contact_info': contacts,
            'lectures': lectures,
        }

        return jsonify(data)

    if request.method == 'PUT':
        profile_photo = 'dump2'
        edit_profile = LecturerProfileInfo.query.filter_by(id=id).first()
        edit_profile.profile_photo = profile_photo
        db.session.add(edit_profile)
        db.session.commit()
        lectures = []
        for lecture in edit_profile.lectures:
            lecture_data = {
                "user": lecture.lectures_name,
                'description': lecture.description,
                'lecturer_id': lecture.lecturer_id,
            }
            lectures.append(lecture_data)
        contacts = []
        for contact in edit_profile.contact_info:
            contact_data = {
                "id": contact.id,
                'email': contact.email,
                'phone': contact.phone,
                'city': contact.city,
                'lecturer_id': contact.lecturer_id,
            }
            contacts.append(contact_data)
        data = {
            "user": edit_profile.user,
            'first_name': edit_profile.first_name,
            'last_name': edit_profile.last_name,
            'profile_photo': edit_profile.profile_photo1,
            'visit_card': edit_profile.visit_card,
            'experience': edit_profile.experience,
            'contact_info': contacts,
            'lectures': lectures,
        }

        return jsonify(data)


# Get or edit profile data for customer
@app.route('/customer_profile/<id>', methods=["GET", "PUT"])
def dummy_edit_customer_profile(id):
    if request.method == 'GET':
        profile = CustomerProfileInfo.query.filter_by(id=id).first()
        contacts = []
        for contact in profile.contact_info:
            contact_data = {
                "id": contact.id,
                'email': contact.email,
                'company': contact.company,
                'phone': contact.phone,
                'city': contact.city,
                'consumer_id': contact.consumer_id,
            }
            contacts.append(contact_data)
        data = {
            "user": profile.user,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'profile_photo': profile.profile_photo1,
            'visit_card': profile.visit_card,
            'contact_info': contacts,
        }
        return jsonify(data)
    if request.method == 'PUT':
        profile_photo = 'dump2'
        edit_profile = CustomerProfileInfo.query.filter_by(id=id).first()
        edit_profile.profile_photo1 = profile_photo
        db.session.add(edit_profile)
        db.session.commit()
        contacts = []
        for contact in edit_profile.contact_info:
            contact_data = {
                "id": contact.id,
                'email': contact.email,
                'company': contact.company,
                'phone': contact.phone,
                'city': contact.city,
                'consumer_id': contact.consumer_id,
            }
            contacts.append(contact_data)
        data = {
            "user": edit_profile.user,
            'first_name': edit_profile.first_name,
            'last_name': edit_profile.last_name,
            'profile_photo': edit_profile.profile_photo1,
            'visit_card': edit_profile.visit_card,
            'contact_info': contacts,
        }

        return jsonify(data)


# Create new lecture
@app.route('/create_lectures', methods=["POST"])
def dummy_create_lecture():
    lectures_name = 'Science in XXI century'
    description = 'description'
    lecturer_id = 2
    new_lecture = Lectures(lectures_name=lectures_name, description=description, lecturer_id=lecturer_id)
    db.session.add(new_lecture)
    db.session.commit()
    data = {
        "user": new_lecture.lectures_name,
        'description': new_lecture.description,
        'lecturer_id': new_lecture.lecturer_id,
        'reviews': new_lecture.reviews,
    }

    return jsonify(data)


# Get, edit or delete lecture
@app.route('/lectures', methods=["GET"])
def dummy_get_all_lectures():
    lectures = Lectures.query.all()
    lectures_list = []
    for lecture in lectures:
        data = {
            "lectures_name": lecture.lectures_name,
            'description': lecture.description,
            'lecturer_id': lecture.lecturer_id,
            # 'reviews': lecture.reviews,
        }
        lectures_list.append(data)
    return jsonify(lectures_list)


# Get, edit or delete lecture
@app.route('/lecture/<id>', methods=["GET", "PUT", "DELETE"])
def dummy_lecture(id):
    if request.method == 'GET':
        new_lecture = Lectures.query.filter_by(id=id).first()
        data = {
            "lectures_name": new_lecture.lectures_name,
            'description': new_lecture.description,
            'lecturer_id': new_lecture.lecturer_id,
            # 'reviews': new_lecture.reviews,
        }

        return jsonify(data)
    if request.method == 'PUT':
        description = 'new description'
        new_lecture = Lectures.query.filter_by(id=id).first()
        new_lecture.description = description
        db.session.add(new_lecture)
        db.session.commit()
        data = {
            "user": new_lecture.lectures_name,
            'first_name': new_lecture.description,
            'last_name': new_lecture.lecturer_id,
            'reviews': new_lecture.reviews,
        }

        return jsonify(data)
    if request.method == 'DELETE':
        lecture = Lectures.query.filter_by(id=id).first()
        db.session.delete(lecture)
        db.session.commit()
        return "Delete"


# Create lecture_review
@app.route('/add_lecture_review', methods=["POST"])
def dump_add_lecture_review():
    consumer = 4
    lecturer = 2
    lecture = 7
    grade = 5
    review_text = "All is fine. Good job"
    date = datetime.datetime.now()
    new_review = LectureReview(consumer=consumer, lecturer=lecturer, lecture=lecture, grade=grade,
                               review_text=review_text, date=date)
    db.session.add(new_review)
    db.session.commit()
    data = {
        "consumer": new_review.consumer,
        'lecturer': new_review.lecturer,
        'lecture': new_review.lecture,
        'grade': new_review.grade,
        'review_text': new_review.review_text,
        'date': new_review.date,
    }

    return jsonify(data)


# Get, edit or delete lecture_review
@app.route('/review_of_lecture/<id>', methods=["GET", "PUT", "DELETE"])
def dummy_review_of_lecture(id):
    if request.method == 'GET':
        review = LectureReview.query.filter_by(id=id).first()
        data = {
            "consumer": review.consumer,
            'lecturer': review.lecturer,
            'lecture': review.lecture,
            'grade': review.grade,
            'review_text': review.review_text,
            'date': review.date,
        }

        return jsonify(data)
    if request.method == 'PUT':
        review_text = 'new review_text'
        edit_review = LectureReview.query.filter_by(id=id).first()
        edit_review.review_text = review_text
        db.session.add(edit_review)
        db.session.commit()
        data = {
            "consumer": edit_review.consumer,
            'lecturer': edit_review.lecturer,
            'lecture': edit_review.lecture,
            'grade': edit_review.grade,
            'review_text': edit_review.review_text,
            'date': edit_review.date,
        }

        return jsonify(data)
    if request.method == 'DELETE':
        review = LectureReview.query.filter_by(id=id).first()
        db.session.delete(review)
        db.session.commit()
        return "Delete"


# Create order_status
@app.route('/add_order_status', methods=["POST"])
def dummy_add_order_status():
    tags_of_status = ('Created', 'Apply', 'Finished', 'Canceled', 'Canceled', 'Refused')
    for status in tags_of_status:
        new_status = OrderStatus(tag_of_status=status)
        db.session.add(new_status)
        db.session.commit()

    return "statuses have been added"


# Create order
@app.route('/create_order', methods=["POST"])
def dummy_create_order():
    lecture = 7
    consumer = 4
    lecturer = 2
    date = datetime.datetime.now()
    order_status = 1
    description = 'This is description'
    new_order = Order(lecture=lecture, consumer=consumer, lecturer=lecturer, date=date, order_status=order_status,
                      description=description)
    db.session.add(new_order)
    db.session.commit()
    data = {
        "lecture": new_order.lecture,
        'consumer': new_order.consumer,
        'lecturer': new_order.lecturer,
        'date': new_order.date,
        'order_status': new_order.order_status,
        'description': new_order.description,
    }

    return jsonify(data)


# Get, edit or delete order
@app.route('/order/<id>', methods=["GET", "PUT"])
def dummy_order(id):
    if request.method == 'GET':
        order = Order.query.filter_by(id=id).first()
        data = {
            "lecture": order.lecture,
            'consumer': order.consumer,
            'lecturer': order.lecturer,
            'date': order.date,
            'order_status': order.order_status,
            'description': order.description,
        }

        return jsonify(data)
    if request.method == 'PUT':
        description = 'new description'
        edit_order = Order.query.filter_by(id=id).first()
        edit_order.description = description
        db.session.add(edit_order)
        db.session.commit()
        data = {
            "lecture": edit_order.lecture,
            'consumer': edit_order.consumer,
            'lecturer': edit_order.lecturer,
            'date': edit_order.date,
            'order_status': edit_order.order_status,
            'description': edit_order.description,
        }

        return jsonify(data)


# Get all_orders
@app.route('/consumer_orders', methods=["GET"])
def dummy_get_all_orders():
    orders = Order.query.all()
    final_data = []
    for order in orders:
        data = {
            "lecture": order.lecture,
            'consumer': order.consumer,
            'lecturer': order.lecturer,
            'date': order.date,
            'order_status': order.order_status,
            'description': order.description,
        }
        final_data.append(data)

    return jsonify(final_data)


# Get all_orders_ by consumer id
@app.route('/consumer_orders/<consumer_id>', methods=["GET"])
def dummy_get_all_orders_by_consumer_id(consumer_id):
    orders = Order.query.filter_by(consumer=consumer_id).all()
    final_data = []
    for order in orders:
        data = {
            "lecture": order.lecture,
            'consumer': order.consumer,
            'lecturer': order.lecturer,
            'date': order.date,
            'order_status': order.order_status,
            'description': order.description,
        }
        final_data.append(data)

    return jsonify(final_data)


# Get all_orders_ by lecturer id
@app.route('/lecturer_orders/<lecturer_id>', methods=["GET"])
def dummy_get_all_orders_by_lecturer_id(lecturer_id):
    orders = Order.query.filter_by(lecturer=lecturer_id).all()
    final_data = []
    for order in orders:
        data = {
            "lecture": order.lecture,
            'consumer': order.consumer,
            'lecturer': order.lecturer,
            'date': order.date,
            'order_status': order.order_status,
            'description': order.description,
        }
        final_data.append(data)

    return jsonify(final_data)


# Create new chat
@app.route('/create_chat', methods=["POST"])
def dummy_create_chat():
    chat_for_order = 1
    new_chat = Chat(chat_for_order=chat_for_order)
    db.session.add(new_chat)
    db.session.commit()
    data = {
        "id": new_chat.id,
        'chat_for_order': new_chat.chat_for_order,
        'chat_messages': new_chat.chat_messages,
    }
    return jsonify(data)


# Get chat with messages
@app.route('/chat/<id>', methods=["GET"])
def dummy_chat(id):
    chat = Chat.query.filter_by(id=id).first()
    print(chat.chat_messages)
    messages = []
    for message in chat.chat_messages:
        print(message.id)
        message_data = {
            "id": message.id,
            'chat_id': message.chat_id,
            'sender': message.sender,
            'recipient': message.recipient,
            'date_time': message.date_time,
            'text_message': message.text_message,
        }
        messages.append(message_data)

    print(messages)

    data = {
        "id": chat.id,
        'chat_for_order': chat.chat_for_order,
        'chat_messages': messages,
    }
    return jsonify(data)


# Create new message
@app.route('/create_message', methods=["POST"])
def dummy_create_message():
    chat_id = 2
    sender = 6
    recipient = 7
    date_time = datetime.datetime.now()
    text_message = 'New Message'
    new_message = ChatMessage(chat_id=chat_id, sender=sender, recipient=recipient, date_time=date_time,
                              text_message=text_message)
    db.session.add(new_message)
    db.session.commit()
    data = {
        "id": new_message.id,
        'chat_id': new_message.chat_id,
        'sender': new_message.sender,
        'recipient': new_message.recipient,
        'date_time': new_message.date_time,
        'text_message': new_message.text_message,
    }
    return jsonify(data)


# Delete message
@app.route('/delete_message/<id>', methods=["DELETE"])
def dummy_delete_message(id):
    message = ChatMessage.query.filter_by(id=id).first()
    db.session.delete(message)
    db.session.commit()
    return "message delete"


# Add new City
@app.route('/add_city', methods=["POST"])
def dummy_add_city():
    city_name = "Moscow"
    utc_time = 'utc+3'
    new_city = Cities(city_name=city_name, utc_time=utc_time)
    db.session.add(new_city)
    db.session.commit()
    return 'Город добавлен'


# Add new contacts
@app.route('/add_contacts', methods=["POST"])
def dummy_add_profile():
    if request.args.get('type') == 'Consumer':
        email = "1232"
        company = "very cool company"
        phone = 1
        city = 1
        consumer_id = 4
        new_profile = ConsumerContactInfo(email=email, company=company, phone=phone, city=city, consumer_id=consumer_id)
        db.session.add(new_profile)
        db.session.commit()
        return redirect(f'/customer_profile/{consumer_id}')

    if request.args.get('type') == 'Lecturer':
        email = "aa@aa1232.ru"
        phone = 1
        city = 1
        lecturer_id = 2
        new_profile = LecturerContactInfo(email=email, phone=phone, city=city, lecturer_id=lecturer_id)
        db.session.add(new_profile)
        db.session.commit()
        return redirect(f'/lecture_profile/{lecturer_id}')


# Get avg rating for lecture by lecturer_id and lecture_id
@app.route('/get_avg_rating/<lecturer_id>/<lecture_id>', methods=["GET"])
def dummy_get_avg_rating_for_lecture_id(lecturer_id, lecture_id):
    reviews = LectureReview.query.filter_by(lecturer=lecturer_id, lecture=lecture_id).all()
    grades = []
    for i in reviews:
        grades.append(i.grade)

    try:
        avg_rating = sum(grades) / len(grades)
        return str(avg_rating)
    except:
        return str(0)


# Get avg rating for lecturer by lecturer_id
@app.route('/get_avg_rating/<lecturer_id>', methods=["GET"])
def dummy_get_avg_rating_for_lecturer(lecturer_id):
    reviews = LectureReview.query.filter_by(lecturer=lecturer_id).all()
    grades = []
    for i in reviews:
        grades.append(i.grade)

    try:
        avg_rating = sum(grades) / len(grades)
        return str(avg_rating)
    except:
        return str(0)


# Total finished orders by lecturer or consumer
@app.route('/orders_finished/<profile_id>', methods=["GET"])
def dummy_total_finished_orders_by_profile(profile_id):
    if request.args.get('type') == 'Consumer':
        orders = Order.query.filter_by(consumer=profile_id, order_status=3).all()
        return str(len(orders))
    if request.args.get('type') == 'Lecturer':
        orders = Order.query.filter_by(lecturer=profile_id, order_status=3).all()
        return str(len(orders))


# Total finished orders
@app.route('/orders_finished', methods=["GET"])
def dummy_total_finished_orders():
    orders = Order.query.filter_by(order_status=3).all()
    return str(len(orders))


# Change order status
@app.route('/change_order_status/<order_id>', methods=["PUT"])
def dummy_change_order_status(order_id):
    order = Order.query.filter_by(id=order_id).first()
    new_status = request.args.get('status')
    order.order_status = int(new_status)
    db.session.add(order)
    db.session.commit()
    data = {
        "lecture": order.lecture,
        'consumer': order.consumer,
        'lecturer': order.lecturer,
        'date': order.date,
        'order_status': order.order_status,
        'description': order.description,
    }
    return jsonify(data)


# SUM messages in the chat by chat_id
@app.route('/sum_messages/<chat_id>', methods=["GET"])
def sum_messages(chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()
    return str(len(chat.chat_messages))
