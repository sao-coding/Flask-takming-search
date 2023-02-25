from forms import (
    CreateStudentForm,
    EditStudentForm,
    SearchStudentForm,
)
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify, abort
# import json
import time
import datetime
import pytz
import firebase_admin
from firebase_admin import credentials, firestore, auth
from flask_wtf import CSRFProtect

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
# 建立資料庫的實例(db)
db = firestore.client()
# 獲取最新的學生資料
def get_student_data(db):
    student_data_object = db.collection('student_list').order_by('bed').stream()
    student_data = []
    for item in student_data_object:
        student = item.to_dict()
        student['id'] = item.id
        created_at = str(student['created_at']).split('.')[0]
        # student['created_at'] = datetime.datetime.strftime(datetime.datetime.strptime(
        #     created_at, '%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
        student['created_at'] = str(datetime.datetime.strptime(
            created_at, '%Y-%m-%d %H:%M:%S'))
        # print(type(student['created_at']), [student['created_at']])
        student_data.append(student)
    return student_data

student_data = get_student_data(db)

# f = open("data.json","w",encoding="utf-8")
# f.write(json.dumps(student_data, default=str))
# f.close()

id_token = ""

# 引用flask相關資源
# 引用各種表單類別

app = Flask(__name__)

csrf = CSRFProtect(app)
csrf.init_app(app)

# 設定應用程式的SECRET_KEY
app.config['SECRET_KEY'] = 'abc12345678'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
login_token = "login_token"


@app.context_processor
def check_login():
    # 檢查是否有登入
    # print('[檢查是否有登入]')
    # 取得login_token內的session_cookie
    session_cookie = request.cookies.get(login_token)
    # 預設登入狀態
    auth_status = {
        # 登入狀態
        'is_login': False,
        # 是否為管理員
        'is_admin': False,
        # 使用者資訊
        'user_info': {}
    }
    # 準備驗證
    try:
        user_info = auth.verify_session_cookie(
            session_cookie, check_revoked=True)
        # # print('[用戶登入]', user_info)
        admin = db.collection('user_list').where(
            'email', '==', user_info['email']).get()
        admin = [doc.to_dict() for doc in admin]
        # # print('[admin]', admin)
        if admin[0]['admin']:
            auth_status['is_admin'] = True
        # 標記此人為登入狀態
        auth_status['is_login'] = True
        # 將用戶資料存到登入狀態內
        auth_status['user_info'] = admin[0]
    except:
        # 未登入
        # print('[用戶未登入]')
        print("not login")
    return dict(auth_status=auth_status)


@app.before_request
def guard():
    # 檢查是否為管理員
    auth_status = check_login()['auth_status']
    is_admin = auth_status['is_admin']
    is_login = auth_status['is_login']
    # # print('[檢查是否為管理員]', is_admin)
    # 取得目前的路由
    current_route = request.endpoint
    # # print('[目前的路由]', current_route)
    # 定義管理員路由
    admin_route_list = [
        'admin_page',
        'create_page',
        'createfinish_page',
        'edit_page',
        'delete_student',
    ]
    # 定義登入路由
    login_route_list = [
        'search_page',
        'search_student',
        'get_student_info',
    ]
    # 檢查是否為管理員路由
    if current_route in admin_route_list and not is_admin:
        return redirect(url_for('index_page'))

    # 檢查是否為登入路由
    if current_route in login_route_list and not is_login:
        return redirect(url_for('index_page'))


@app.route('/')
def index_page():
    return render_template('index.html')

# TODO:優化Firebase資料庫的讀取數量
@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    # 管理員路由
    page = request.args.get('page', 1, type=int)
    if page < 1:
        page = 1
    student_list = []
    global student_data
    student_list = student_data.copy()
    # student_list = student_data.copy()
    # len_student_list = len(student_list)

    # for doc in collection:
    #     student = doc.to_dict()
    #     student['id'] = doc.id
    #     created_at = str(student['created_at']).split('.')[0]
    #     student['created_at'] = datetime.datetime.strptime(
    #         created_at, '%Y-%m-%d %H:%M:%S')
    #     student_list.append(student)
    page_len = 6
    result = []
    page_list = []
    last_page = int(len(student_list) / page_len) + 1 if len(student_list) % page_len != 0 else int(len(student_list) / page_len)

    total = 0
    count = 0
    form = SearchStudentForm()
    if form.validate_on_submit():
        for i in range(len(student_list)):
            total += 1
            if form.room.data == student_list[i]['room']:
                count += 1
                if count == page_len:
                    break
        page = total // 6
        return redirect("/admin?page="+str(page))

    for i in range(page_len):
        index = (page_len * (page - 1)) + i
        if index < len(student_list):
            result.append(student_list[index])
    student_list = result
    if page - 1 < 1:
        page_list.append(str(page)+"#")
        page_list.append(page)
        page_list.append(page + 1)
        page_list.append(page + 2)
        page_list.append(page + 1)
    elif page + 1 > last_page:
        page_list.append(page - 1)
        page_list.append(page - 2)
        page_list.append(page - 1)
        page_list.append(page)
        page_list.append(str(page)+"#")
    else:
        page_list.append(page - 1)
        page_list.append(page - 1)
        page_list.append(page)
        page_list.append(page + 1)
        page_list.append(page + 1)
    if last_page >= 3:
        page_list.append(4)
    # print('[page_list]', page_list)

    return render_template('admin/index.html', student_list=student_list, page=page, page_list=page_list, last_page=last_page, form=form)


@app.route('/admin/create', methods=['GET', 'POST'])
def create_page():
    form = CreateStudentForm()
    if form.validate_on_submit():
        created_at = datetime.datetime.now(tz=pytz.timezone('Asia/Taipei'))
        # 取得表單資料
        new_student = {
            'country': form.country.data,
            'room': form.room.data,
            'bed': form.bed.data,
            'member_class': form.member_class.data,
            'student_ID': form.student_ID.data,
            'name': form.name.data,
            'ID_number': form.ID_number.data,
            'birthday': datetime.datetime.combine(form.birthday.data, datetime.time(0, 0)),
            'phone': form.phone.data,
            'home_phone': form.home_phone.data,
            'address': form.address.data,
            'emergency_contact': form.emergency_contact.data,
            'emergency_contact_phone': form.emergency_contact_phone.data,
            'created_at': created_at,
        }
        # datetime.datetime.combine(form.birthday.data, datetime.time(0, 0))
        # 新增資料
        db.collection('student_list').add(new_student)
        # 更新後端資料庫
        global student_data
        student_data = get_student_data(db)
        # 把資料存到 session 內
        new_student['birthday'] = new_student['birthday'].strftime('%Y-%m-%d')
        new_student['created_at'] = created_at.strftime('%Y-%m-%d %H:%M:%S')
        title = ['國別', '房號', '床號', '班級', '學號', '姓名', '身分證字號',
                 '生日', '手機', '家裡電話', '地址', '緊急聯絡人', '緊急聯絡人電話', '建立時間']
        new_student = list(zip(title, new_student.values()))
        # print('[新增資料]', new_student)
        session['new_student'] = new_student
        return redirect(url_for('createfinish_page'))
    return render_template('admin/create.html', form=form)


@app.route('/admin/createdone', methods=['GET', 'POST'])
def createfinish_page():
    # 取得 session 內的資料
    new_student = session['new_student']
    # print('[資料]', new_student)
    return render_template('admin/create_done.html', new_student=new_student)


@app.route('/admin/edit/<string:student_id>', methods=['GET', 'POST'])
def edit_page(student_id):
    form = EditStudentForm()
    doc = db.collection('student_list').document(student_id).get()
    student = doc.to_dict()
    # student['birthday'] = student['birthday'].strftime('%Y-%m-%d')
    # student['created_at'] = student['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    if form.validate_on_submit():
        updated_at = datetime.datetime.now(tz=pytz.timezone('Asia/Taipei'))
        # 取得表單資料
        updated_student = {
            'country': form.country.data,
            'room': form.room.data,
            'bed': form.bed.data,
            'member_class': form.member_class.data,
            'student_ID': form.student_ID.data,
            'name': form.name.data,
            'ID_number': form.ID_number.data,
            'birthday': datetime.datetime.combine(form.birthday.data, datetime.time(0, 0)),
            'phone': form.phone.data,
            'home_phone': form.home_phone.data,
            'address': form.address.data,
            'emergency_contact': form.emergency_contact.data,
            'emergency_contact_phone': form.emergency_contact_phone.data,
            'updated_at': updated_at,
        }
        # 更新資料
        db.collection('student_list').document(student_id).update(updated_student)
        global student_data
        student_data = get_student_data(db)

        return redirect(url_for('admin_page'))
    form.country.data = student['country']
    form.room.data = student['room']
    form.bed.data = student['bed']
    form.member_class.data = student['member_class']
    form.student_ID.data = student['student_ID']
    form.name.data = student['name']
    form.ID_number.data = student['ID_number']
    form.birthday.data = student['birthday']
    form.phone.data = student['phone']
    form.home_phone.data = student['home_phone']
    form.address.data = student['address']
    form.emergency_contact.data = student['emergency_contact']
    form.emergency_contact_phone.data = student['emergency_contact_phone']

    return render_template('admin/edit.html', form=form, student=student)


@app.route('/api/delete/<string:student_id>', methods=['POST'])
def delete_student(student_id):
    db.collection('student_list').document(student_id).delete()
    global student_data
    student_data = get_student_data(db)
    return jsonify({'result': 'success'})


@app.route('/search', methods=['GET'])
def search_page():
    return render_template('search.html')


@app.route('/api/search/<string:mode>', methods=['POST'])
def search_student(mode):
    ID_Token = request.json['IDToken']
    search_data = []
    if ID_Token == id_token:
        if mode == 'room':
            room = request.json['search']
            for student in student_data:
                if room in student['room'] and room != '':
                    search_data.append(student)
        elif mode == 'name':
            name = request.json['search']
            for student in student_data:
                if name in student['name'] and name != '':
                    search_data.append(student)

    return jsonify(search_data)


@app.route('/api/info', methods=['POST'])
def get_student_info():
    student_id = request.json['id']
    ID_Token = request.json['IDToken']
    if ID_Token == id_token:
        doc = db.collection('student_list').document(student_id).get()
        student = doc.to_dict()
        student['id'] = doc.id
        student['birthday'] = student['birthday'].strftime('%Y-%m-%d')
        student['created_at'] = student['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(student)


@app.route('/api/login/user', methods=['POST'])
def login_user():
    user = request.json['username']
    doc = db.document(f'user_list/{user}').get()
    if doc.exists:
        check_user = doc.to_dict()
        return jsonify({'email': check_user['email'], 'name': check_user['name']})
    else:
        return jsonify({'email': None, 'name': None})


@app.route('/api/login', methods=['POST'])
def login():
    global id_token
    id_token = request.json['idToken']
    # print('[id_token]', id_token)
    # 過期時間
    expires_in = datetime.timedelta(days=5)
    try:
        # 產生session_cookie
        session_cookie = auth.create_session_cookie(id_token, expires_in)
        # 設定session_cookie的過期時間
        expires = datetime.datetime.now() + expires_in
        # 將session_cookie存到session內
        res = jsonify({'status': 'success'})
        res.set_cookie(login_token, session_cookie, expires=expires, httponly=True, samesite='Lax')
        return res
    except:
        return abort(401, "無效的ID Token")


@app.route('/api/logout', methods=['POST'])
def logout():
    # 登出
    res = jsonify({'status': 'success'})
    res.set_cookie(login_token, expires=0)
    return res


if __name__ == '__main__':
    # 應用程式開始運行
    app.run(host="0.0.0.0", port=2009, debug=True)
