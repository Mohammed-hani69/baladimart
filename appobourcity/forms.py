from wtforms.validators import Optional, NumberRange
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FloatField, IntegerField, PasswordField, SelectField, SelectMultipleField, StringField, EmailField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length , NumberRange, URL
from flask_wtf.file import FileRequired, FileAllowed

# تعريف نموذج Flask-WTF لإضافة التاجر
class SellerForm(FlaskForm):
    seller_name = StringField('اسم التاجر', validators=[DataRequired(), Length(min=3, max=255)])
    store_name = StringField('اسم المتجر', validators=[DataRequired(), Length(min=3, max=255)])
    store_category = SelectField('تخصص المتجر', validators=[DataRequired(), Length(min=3, max=255)])
    email = EmailField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    phone = StringField('رقم الهاتف', validators=[DataRequired()])
    address = StringField('العنوان', validators=[Length(max=255)])
    password = PasswordField('كلمة المرور', validators= [DataRequired() , Length( min = 8 , max = 16)])
    
    # حقول الصور مع التحقق من النوع
    store_image = FileField('صورة المتجر', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'الرجاء تحميل صورة بصيغة PNG، JPG، أو GIF')
    ])
    owner_image = FileField('صورة صاحب المتجر', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'الرجاء تحميل صورة بصيغة PNG، JPG، أو GIF')
    ])

    owner_banner = FileField('صورة صاحب المتجر', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'الرجاء تحميل صورة بصيغة PNG، JPG، أو GIF')
    ])
    status = BooleanField('البائع نشط؟', default=True)
    submit = SubmitField("أضافة")


class CategoryForm(FlaskForm):
    category_name = StringField('اسم القسم', validators=[DataRequired()])
    image_category = FileField('صورة القسم', validators=[DataRequired()])
    submit = SubmitField('إضافة القسم')



class Types_of_servicesForm(FlaskForm):
    Types_of_services_name = StringField('اسم نوع الخدمه', validators=[DataRequired()])
    image_Types_of_services = FileField('صورة نوع الخدمه', validators=[DataRequired()])
    submit = SubmitField('إضافة نوع الخدمه')




class ServiceForm(FlaskForm):
    service_name = StringField('اسم الخدمة', validators=[DataRequired(), Length(max=255)])
    provider_name = StringField('اسم مقدم الخدمة', validators=[DataRequired(), Length(max=255)])
    typesofservices = StringField('نوع الخدمه', default='0')
    address = StringField('العنوان', validators=[DataRequired(), Length(max=255)])
    phone = StringField('رقم الهاتف', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('وصف الخدمة', validators=[DataRequired()])
    price = IntegerField('التكلفة', validators=[DataRequired(), NumberRange(min=1)])
    experience_years = StringField('سنوات الخبره', validators=[DataRequired(), Length(max=255)])
    service_image = FileField('صورة الخدمة')
    submit = SubmitField('إضافة الخدمة')




class NotificationForm(FlaskForm):
    send_to = SelectField('Send To', choices=[('all', 'All'),('single', 'Single') ], validators=[DataRequired()])
    seller_email = EmailField('بريد البائع', validators=[DataRequired() , Email()])
    title = StringField('عنوان الإشعار', validators=[DataRequired()])
    message = TextAreaField('نص الإشعار', validators=[DataRequired()])
    action_url = StringField('رابط الإشعار', validators=[DataRequired()])
    submit = SubmitField('إرسال')





class BannerForm(FlaskForm):
    title = StringField('عنوان البنر', validators=[DataRequired()])
    typebanner = SelectField('نوع البنر', choices=[
        ('homepage', 'البانر الرئيسي'),
        ('topright', 'الايمن العلوي'),
        ('topcenter', 'الاوسط العلوي'),
        ('topleft', 'الايسر العلوي'),
        ('centerright', 'الايمن المركزي'),
        ('centerleft', 'الايسر المركزي'),
        ('category1', 'منتجات1'),
        ('category2', 'منتجات2'),
        ('category3', 'منتجات3'),
        ('category4', 'منتجات4'),
        ('bottomright', 'الايمن السفلي'),
        ('bottomcenter', 'الاوسط السفلي'),
        ('bottomleft', 'الايسر السفلي'),
    ], validators=[DataRequired()])
    image = FileField('صورة البنر', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], 'الرجاء تحميل صورة بصيغة JPG أو PNG')
    ])
    link = StringField('الرابط', validators=[URL(message='الرجاء إدخال رابط صالح')])
    is_active = BooleanField('نشط')
    submit = SubmitField('إضافة')

#===================================================================================
#===================================================================================
#=============================trader ===============================================
#=============================trader ===============================================
#===================================================================================
#===================================================================================





class LoginForm(FlaskForm):
    email = EmailField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators= [DataRequired() , Length( min = 8 , max = 16)]
    )
    submit = SubmitField("دخول")


# نموذج إدخال بيانات المنتج
class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_category = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired()])
    discount = FloatField('discount', validators=[Optional(), NumberRange(min=0)], default=0.0)
    stock_quantity = IntegerField('Stock Quantity', validators=[DataRequired()])
    image1 = FileField('Image 1')
    image2 = FileField('Image 2')
    image3 = FileField('Image 3')
    image4 = FileField('Image 4')
    image5 = FileField('Image 5')
    submit = FileField('حفظ المنتج')




class SubcategoryForm(FlaskForm):
    name = StringField('اسم القسم الفرعي', validators=[DataRequired(), Length(max=255)])
    image = FileField('صورة القسم الفرعي', validators=[DataRequired()])
    submit = SubmitField('إضافة القسم الفرعي')



#=================================  offer  ==================================================

class OfferForm(FlaskForm):
    name = StringField('اسم العرض', validators=[DataRequired()])
    code = StringField('كود العرض', validators=[DataRequired()])
    typename = SelectField('نوع العرض (نسبي أو ثابت)', choices=[
        ('discount', ' نسبي'),
        ('value', ' ثابت'),
    ], validators=[DataRequired()])
    discount_value = FloatField('قيمة الخصم', validators=[DataRequired(), NumberRange(min=0)])
    start_date = DateField('تاريخ البداية', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('تاريخ النهاية', format='%Y-%m-%d', validators=[DataRequired()])
    description = TextAreaField('الوصف', validators=[])
    image = FileField('صورة العرض', validators=[])
    products = SelectMultipleField(
        'اختر المنتجات', 
        choices=[],  # يتم ملؤها ديناميكيًا في العرض
        validators=[DataRequired()],
        render_kw={"class": "form-control", "multiple": True}  # إضافة سمات HTML
    )  # المنتجات كقائمة متعددة
    status = BooleanField('نشط', default=True)
    submit = SubmitField('حفظ العرض')

#======================================   site   =============================
#======================================   site   =============================
#======================================   site   =============================
#======================================   site   =============================



class UserForm(FlaskForm):
    
    seller_name = StringField('الاسم', validators=[DataRequired()])
    email = EmailField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    phone = StringField('رقم الهاتف', validators=[DataRequired()])
    governorate = StringField('المحافظة', validators=[DataRequired()])
    city = StringField('المدينة', validators=[DataRequired()])
    village = StringField('الحي', validators=[DataRequired()])
    street_address = StringField('الشارع و رقم المنزل ', validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=8, max=255)])
    submit = SubmitField('تسجيل')

    



