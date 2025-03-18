# app.py
import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
from sqlalchemy import text  # استيراد text
# تفعيل قيود المفاتيح الخارجية عند إنشاء الاتصال
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_cors import CORS








# إنشاء تطبيق Flask
app = Flask(__name__)
CORS(app)
# ضمان وجود مجلد /data لتخزين قاعدة البيانات
DATA_DIR = "/data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# إعدادات قاعدة البيانات لحفظها في /data لضمان استمراريتها على Fly.io
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DATA_DIR, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Y5lKJk50mo_mx0N-ZY0fYCxnn6SUHlUvnzPzOQ'
app.config["JWT_SECRET_KEY"] = "b4b38504c6b61a7529e353a1c5b3d42b142739b23ce8ca8ac2c7770c24259bf7"  # استخدم مفتاحًا سريًا قويًا
jwt = JWTManager(app)
db = SQLAlchemy()




@app.before_request
def enable_foreign_keys():
    db.session.execute(text('PRAGMA foreign_keys = ON;'))
# تهيئة LoginManager واحد
login_manager = LoginManager(app)
login_manager.login_message = 'الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.'
login_manager.login_message_category = 'info'

# ربط التطبيق
login_manager.init_app(app)

# إعداد صفحة تسجيل الدخول الافتراضية
login_manager.login_view = 'login'  # الافتراضية (يمكن تغييرها ديناميكيًا)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)
app.app_context().push()

CORS(app)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


# إعداد المجلد لحفظ الصور
app.config['UPLOAD_FOLDER_QRCODE'] = 'appobourcity/static/uploads/qrcode'
app.config['UPLOAD_FOLDER'] = 'appobourcity/static/uploads/'
app.config['UPLOAD_FOLDER_TRADER_BANNER'] = 'appobourcity/static/uploads/Trader/banner'
app.config['UPLOAD_FOLDER_TRADER_LOGO'] = 'appobourcity/static/uploads/Trader/logo'
app.config['SERVICE_FOLDER'] = 'appobourcity/static/uploads/services'
app.config['PRODUCTS_FOLDER'] = 'appobourcity/static/uploads/products'
app.config['CATEGORY_FOLDER'] = 'appobourcity/static/uploads/category'
app.config['OFFER_FOLDER'] = 'appobourcity/static/uploads/offer'
app.config['SUBCATEGORIES_FOLDER'] = 'appobourcity/static/uploads/category/subcategories'
app.config['BANNERS_FOLDER'] = 'appobourcity/static/uploads/banners'
app.config['Types_of_services_FOLDER'] = 'appobourcity/static/uploads/Types_of_services'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif' ,'avif','svg'}

db.init_app(app)

from appobourcity import routes