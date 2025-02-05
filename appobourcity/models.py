from datetime import date, datetime
from appobourcity import db , bcrypt
from flask_login import UserMixin
from babel.dates import format_datetime






class Seller(db.Model, UserMixin):
    __tablename__ = 'sellers'
    
    seller_id = db.Column(db.Integer, primary_key=True, nullable=False)
    seller_name = db.Column(db.String(255), nullable=False)
    store_name = db.Column(db.String(255), nullable=True)
    store_category = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False)
    governorate = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    village = db.Column(db.String(255), nullable=False)
    store_image = db.Column(db.String(255), nullable=True)
    owner_image = db.Column(db.String(255), nullable=True , default='th.jpg')
    owner_banner = db.Column(db.String(255), nullable=True , default='banner_seller.png')
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    last_login = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=False)  # True = نشط، False = غير نشط
    is_seller = db.Column(db.Boolean, default=False)  # True = بائع False = غير بائع
    rating = db.Column(db.Float, nullable=True, default=1.0)
    comment = db.Column(db.String(255), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)  # عنوان الشارع

    
    # العلاقة مع المنتجات
    products = db.relationship('Product', backref='associated_seller', cascade="all, delete-orphan", passive_deletes=True)
    subcategories = db.relationship('Subcategory', backref='seller', cascade='all, delete-orphan', passive_deletes=True)

    
    def update_last_login(self):
        self.last_login = datetime.now()

    def get_id(self):
        return self.seller_id  # إرجاع معرف البائع فقط

    def __repr__(self):
        return f"Seller('{self.seller_id}', '{self.seller_name}', '{self.store_name}', '{self.store_category}', '{self.governorate}', '{self.city}', '{self.village}', '{self.store_image}', '{self.owner_image}', '{self.registration_date}', '{self.last_login}', '{self.status}', '{self.is_seller}', '{self.rating}')"


class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False, unique=True)
    image_category = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)  # حالة تفعيل القسم


    def __repr__(self):
        return f"Category('{self.category_id}', '{self.category_name}', '{self.image_category}', '{self.is_active}')"


class Subcategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # حالة تفعيل القسم
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id', ondelete='CASCADE'), nullable=True)

    def __repr__(self):
        return f"Subcategory('{self.id}', '{self.name}', '{self.image}', '{self.is_active}', '{self.seller_id}')"



class Typesofservices(db.Model):
    __tablename__ = 'typesofservices'
    
    Types_of_services_id = db.Column(db.Integer, primary_key=True)
    Types_of_services_name = db.Column(db.String(255), nullable=False, unique=True)
    image_Types_of_services = db.Column(db.String(255))

    def __repr__(self):
        return f"Types_of_services('{self.Types_of_services_id}', '{self.Types_of_services_name}', '{self.image_Types_of_services}')"


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id', ondelete="CASCADE"), nullable=True)  # الربط بالبائع
    product_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    product_category = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=True)  # True = نشط، False = غير نشط
    rating = db.Column(db.Float, nullable=True)
    discount = db.Column(db.Float, nullable=True, default=0.0)  # نسبة الخصم أو القيمة
    net_profit = db.Column(db.Float, nullable=True)  # صافي الربح
    total_after_commission = db.Column(db.Float, nullable=True)  # إجمالي المبلغ بعد العمولة

    # أعمدة الصور
    image1 = db.Column(db.String(255))
    image2 = db.Column(db.String(255))
    image3 = db.Column(db.String(255))
    image4 = db.Column(db.String(255))
    image5 = db.Column(db.String(255))

    # العلاقة مع جدول Seller
    seller = db.relationship('Seller', backref='product_association', lazy=True, passive_deletes=True)
    # العلاقة مع جدول OfferProduct
    offers = db.relationship('OfferProduct', backref='product', cascade='all, delete-orphan', lazy=True)


    def __repr__(self):
        return f"Product('{self.product_id}','{self.net_profit}','{self.total_after_commission}', '{self.product_name}', '{self.status}', '{self.rating}', '{self.description}', '{self.price}', '{self.image1}', '{self.image2}', '{self.image3}', '{self.image4}', '{self.image5}', '{self.category_id}', '{self.stock_quantity}', '{self.seller_id}')"
    def has_active_offer(self):
        today = date.today()
        for offer_product in self.offers:
            offer = offer_product.offer
            if (
                offer.status == True and
                offer.approval_status == 'approved' and
                offer.start_date <= today and
                offer.end_date >= today
            ):
                return True  # المنتج موجود داخل عرض نشط
        return False  # المنتج غير مرتبط بأي عرض نشط

# نموذج لجدول العروض
class Offer(db.Model):
    __tablename__ = 'offers'

    offer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(255), nullable=False)
    typename = db.Column(db.String(50), nullable=False)  # خصم نسبي أو خصم ثابت
    discount_value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    approval_status = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Boolean, default=False)  # True = نشط، False = غير نشط


    # العلاقة مع OfferProduct
    products = db.relationship('OfferProduct', backref='offer', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f"Offer('{self.offer_id}', '{self.name}', '{self.type}', '{self.discount_value}', '{self.start_date}', '{self.end_date}', '{self.description}', '{self.image}')"


#نموذج لجدول الربط بين المنتجات و العروض
class OfferProduct(db.Model):
    __tablename__ = 'offer_products'

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offers.offer_id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"OfferProduct('{self.id}', '{self.offer_id}', '{self.product_id}')"

# نموذج لجدول الفواتير
class Invoice(db.Model):
    __tablename__ = 'invoices'
    invoice_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Invoice('{self.invoice_id}', '{self.order_id}', '{self.invoice_date}', '{self.total_amount}')"




class Services(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(255), nullable=False)
    typesofservices_id = db.Column(db.Integer, db.ForeignKey('typesofservices.Types_of_services_id'), nullable=True)
    typesofservices = db.Column(db.String(255), nullable=True)
    provider_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    service_image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Boolean, default=True)  # True = نشط، False = غير نشط
    rating = db.Column(db.Float, nullable=True)
    created_datetime = db.Column(db.DateTime, default=datetime.now)



    def __repr__(self):
        return f"Services('{self.id}','{self.service_name}','{self.provider_name}','{self.phone}','{self.address}','{self.description}','{self.price}','{self.experience_years}','{self.service_image}','{self.status}','{self.rating}','{self.created_datetime}')"





class Notification(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id', ondelete="CASCADE"), nullable=True)  # الربط بجدول المستخدمين
    title = db.Column(db.String(255), nullable=False)  # عنوان الإشعار
    message = db.Column(db.Text, nullable=False)  # نص الإشعار
    created_at = db.Column(db.DateTime, default=datetime.now)  # وقت الإرسال
    read_status = db.Column(db.Boolean, default=False)  # حالة القراءة
    action_url = db.Column(db.String(255), nullable=False)  # عنوان الإشعار


    seller = db.relationship('Seller', backref='notifications_list', passive_deletes=True)  # تغيير اسم العلاقة الخلفية

    @property
    def formatted_created_at(self):
        """خاصية لإرجاع الوقت بالتنسيق العربي المطلوب."""
        return format_datetime(self.created_at, "h:mm a d MMMM y", locale="ar")

    def __repr__(self):
        return f"Notification('{self.notification_id}', '{self.seller_id}','{self.title}','{self.message}','{self.created_at}','{self.read_status}','{self.seller}')"




class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)  # عدد المنتجات
    added_at = db.Column(db.DateTime, default=datetime.now)
    old_price = db.Column(db.Float, nullable=True)  # السعر قبل الخصم
    price = db.Column(db.Float, nullable=True)  # السعر بعد الخصم
    new_offer_price = db.Column(db.Float, nullable=True)  # السعر بعد الخصم الجديد
    total_price = db.Column(db.Float, nullable=True)  # السعر النهائي


    # العلاقات
    seller = db.relationship('Seller', backref=db.backref('cart_items', cascade='all, delete-orphan'))
    product = db.relationship('Product', backref=db.backref('cart_association', cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<Cart(cart_id={self.cart_id}, seller_id={self.seller_id}, product_id={self.product_id}, quantity={self.quantity}, added_at={self.added_at}, latitude={self.latitude}, longitude={self.longitude})>"



# نموذج لجدول الطلبات
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    order_status = db.Column(db.String(50), default='pending')  # حالة الطلب
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.Boolean, default=False)  # حالة الدفع
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    payment_price = db.Column(db.Float, nullable=False)  
    payment_phone = db.Column(db.String(50), nullable=False)

    # العلاقات
    details = db.relationship('OrderDetail', backref='order', cascade='all, delete-orphan')

    

    def __repr__(self):
        return f"Order('{self.order_id}', '{self.order_date}','{self.payment_price}','{self.payment_phone}', '{self.customer_name}', '{self.order_status}', '{self.total_amount}', '{self.payment_method}', '{self.phone}', '{self.latitude}', '{self.longitude}')"


# نموذج لجدول تفاصيل الطلبات
class OrderDetail(db.Model):
    __tablename__ = 'order_details'

    detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)  # معرف المنتج
    quantity = db.Column(db.Integer, nullable=False)  # الكمية
    price = db.Column(db.Numeric(10, 2), nullable=True)         # السعر
    product_name = db.Column(db.String(255), nullable=True)  # اسم المنتج
    seller_name = db.Column(db.String(255), nullable=True)   # اسم البائع
    store_name = db.Column(db.String(255), nullable=True)    # اسم المتجر
    customer_name = db.Column(db.String(255), nullable=True) # اسم العميل
    customer_address = db.Column(db.String(255), nullable=True) # عنوان العميل
    customer_phone = db.Column(db.String(20), nullable=True)    # رقم هاتف العميل
    price_comition = db.Column(db.Numeric(10, 2), nullable=True) # السعر بعد العمولة

    def __repr__(self):
        return f"<OrderDetail(detail_id={self.detail_id}, order_id={self.order_id}, product_name={self.product_name}, seller_name={self.seller_name}, store_name={self.store_name}, customer_name={self.customer_name}, customer_address={self.customer_address}, customer_phone={self.customer_phone},price_comition={self.price_comition}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})>"



class Banner(db.Model):
    __tablename__ = 'banners'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # عنوان البنر
    typebanner = db.Column(db.String(255), nullable=False)  # نوع البنر
    image = db.Column(db.String(255), nullable=False)  # مسار صورة البنر
    link = db.Column(db.String(255), nullable=True)  # الرابط عند الضغط على البنر
    is_active = db.Column(db.Boolean, default=False)  # حالة تفعيل البنر


class SellerReview(db.Model):
    __tablename__ = 'seller_reviews'
    
    review_id = db.Column(db.Integer, primary_key=True, nullable=False)  # المعرف الفريد للتقييم
    rating = db.Column(db.Float, nullable=False)  # التقييم
    comment = db.Column(db.String(255), nullable=True)  # التعليق
    customer_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id'), nullable=False)  # معرف العميل
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id'), nullable=False)  # معرف البائع
    
    # العلاقات
    customer = db.relationship('Seller', foreign_keys=[customer_id], backref='customer_reviews')  # ارتباط بالعميل
    seller = db.relationship('Seller', foreign_keys=[seller_id], backref='seller_reviews')  # ارتباط بالبائع
    
    def __repr__(self):
        return f"SellerReview('{self.review_id}', '{self.rating}', '{self.comment}', '{self.customer_id}', '{self.seller_id}')"


class FavoriteProduct(db.Model):
    __tablename__ = 'favorite_products'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.seller_id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id', ondelete="CASCADE"), nullable=False)
    added_date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # العلاقات
    seller = db.relationship('Seller', backref='favorite_products', lazy=True, passive_deletes=True)
    product = db.relationship('Product', backref='favorite_products', lazy=True, passive_deletes=True)

    def __repr__(self):
        return f"FavoriteProduct('{self.id}', '{self.seller_id}', '{self.product_id}', '{self.added_date}')"
