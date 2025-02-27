import re
from babel.dates import format_datetime
from datetime import date, datetime
from flask_jwt_extended import create_access_token
from flask_login import current_user, login_required, login_user, logout_user 
from babel.dates import format_datetime
from sqlalchemy.exc import SQLAlchemyError
import os
import qrcode
from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import extract, func, text
from sqlalchemy.orm import joinedload
from appobourcity.forms import BannerForm, CategoryForm,  LoginForm, NotificationForm, OfferForm, ProductForm, SellerForm, ServiceForm, SubcategoryForm, Types_of_servicesForm, UserForm
from appobourcity import app, db, bcrypt ,login_manager
from werkzeug.utils import secure_filename
from appobourcity.models import Banner, Cart, FavoriteProduct, Notification, Offer, OfferProduct, Product, Seller, Category,  Invoice, Order, OrderDetail, SellerReview, Services, Subcategory,Typesofservices
import sqlite3 as sql
from werkzeug.security import generate_password_hash,check_password_hash
from sklearn.cluster import KMeans
import pandas as pd
from flask_limiter import Limiter

limiter = Limiter(app)




@login_manager.user_loader
def load_seller(user_id):
    """تحميل مستخدم البائع بناءً على معرف المستخدم."""
    return Seller.query.get(int(user_id))

# دالة للتحقق من نوع الملف
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

#====================================== start ======================================================================
#====================================== start ======================================================================
#====================================== start ======================================================================
#====================================== start ======================================================================
#====================================== start ======================================================================

@app.route('/loginadmin')
def admin():
    return render_template('admin.html')

#======================================   banner ===================================================================

@app.route('/banner', methods=['GET', 'POST'])
def banner():
    form = BannerForm()
    if form.validate_on_submit():
        # الحصول على البيانات من النموذج
        title = form.title.data
        typebanner = form.typebanner.data
        link = form.link.data
        is_active = form.is_active.data

        # التحقق من رفع الصور بشكل منفصل
        image_file = request.files.get('image')  # اسم الحقل "image" مطابق لحقل الصورة في النموذج
        image_filename = None

        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_filepath = os.path.join(app.config['BANNERS_FOLDER'], image_filename)
            image_file.save(image_filepath)

        # التحقق من رفع الصورة بنجاح
        if not image_filename:
            flash('الرجاء تحميل صورة البنر.', 'error')
            return redirect(url_for('banner'))

        # إضافة البنر إلى قاعدة البيانات
        new_banner = Banner(
            title=title,
            typebanner=typebanner,
            image=image_filename,  # فقط اسم الملف
            link=link,
            is_active=is_active
        )
        db.session.add(new_banner)
        db.session.commit()

        flash('تمت إضافة البنر بنجاح!', 'success')
        return redirect(url_for('banner'))
    

    banners = Banner.query.all()

    return render_template('banner.html', form=form , banners= banners)

#======================================  update banner 


@app.route('/update-banner-is_active', methods=['POST'])
@login_required
def update_banner_is_active():
    data = request.get_json()
    banner_id = data.get('banner_id')  # تأكد من استخدام 'banner_id' بدلاً من 'product_id'
    is_active = data.get('is_active')

    # تحقق من وجود البنر
    banner = Banner.query.get(banner_id)
    if not banner:
        return jsonify({'success': False, 'error': 'Banner not found'}), 404

    # تحديث الحالة
    try:
        banner.is_active = is_active
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500



#================================ === delete banner  




@app.route('/delete_banner/<int:id>', methods=['GET'])
def delete_banner(id):
    # العثور على التخصص بناءً على ID
    banners = Banner.query.get_or_404(id)
    
    # حذف التخصص
    db.session.delete(banners)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف البانر بنجاح!', 'success')
    
    return redirect(url_for('banner'))  # إعادة التوجيه إلى صفحة البانر

#======================================   category ===================================================================
#======================================   category ===================================================================


@app.route('/category', methods=['GET', 'POST'])
def category():
    form = CategoryForm()

    if form.validate_on_submit():
        image_category_file = request.files['image_category']

        image_category_filename = None

        # تحقق من رفع صورة صاحب المتجر
        if image_category_file and image_category_file.filename != '':
            image_category_filename = secure_filename(image_category_file.filename)
            image_category_filepath = os.path.join(app.config['CATEGORY_FOLDER'], image_category_filename)
            image_category_file.save(image_category_filepath)


        category_name = form.category_name.data

        # تحقق من وجود القسم في قاعدة البيانات
        existing_category = Category.query.filter_by(category_name=category_name).first()
        if existing_category:
            # عرض رسالة خطأ
            flash("هذا القسم موجود بالفعل . يرجى إدخال قسم مختلف.", "error")
            con = sql.connect("instance/database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM categories")
            category = cur.fetchall()
            return render_template('category.html', form=form , category=category)
        category_name = form.category_name.data
        new_category = Category(category_name=category_name,
                                image_category=image_category_filename)
        db.session.add(new_category)
        db.session.commit()
        flash('تم إضافة القسم بنجاح!', 'success')

        return redirect(url_for('category'))  # بعد إضافة التخصص يعيد التوجيه إلى نفس الصفحة
    
    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM categories")
    category = cur.fetchall()

    return render_template('category.html', form=form , category=category)




#=====================================================  delete category 


@app.route('/delete_category/<int:category_id>', methods=['GET'])
def delete_category(category_id):
    # العثور على التخصص بناءً على ID
    category = Category.query.get_or_404(category_id)
    
    # حذف التخصص
    db.session.delete(category)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف القسم بنجاح!', 'success')
    
    return redirect(url_for('category'))  # إعادة التوجيه إلى صفحة الفئات



#================================  dashboard admin =============================================
#================================  dashboard admin =============================================

@app.route('/dashboard')
def dashboard():

    #=============================     تحليل البيانات   ============================

    
    #=============================     مبيعات المنتجات  ============================

    # حساب المبيعات لكل شهر للطلبات المدفوعة
    sales_data = db.session.query(
        extract('month', Order.order_date).label('month'),
        func.sum(OrderDetail.price * OrderDetail.quantity).label('total_sales')
    ).join(OrderDetail, Order.order_id == OrderDetail.order_id) \
     .filter(Order.payment_status == True) \
     .group_by(extract('month', Order.order_date)) \
     .order_by(extract('month', Order.order_date)) \
     .all()

    # تحويل البيانات إلى قوائم مناسبة للرسم
    months = [int(row.month) for row in sales_data]
    sales = [float(row.total_sales) for row in sales_data]

    # أسماء الأشهر
    month_names = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    
    # تحويل الأشهر من أرقام إلى أسماء
    sales_months_labels = [month_names[month - 1] for month in months]

    #=============================     عدد المستخدمين و البائعين ============================


    # الحصول على عدد المستخدمين في كل شهر
    monthly_users = db.session.query(
        extract('month', Seller.registration_date).label('month'),
        func.count(Seller.seller_id).label('user_count')
    ).group_by(
        extract('month', Seller.registration_date)
    ).order_by('month').all()

    # الحصول على عدد البائعين في كل شهر
    monthly_sellers = db.session.query(
        extract('month', Seller.registration_date).label('month'),
        func.count(Seller.seller_id).label('seller_count')  # هنا تم تغيير 'user_count' إلى 'seller_count'
    ).group_by(
        extract('month', Seller.registration_date)
    ).filter(Seller.is_seller == 1).group_by('month').order_by('month').all()

    # تحويل البيانات إلى تنسيق مناسب للرسم البياني
    months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    users_data = [0] * 12  # تهيئة بيانات المستخدمين لجميع الأشهر
    sellers_data = [0] * 12  # تهيئة بيانات البائعين لجميع الأشهر

    for entry in monthly_users:
        month_index = int(entry.month) - 1  # تحويل الشهر إلى فهرس (0-based)
        users_data[month_index] = entry.user_count

    for entry in monthly_sellers:
        month_index = int(entry.month) - 1  # تحويل الشهر إلى فهرس (0-based)
        sellers_data[month_index] = entry.seller_count  # استخدام seller_count هنا بدلاً من user_count

    #=============================     نسبة المبيعات حسب الفئة============================


    # استرجاع أسماء الفئات المستخدمة من قبل البائعين فقط
    categories_used_by_sellers = db.session.query(Seller.store_category).filter(
        Seller.store_category.isnot(None)  # استثناء القيم الفارغة
    ).distinct().all()

    # تحويل النتائج إلى قائمة بسيطة
    category_names = [category[0] for category in categories_used_by_sellers]



    # استرجاع مبيعات الفئات المستخدمة من قبل البائعين
    if category_names:  # تأكد أن قائمة الفئات ليست فارغة
        category_sales_data = db.session.query(
        Seller.store_category,
        func.sum(OrderDetail.price_comition * OrderDetail.quantity).label('total_sales')
    ).select_from(Seller).join(
        Product, Seller.seller_id == Product.seller_id
    ).join(
        OrderDetail, OrderDetail.product_id == Product.product_id
    ).join(
        Order, Order.order_id == OrderDetail.order_id
    ).filter(
        Order.payment_status == 1
    ).filter(
        Seller.store_category.isnot(None)  # استبعاد القيم الفارغة
    ).group_by(
        Seller.store_category
    ).all()

        # تحضير البيانات لعرضها في الرسم البياني
        categories = [category[0] for category in category_sales_data]
        category_sales = [float(category[1]) for category in category_sales_data]
    else:
        categories = []
        category_sales = []

    #=============================     نمو المبيعات  ===========================
        # استعلام لجلب مبيعات كل شهر
    monthly_sales_data = db.session.query(
        func.strftime('%m', Order.order_date).label('month'),  # استخدم strftime لاستخراج الشهر
        func.sum(OrderDetail.price_comition * OrderDetail.quantity).label('total_sales')
    ).join(OrderDetail, Order.order_id == OrderDetail.order_id) \
     .filter(Order.payment_status == 1) \
     .group_by(func.strftime('%m', Order.order_date)) \
     .order_by(func.strftime('%m', Order.order_date)) \
     .all()

    # تحويل البيانات الشهرية إلى قوائم قابلة للعرض في القالب
    monthly = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
    monthly_sales = [0] * 12  # إنشاء قائمة للمبيعات على مدار 12 شهرًا

    # تعبئة بيانات المبيعات بالشهر المناسب
    for month, total_sales in monthly_sales_data:
        # تحويل الشهر من %m إلى الرقم المناسب في قائمة "monthly"
        month_index = int(month) - 1
        monthly_sales[month_index] = total_sales

#==================================    نهاية التحليل     =============================================
#==================================    نهاية التحليل     =============================================
#==================================    نهاية التحليل     =============================================


    # البيانات الأخرى
    sellers_count = Seller.query.filter_by(is_seller=1).count()
    customers_count =Seller.query.filter_by(is_seller=0).count()
    user = Seller.query.count()
    order = Order.query.filter(Order.payment_status != 0).count()
    products_count = Product.query.count()
    unread_offer = Offer.query.filter(Offer.approval_status == "pending").count()
    
    seller = (
        db.session.query(Seller)
        .filter(Seller.is_seller == 1)  # البائعين المفعلين فقط وغير مفعلين
        .order_by(Seller.registration_date.desc())  # ترتيب حسب تاريخ التسجيل (الأحدث أولاً)
        .limit(10)  # تحديد آخر 10 بائعين
        .all()  # جلب البيانات
    )  
    # حساب مجموع عمود payment_price
    # حساب مجموع قيمة الدفع للطلبات المدفوعة فقط
    total_payment_price = db.session.query(func.sum(Order.payment_price)) \
        .filter(Order.payment_status != 0) \
        .scalar() or 0  # إذا لم تكن هناك نتائج، يتم إرجاع 0

    # ضرب النتيجة في 0.02
    formatted_result = total_payment_price * 0.05

    # تنسيق النتيجة باستخدام f-string
    total_profit = f"{formatted_result:.2f}"



    # استعلام لجلب آخر عشر طلبات تم إنشاؤها بشرط أن لا تكون الحالة 'approved'
    orders = Order.query.filter(Order.order_status != 'approved') \
        .order_by(Order.order_date.desc()) \
        .limit(10).all()
    
    # تحديث الحقل payment_price ليكون مساويًا لقيمة total_amount عندما يكون payment_status = 1
    db.session.query(Order).filter(Order.payment_status == 1).update({Order.payment_price: Order.total_amount})
    
    # حفظ التغييرات في قاعدة البيانات
    db.session.commit()
    




    return render_template(
        'dashboard.html',
        sellers_count=sellers_count,
        products_count=products_count,
        user=user,
        users_data=users_data,
        sellers_data=sellers_data,
        months=months,
        seller=seller,
        customers_count=customers_count,
        unread_offer=unread_offer,
        order=order,
        total_profit=total_profit,
        sales_months_labels=sales_months_labels,
        sales=sales,
        orders=orders,
        categories=categories,
        category_sales=category_sales,
        monthly=monthly,
        monthly_sales=monthly_sales,


    )
#==========================================    notifications admin   ================================
#==========================================    notifications admin   ================================
@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    form = NotificationForm()

    if form.validate_on_submit():
        send_to = request.form.get('send_to')  # تحديد الإرسال إلى الجميع أو فردي
        title = form.title.data
        message = form.message.data
        action_url = form.action_url.data

        if send_to == 'all':
            # إنشاء قائمة بمعرفات البائعين
            seller_ids = [seller.seller_id for seller in Seller.query.all()]
            if not seller_ids:
                flash("لا يوجد بائعون لإرسال الإشعار.", "error")
                return redirect(url_for('notifications'))

            # إنشاء إشعار لكل بائع في القائمة
            for seller_id in seller_ids:
                notification = Notification(
                    seller_id=seller_id,
                    title=title,
                    message=message,
                    action_url=action_url,
                )
                db.session.add(notification)
            db.session.commit()
            flash('تم إرسال الإشعار إلى جميع المستخدمين بنجاح!', 'success')

        elif send_to == 'single':
            seller_email = form.seller_email.data
            # البحث عن البائع بالبريد الإلكتروني
            seller = Seller.query.filter_by(email=seller_email).first()
            if not seller:
                flash("البائع غير موجود. تأكد من البريد الإلكتروني.", "error")
                return redirect(url_for('notifications'))

            # إنشاء الإشعار للبائع الفردي
            notification = Notification(
                seller_id=seller.seller_id,
                title=title,
                message=message,
                action_url=action_url,
            )
            db.session.add(notification)
            db.session.commit()
            flash('تم إرسال الإشعار بنجاح!', 'success')

        return redirect(url_for('notifications'))

    # جلب جميع الإشعارات للعرض
    notifications = db.session.query(Notification, Seller).join(Seller).all()

    return render_template('notifications.html', form=form, notifications=notifications)


#=======================================  delete notifications admin

@app.route('/delete_notification/<int:notification_id>', methods=['GET'])
def delete_notification(notification_id):
    # البحث عن الإشعار المراد حذفه
    notification = Notification.query.get(notification_id)
    
    if notification is None:
        flash("الإشعار غير موجود!", "error")
        return redirect(url_for('notifications'))
    
    # حذف الإشعار
    db.session.delete(notification)
    db.session.commit()
    
    flash("تم حذف الإشعار بنجاح!", "success")
    return redirect(url_for('notifications'))

#===========================================   offers admin  =============================================
#===========================================   offers admin  =============================================

@app.route('/offers_admin')
def offers_admin():

    offers = db.session.query(
        Offer, 
        Seller.seller_name.label('seller_name'),  # استخدام اسم الحقل الصحيح هنا
        Seller.store_name.label('store_name')  # إضافة حقل اسم المتجر هنا
    ).join(
        OfferProduct, OfferProduct.offer_id == Offer.offer_id
    ).join(
        Product, Product.product_id == OfferProduct.product_id
    ).join(
        Seller, Seller.seller_id == Product.seller_id
    ).all()

    return render_template('offers.html' , offers=offers)

#===============================================  update offer admin

@app.route('/update-offer-status', methods=['POST'])
@login_required
def update_offer_status():
    data = request.get_json()  # استقبال البيانات المرسلة عبر الـ request
    offer_id = data.get('offer_id')  # المعرف الخاص بالعرض
    status = data.get('status')  # الحالة الجديدة (True/False)

    # تحقق من وجود العرض في قاعدة البيانات
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'success': False, 'error': 'Offer not found'}), 404

    try:
        # تحديث حالة العرض
        offer.status = status  # تحديث الحقل في قاعدة البيانات
        db.session.commit()  # حفظ التغييرات في قاعدة البيانات
        return jsonify({'success': True}), 200  # إرجاع استجابة ناجحة
    except Exception as e:
        db.session.rollback()  # في حال حدوث خطأ نقوم بإرجاع التغيير
        return jsonify({'success': False, 'error': str(e)}), 500  # إرجاع استجابة فاشلة مع الخطأ
    

#===============================================  update offer status admin



@app.route('/update-approval-status', methods=['POST'])
@login_required
def update_approval_status():
    data = request.get_json()  # استقبال البيانات المرسلة عبر الـ request
    offer_id = data.get('offer_id')  # المعرف الخاص بالعرض
    approval_status = data.get('approval_status')  # حالة الموافقة الجديدة (pending, approved, rejected)

    # تحقق من وجود العرض في قاعدة البيانات
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'success': False, 'error': 'Offer not found'}), 404

    try:
        # تحديث حالة الموافقة
        offer.approval_status = approval_status  # تحديث الحقل في قاعدة البيانات
        db.session.commit()  # حفظ التغييرات في قاعدة البيانات
        return jsonify({'success': True}), 200  # إرجاع استجابة ناجحة
    except Exception as e:
        db.session.rollback()  # في حال حدوث خطأ نقوم بإرجاع التغيير
        return jsonify({'success': False, 'error': str(e)}), 500  # إرجاع استجابة فاشلة مع الخطأ
    

#===============================================  update offer notes admin



@app.route('/update-offer', methods=['POST'])
@login_required
def update_offer():
    data = request.get_json()  # استلام البيانات
    offer_id = data.get('offer_id')  # استخراج معرف العرض
    notes = data.get('notes')  # استخراج الملاحظات

    # التحقق من وجود العرض
    offer = Offer.query.get(offer_id)
    if not offer:
        return jsonify({'success': False, 'error': 'Offer not found'}), 404

    try:
        # تحديث الحقول
        offer.notes = notes
        db.session.commit()  # حفظ التغييرات
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()  # التراجع في حالة حدوث خطأ
        return jsonify({'success': False, 'error': str(e)}), 500
    

#===============================================  delete offer admin



@app.route('/delete_offer_admin/<int:offer_id>', methods=['GET'])
def delete_offer_admin(offer_id):
    # العثور على التخصص بناءً على ID
    offer = Offer.query.get_or_404(offer_id)
    
    # حذف التخصص
    db.session.delete(offer)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف العرض بنجاح!', 'success')
    
    return redirect(url_for('offers_admin'))  # إعادة التوجيه إلى صفحة الفئات


#================================================   order details for admin  ===========================================
#================================================   order details for admin  ===========================================

@app.route('/order_details_admin/<int:order_id>')
def order_details_admin(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return redirect(url_for('dashboard'))
    
    # إعداد QR Code
    page_url = f"http://127.0.0.1:5000/order_details_admin/{order_id}"
    qr_folder = app.config['UPLOAD_FOLDER_QRCODE']
    qr_filename = f'qrcode_order_{order_id}.png'
    qr_filepath = os.path.join(qr_folder, qr_filename)
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)
    if not os.path.exists(qr_filepath):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(page_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(qr_filepath)

    # جلب تفاصيل الطلب
    result = db.session.query(Order, OrderDetail)\
        .join(OrderDetail, Order.order_id == OrderDetail.order_id)\
        .filter(Order.order_id == order_id).all()

    order_details = []
    total_price = 0
    total_profit = 0
    seller_names = set()
    sellers = {}

    for order_data, detail in result:
        # جمع أسماء البائعين من تفاصيل الطلب
        if detail.seller_name:
            seller_names.add(detail.seller_name)

        # حساب السعر النهائي والربح
        final_price = detail.price_comition * detail.quantity
        total_price += final_price
        profit = final_price - (detail.price * detail.quantity)
        total_profit += profit

        detail.final_price = final_price
        detail.total_profit = profit
        order_details.append(detail)

    # جلب بيانات البائعين بناءً على seller_name
    if seller_names:
        seller_records = Seller.query.filter(Seller.seller_name.in_(seller_names)).all()
        for seller in seller_records:
            sellers[seller.seller_name] = {
                'seller_name': seller.seller_name,
                'phone': seller.phone,
                'address': f"{seller.governorate}, {seller.city}, {seller.village}, {seller.street_address or ''}",
                'store_name': seller.store_name
            }

    return render_template(
    'order_details.html',
    order=order,
    order_details=order_details,
    sellers=list(sellers.values()),  # تحويل القيم إلى قائمة
    total_price=total_price,
    total_profit=total_profit
    )



#================================================   order  =====================================================
#================================================   order  =====================================================



@app.route('/Orders')
def Orders():
    orders = Order.query.all()

    # تحديث الحقل payment_price ليكون مساويًا لقيمة total_amount عندما يكون payment_status = 1
    db.session.query(Order).filter(Order.payment_status == 1).update({Order.payment_price: Order.total_amount})
    
    # حفظ التغييرات في قاعدة البيانات
    db.session.commit()


    return render_template('Orders.html' , orders=orders)

#================================================   products admin   ==================================================
#================================================   products admin   ==================================================


@app.route('/products')
def products():
    products = Product.query.all()

    return render_template('products.html', products=products)




@app.route('/check-product-offers')
def check_product_offers():
    product = Product.query.get_or_404()
    if product.has_active_offer():
        return f"المنتج '{product.product_name}' موجود داخل عرض نشط."
    else:
        return f"المنتج '{product.product_name}' غير مرتبط بأي عرض نشط."

#============================================  delete products admin

@app.route('/delete_product_admin/<int:product_id>', methods=['GET'])
def delete_product_admin(product_id):
    # العثور على التخصص بناءً على ID
    product = Product.query.get_or_404(product_id)
    
    # حذف التخصص
    db.session.delete(product)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف المنتج بنجاح!', 'success')
    
    return redirect(url_for('products'))  # إعادة التوجيه إلى صفحة الفئات








#================================================   seller   ====================================================
#================================================   seller   ====================================================


# المسار لإضافة التاجر وعرض جميع التجار
@app.route('/sellers', methods=['GET', 'POST'])
def sellers():
    form = SellerForm()

    if form.validate_on_submit():
        email = form.email.data

        # تحقق من وجود البريد الإلكتروني في قاعدة البيانات
        existing_seller = Seller.query.filter_by(email=email).first()
        if existing_seller:
            # عرض رسالة خطأ
            flash("هذا البريد الإلكتروني مسجل بالفعل . يرجى إدخال بريد إلكتروني مختلف.", "error")
            con = sql.connect("instance/database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM sellers")
            seller = cur.fetchall()
            return render_template('sellers.html', form=form , seller=seller)

        # التحقق من رفع الصور بشكل منفصل
        owner_image_file = request.files['owner_image']
        store_image_file = request.files['store_image']

        owner_image_filename = None
        store_image_filename = None

        # تحقق من رفع صورة صاحب المتجر
        if owner_image_file and owner_image_file.filename != '':
            owner_image_filename = secure_filename(owner_image_file.filename)
            owner_image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], owner_image_filename)
            owner_image_file.save(owner_image_filepath)

        # تحقق من رفع صورة المتجر
        if store_image_file and store_image_file.filename != '':
            store_image_filename = secure_filename(store_image_file.filename)
            store_image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], store_image_filename)
            store_image_file.save(store_image_filepath)


        
        # إنشاء كائن التاجر
        seller = Seller(
            seller_name=form.seller_name.data,
            store_name=form.store_name.data,
            store_category=form.store_category.data,
            email=email,
            phone=form.phone.data,
            address=form.address.data,
            store_image=store_image_filename,
            owner_image=owner_image_filename,
            password=form.password.data,
        )

        # إضافة التاجر إلى قاعدة البيانات
        db.session.add(seller)
        db.session.commit()
        flash('تم تسجيل البائع بنجاح!', 'success')
        # إعادة التوجيه إلى الصفحة نفسها أو إلى صفحة أخرى بعد حفظ البيانات
        return redirect(url_for('sellers'))

    # استرجاع جميع التجار من قاعدة البيانات (إذا كنت بحاجة إلى عرضهم)
    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM sellers")
    seller = cur.fetchall()

    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM categories")
    category = cur.fetchall()

    formatted_sellers = []
    for seller in seller:
        seller_dict = dict(seller)  # تحويل الصف إلى قاموس
        registration_date = seller_dict["registration_date"]
        if registration_date:  # التحقق من وجود التاريخ
            # تحويل النص إلى كائن datetime
            dt = datetime.strptime(registration_date, "%Y-%m-%d %H:%M:%S.%f")
            # تنسيق التاريخ والوقت باللغة العربية
            formatted_date = format_datetime(dt, "h:mm a d MMMM y", locale="ar")
            seller_dict["formatted_registration_date"] = formatted_date  # إضافة التاريخ بالتنسيق الجديد
        formatted_sellers.append(seller_dict)


    return render_template('sellers.html', form=form, seller=formatted_sellers, category=category)

#======================================   toggle seller status 


@app.route('/toggle_seller_status', methods=['POST'])
def toggle_seller_status():
    data = request.get_json()
    seller_id = data.get('seller_id')
    new_status = data.get('status')

    # جلب البائع من قاعدة البيانات
    seller = Seller.query.get(seller_id)
    if seller:
        # تغيير حالة البائع
        seller.status = new_status
        db.session.commit()
        return jsonify(success=True)  # الرد بالنجاح
    return jsonify(success=False)  # الرد بالفشل إذا لم يكن البائع موجودًا

#======================================   toggle seller is seller 



@app.route('/toggle_seller_is_seller', methods=['POST'])
def toggle_seller_is_seller():
    data = request.get_json()
    seller_id = data.get('seller_id')
    is_seller = data.get('is_seller')

    # جلب البائع من قاعدة البيانات
    seller = Seller.query.get(seller_id)
    if seller:
        # تغيير حالة البائع
        seller.is_seller = is_seller
        db.session.commit()
        return jsonify(success=True)  # الرد بالنجاح
    return jsonify(success=False)  # الرد بالفشل إذا لم يكن البائع موجودًا


#==========================================   update seller 


@app.route('/update_seller', methods=['POST'])
def update_seller():
    try:
        seller_id = request.form['seller_id']
        seller = Seller.query.get_or_404(seller_id)

        # تحديث البيانات
        seller.seller_name = request.form['seller_name']
        seller.store_name = request.form['store_name']
        seller.store_category = request.form['store_category']
        seller.phone = request.form['phone']
        seller.address = request.form['address']

        db.session.commit()
        flash('تم تحديث بيانات البائع بنجاح!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تحديث بيانات البائع: {str(e)}', 'error')

    return redirect(url_for('sellers'))


#==========================================  services   ==========================================
#==========================================  services   ==========================================




@app.route('/services', methods=['GET', 'POST'])
def services():
    form = ServiceForm()

    if form.validate_on_submit():
        # التحقق من رفع الصور بشكل منفصل
        service_image_file = request.files['service_image']

        service_image_filename = None

        # تحقق من رفع صورة صاحب المتجر
        if service_image_file and service_image_file.filename != '':
            service_image_filename = secure_filename(service_image_file.filename)
            service_image_filepath = os.path.join(app.config['SERVICE_FOLDER'], service_image_filename)
            service_image_file.save(service_image_filepath)


        # إضافة الخدمة إلى قاعدة البيانات
        new_service = Services(
            service_name=form.service_name.data,
            provider_name=form.provider_name.data,
            address=form.address.data,
            typesofservices=form.typesofservices.data,
            phone=form.phone.data,
            description=form.description.data,
            price=form.price.data,
            experience_years=form.experience_years.data,
            service_image=service_image_filename,
        )
        db.session.add(new_service)
        db.session.commit()
        
        # عرض رسالة فلاش بعد إضافة الخدمة
        flash('تم إضافة الخدمة بنجاح!', 'success')
        return redirect(url_for('services'))  # إعادة توجيه المستخدم إلى نفس الصفحة لتمكين إضافة أخرى
    

    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM services")
    services = cur.fetchall()


    typesofservices=Typesofservices.query.all()



    return render_template('services.html', form=form , services=services, typesofservices=typesofservices)

#==========================================  toggle services status


@app.route('/toggle_services_status', methods=['POST'])
def toggle_services_status():
    data = request.get_json()  # استلام البيانات من الطلب
    service_id = data.get('service_id')
    status = data.get('status')

    if service_id is not None and status is not None:
        service = Services.query.get(service_id)  # البحث عن الخدمة باستخدام ID
        if service:
            service.status = status  # تحديث حالة الخدمة
            db.session.commit()  # حفظ التغييرات في قاعدة البيانات
            return jsonify({"success": True, "message": "تم تحديث الحالة بنجاح"})
        else:
            return jsonify({"success": False, "message": "الخدمة غير موجودة"}), 404
    return jsonify({"success": False, "message": "بيانات غير صحيحة"}), 400



#============================================  delete services


@app.route('/delete_services/<int:id>', methods=['GET'])
def delete_services(id):
    # العثور على التخصص بناءً على ID
    services = Services.query.get_or_404(id)
    
    # حذف التخصص
    db.session.delete(services)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف الخدمه بنجاح!', 'success')
    
    return redirect(url_for('services'))  # إعادة التوجيه إلى صفحة الفئات



#=======================================   type services   =========================================
#=======================================   type services   =========================================


@app.route('/Types_of_services', methods=['GET', 'POST'])
def Types_of_services():
    form = Types_of_servicesForm()
    if form.validate_on_submit():
        image_Types_of_services_file = request.files['image_Types_of_services']

        image_Types_of_services_filename = None

        # تحقق من رفع صورة صاحب المتجر
        if image_Types_of_services_file and image_Types_of_services_file.filename != '':
            image_Types_of_services_filename = secure_filename(image_Types_of_services_file.filename)
            image_Types_of_services_filepath = os.path.join(app.config['Types_of_services_FOLDER'], image_Types_of_services_filename)
            image_Types_of_services_file.save(image_Types_of_services_filepath)


        Types_of_services_name = form.Types_of_services_name.data

        # تحقق من وجود القسم في قاعدة البيانات
        existing_Types_of_services = Typesofservices.query.filter_by(Types_of_services_name=Types_of_services_name).first()
        if existing_Types_of_services:
            # عرض رسالة خطأ
            flash("هذا القسم موجود بالفعل . يرجى إدخال قسم مختلف.", "error")
            con = sql.connect("instance/database.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM typesofservices")
            Types_of_services = cur.fetchall()
            return render_template('Types_of_services.html', form=form , Types_of_services=Types_of_services)
        Types_of_services_name = form.Types_of_services_name.data
        new_Types_of_services = Typesofservices(Types_of_services_name=Types_of_services_name,
                                image_Types_of_services=image_Types_of_services_filename)
        db.session.add(new_Types_of_services)
        db.session.commit()
        flash('تم إضافة نوع الخدمه بنجاح!', 'success')

        return redirect(url_for('Types_of_services'))  # بعد إضافة التخصص يعيد التوجيه إلى نفس الصفحة
    
    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM typesofservices")
    Types_of_services_data = cur.fetchall()

    return render_template('Types_of_services.html', form=form , Types_of_services=Types_of_services_data)


#=====================================  delete type services

@app.route('/delete_Typesofservices/<int:Types_of_services_id>', methods=['GET'])
def delete_Typesofservices(Types_of_services_id):
    # العثور على التخصص بناءً على ID
    Types_of_services = Typesofservices.query.get_or_404(Types_of_services_id)
    
    # حذف التخصص
    db.session.delete(Types_of_services)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف القسم بنجاح!', 'success')
    
    return redirect(url_for('Types_of_services'))  # إعادة التوجيه إلى صفحة الفئات


#=======================================================  setting  ==========================

@app.route('/settings')
def settings():
    return render_template('settings.html')


#===================================================================================
#===================================================================================
#=============================start_trader =========================================
#=============================start_trader =========================================
#=============================start_trader =========================================
#=============================start_trader =========================================
#===================================================================================
#===================================================================================




#============================= لوحة التحكم ======================================================================


@app.route('/dashboard_trader')
@login_required
def dashboard_trader():

    # التحقق من حالة المستخدم
    if current_user.status == 0:
        flash('تم تعطيل حساب التاجر الخاص بك. يرجى التواصل مع الدعم.', 'error')
        return redirect(url_for('home'))
    

    # جلب البيانات الخاصة بالبائع
    seller_name = current_user.seller_name
    email = current_user.email
    image = current_user.owner_image
    store_image = current_user.store_image
    products_count = Product.query.filter_by(seller_id=current_user.seller_id).count()

    # تحويل تاريخ التسجيل وتاريخ آخر دخول
    registration_date = current_user.registration_date
    formatted_date = format_datetime(registration_date, format='d MMMM yyyy/ h:mm a', locale='ar')
    last_login = current_user.last_login
    formatted_last_login = format_datetime(last_login, format='d MMMM yyyy/ h:mm a', locale='ar') if last_login else formatted_date

    unread_count = Notification.query.filter_by(seller_id=current_user.seller_id, read_status=0).count()
    store_name = current_user.store_name
    products = Product.query.filter_by(seller_id=current_user.seller_id)\
    .order_by(Product.product_id.desc())\
    .limit(5)\
    .all()

    # جلب آخر 10 طلبات للبائع الحالي
    latest_orders = (
        db.session.query(Order, OrderDetail)
        .join(OrderDetail, Order.order_id == OrderDetail.order_id)
        .filter(OrderDetail.seller_name == current_user.seller_name)
        .order_by(Order.order_date.desc())
        .limit(5)
        .all()
    )


    total_revenue = db.session.query(func.sum(OrderDetail.price* OrderDetail.quantity)).join(Product, Product.product_id == OrderDetail.product_id).join(Order, Order.order_id == OrderDetail.order_id).filter(
         OrderDetail.seller_name == seller_name,
         Order.payment_status != 0  # التحقق من حالة الدفع
     ).scalar() or 0  # إذا لم تكن هناك نتائج، يتم إرجاع 0
    

    # حساب عدد الطلبات الخاصة ببائع معين
    seller_order_count = db.session.query(func.count(func.distinct(Order.order_id))) \
        .join(OrderDetail, Order.order_id == OrderDetail.order_id) \
        .filter(OrderDetail.seller_name == current_user.seller_name, Order.payment_status != 0) \
        .scalar() or 0  # إذا لم تكن هناك نتائج، يتم إرجاع 0

        # حساب عدد العملاء بدون تكرار الذين أكملوا الدفع لبائع معين
    unique_customer_count = db.session.query(func.count(func.distinct(Order.customer_name))) \
        .join(OrderDetail, Order.order_id == OrderDetail.order_id) \
        .filter(
            OrderDetail.seller_name == current_user.seller_name,  # تحديد البائع
            Order.payment_status != 0  # التأكد من أن الطلب مدفوع
        ) \
        .scalar() or 0  # إذا لم تكن هناك نتائج، يتم إرجاع 0

    
    return render_template(
        'Trader/dashboard.html',
        seller_name=seller_name,
        email=email,
        image=image,
        store_image=store_image,
        date=formatted_date,
        last_login=formatted_last_login,
        products_count=products_count,
        unread_count=unread_count,
        store_name=store_name,
        products=products,
        total_revenue=total_revenue,
        seller_order_count=seller_order_count,
        unique_customer_count=unique_customer_count,
        latest_orders=latest_orders
    )

#=====================================التعديل علي المعلومات الشخصيه في لوحة التحكم  ============================


@app.route('/update_dashboard_trader', methods=['POST'])
@login_required
def update_dashboard_trader():
    
    # الحصول على البيانات من النموذج
    seller_name = request.form.get('seller_name')
    email = request.form.get('email')
    password = request.form.get('password')
    image = request.files.get('image')  # لتحميل الصورة
    
    # التحقق إذا تم تغيير كلمة المرور
    if password:
        # تشفير كلمة المرور الجديدة إذا تم تغييرها
        password = generate_password_hash(password)
    else:
        # إذا لم يتم تغيير كلمة المرور، الاحتفاظ بالكلمة القديمة
        password = current_user.password

    # تحديث البيانات في قاعدة البيانات
    if image:
        # حفظ الصورة (إذا كانت موجودة)
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
    else:
        image_filename = current_user.owner_image  # الاحتفاظ بالصورة القديمة إذا لم يتم تحميل صورة جديدة

    # تحديث بيانات المستخدم
    current_user.seller_name = seller_name
    current_user.email = email
    current_user.password = password
    current_user.owner_image = image_filename
    
    # حفظ التغييرات
    db.session.commit()

    flash("تم تحديث البيانات بنجاح", "success")
    return redirect(url_for('dashboard_trader'))

#=============================================     العملاء      ================================
@app.route('/customers')
@login_required
def customers():
    seller_id = current_user.seller_id

    # جلب العملاء الذين قاموا بتقييم البائع الحالي
    customers = (
        db.session.query(
            Seller.seller_name.label('customer_name'),  # اسم العميل
            SellerReview.rating.label('rating'),       # التقييم
            SellerReview.comment.label('comment')      # التعليق
        )
        .join(Seller, Seller.seller_id == SellerReview.customer_id)  # الربط بين العملاء والتقييمات
        .filter(SellerReview.seller_id == seller_id)  # تصفية حسب معرف البائع
        .all()
    )

    # عدد الإشعارات غير المقروءة
    unread_count = Notification.query.filter_by(seller_id=seller_id, read_status=0).count()

    return render_template(
        'Trader/customers.html',
        unread_count=unread_count,
        customers=customers
    )


#=============================================     العروض      ================================


@app.route('/offers', methods=['GET', 'POST'])
@login_required
def offers():
    form = OfferForm()

    # تعبئة قائمة المنتجات المرتبطة بالبائع الحالي في الفورم
    products = Product.query.filter_by(seller_id=current_user.seller_id).all()
    form.products.choices = [(p.product_id, p.product_name) for p in products]

    # معرف البائع الحالي
    seller_id = current_user.seller_id        


    if form.validate_on_submit():



        image_file = request.files['image']

        image_filename = None


         #تحقق من رفع الصور
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_filepath = os.path.join(app.config['OFFER_FOLDER'], image_filename)
            image_file.save(image_filepath)



        # إنشاء العرض الجديد
        new_offer = Offer(
            name=form.name.data,
            code=form.code.data,
            typename=form.typename.data,
            discount_value=form.discount_value.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            image=image_filename
        )
        db.session.add(new_offer)
        db.session.commit()

        # ربط المنتجات المختارة بالعروض
        for product_id in form.products.data:
            offer_product = OfferProduct(offer_id=new_offer.offer_id, product_id=product_id)
            db.session.add(offer_product)
        db.session.commit()

        flash('تم إنشاء العرض بنجاح!', 'success')
        return redirect(url_for('offers'))

    # جلب العروض المرتبطة بالبائع الحالي فقط
    offers = (
        db.session.query(Offer)
        .join(OfferProduct, Offer.offer_id == OfferProduct.offer_id)
        .join(Product, Product.product_id == OfferProduct.product_id)
        .filter(Product.seller_id == seller_id)
        .all()
    )

    # حساب عدد الإشعارات غير المقروءة
    unread_count = Notification.query.filter_by(seller_id=seller_id, read_status=0).count()

    return render_template('Trader/offers.html', form=form, offers=offers, unread_count=unread_count)

@app.route('/update-offer-data', methods=['POST'])
def update_offer_data():
    try:
        # التحقق من وجود offer_id
        if 'offer_id' not in request.form:
            flash("معرف العرض مفقود.", "error")
            return redirect(url_for('offers'))

        offer_id = request.form['offer_id']
        offer = Offer.query.get_or_404(offer_id)  # التحقق من وجود العرض

        # تحويل النصوص إلى كائنات تاريخ
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()

        # الحصول على البيانات من النموذج
        name = request.form['name']
        code = request.form['code']
        typename = request.form['typename']
        discount_value = float(request.form['discount_value'])
        description = request.form['description']
        products = request.form.getlist('products')  # الحصول على قائمة المنتجات
        image = request.files.get('image')  # لتحميل الصورة

        # التعامل مع الصورة (إذا كانت موجودة)
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['OFFER_FOLDER'], image_filename))
        else:
            image_filename = offer.image  # استخدام الصورة القديمة

        # تحديث بيانات العرض
        offer.name = name
        offer.code = code
        offer.typename = typename
        offer.discount_value = discount_value
        offer.start_date = start_date
        offer.end_date = end_date
        offer.description = description
        offer.image = image_filename

        # تحديث المنتجات المرتبطة
        db.session.query(OfferProduct).filter_by(offer_id=offer_id).delete()
        for product_id in products:
            offer_product = OfferProduct(offer_id=offer_id, product_id=int(product_id))
            db.session.add(offer_product)

        # حفظ التعديلات
        db.session.commit()

        flash("تم تحديث العرض بنجاح", "success")
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تحديث العرض: {str(e)}', 'error')

    return redirect(url_for('offers'))




@app.route('/delete_offer_trader/<int:offer_id>', methods=['GET'])
@login_required
def delete_offer_trader(offer_id):
    # العثور على التخصص بناءً على ID
    offer = Offer.query.get_or_404(offer_id)
    
    # حذف التخصص
    db.session.delete(offer)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف المنتج بنجاح!', 'success')
    
    return redirect(url_for('offers'))  # إعادة التوجيه إلى صفحة الفئات



#=============================================     المنتجات      ================================
#=============================================     المنتجات      ================================




@app.route('/product_trader', methods=['GET', 'POST'])
@login_required
def product_trader():
        # التحقق من حالة المستخدم
    if current_user.status == 0:
        flash('تم تعطيل حساب التاجر الخاص بك. يرجى التواصل مع الدعم.', 'error')
        return redirect(url_for('home'))
    


    seller_id = current_user.seller_id
    store_image = current_user.store_image

        # التأكد من أن المستخدم مسجل الدخول
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    
    form = ProductForm()
    
    if form.validate_on_submit():
        # التحقق من رفع الصور بشكل منفصل
        image1_file = request.files['image1']
        image2_file = request.files['image2']
        image3_file = request.files['image3']
        image4_file = request.files['image4']
        image5_file = request.files['image5']

        image1_filename = None
        image2_filename = None
        image3_filename = None
        image4_filename = None
        image5_filename = None

        #تحقق من رفع الصور
        if image1_file and image1_file.filename != '':
            image1_filename = secure_filename(image1_file.filename)
            image1_filepath = os.path.join(app.config['PRODUCTS_FOLDER'], image1_filename)
            image1_file.save(image1_filepath)

        if  image2_file and image2_file.filename != '':
            image2_filename = secure_filename(image2_file.filename)
            image2_filepath = os.path.join(app.config['PRODUCTS_FOLDER'], image2_filename)
            image2_file.save(image2_filepath)

        if  image3_file and image3_file.filename != '':
            image3_filename = secure_filename(image3_file.filename)
            image3_filepath = os.path.join(app.config['PRODUCTS_FOLDER'], image3_filename)
            image3_file.save(image3_filepath)

        if  image4_file and image4_file.filename != '':
            image4_filename = secure_filename(image4_file.filename)
            image4_filepath = os.path.join(app.config['PRODUCTS_FOLDER'], image4_filename)
            image4_file.save(image4_filepath)

        if  image5_file and image5_file.filename != '':
            image5_filename = secure_filename(image5_file.filename)
            image5_filepath = os.path.join(app.config['PRODUCTS_FOLDER'], image5_filename)
            image5_file.save(image5_filepath)


        product_category = Subcategory.query.filter_by(name=form.product_category.data).first()
        category_id = product_category.id

        seller_id = current_user.seller_id

        if form.discount.data == None:
            discount = 0.0
        else:
            discount = form.discount.data
        total_after_commission = form.price.data*1.05
        net_profit = form.price.data*0.05
        product = Product(
                    product_name=form.product_name.data, 
                    description=form.description.data, 
                    price=form.price.data, 
                    category_id=category_id,
                    seller_id=seller_id,
                    stock_quantity=form.stock_quantity.data,
                    product_category=form.product_category.data,
                    image1=image1_filename, 
                    image2=image2_filename, 
                    image3=image3_filename, 
                    image4=image4_filename, 
                    image5=image5_filename,
                    discount=discount,
                    total_after_commission=total_after_commission,
                    net_profit=net_profit
                    )
                           
        db.session.add(product)
        db.session.commit()
        flash('تم إضافة المنتج بنجاح!', 'success')
        return redirect(url_for('product_trader'))  # إعادة التوجيه بعد إضافة البيانات

    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM products WHERE seller_id = ?", (seller_id,))
    products = cur.fetchall()



    subcategories = Subcategory.query.filter_by(seller_id=current_user.seller_id)

    unread_count = Notification.query.filter_by(seller_id=seller_id, read_status=0).count()


    return render_template('Trader/products.html' ,store_image=store_image, form=form, products=products , subcategories=subcategories, unread_count=unread_count)



@app.route('/delete_product/<int:product_id>', methods=['GET'])
@login_required
def delete_product(product_id):
    # العثور على التخصص بناءً على ID
    product = Product.query.get_or_404(product_id)
    
    # حذف التخصص
    db.session.delete(product)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف المنتج بنجاح!', 'success')
    
    return redirect(url_for('product_trader'))  # إعادة التوجيه إلى صفحة الفئات


@app.route('/update-product-data', methods=['POST'])
def update_product_data():
    try:
        # التحقق من وجود product_id
        if 'product_id' not in request.form:
            flash("معرف المنتج مفقود.", "error")
            return redirect(url_for('product_trader'))

        product_id = request.form['product_id']
        product = Product.query.get_or_404(product_id)  # التحقق من وجود المنتج

        # الحصول على البيانات من النموذج
        product_name = request.form['product_name']
        description = request.form['description']
        price = float(request.form['price'])
        stock_quantity = int(request.form['stock_quantity'])
        product_category = request.form['product_category']
        discount = float(request.form['discount']) if request.form['discount'] else 0.0

        # التعامل مع الصور
        images = {}
        for i in range(1, 6):  # الصور من image1 إلى image5
            image = request.files.get(f'image{i}')
            if image and image.filename != '':
                image_filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['PRODUCT_IMAGE_FOLDER'], image_filename)
                image.save(image_path)
                images[f'image{i}'] = image_filename
            else:
                images[f'image{i}'] = getattr(product, f'image{i}')  # استخدام الصورة القديمة

        # تحديث بيانات المنتج
        product.product_name = product_name
        product.description = description
        product.price = price
        product.stock_quantity = stock_quantity
        product.product_category = product_category
        product.discount = discount

        # تحديث صور المنتج
        for key, value in images.items():
            setattr(product, key, value)

        # حفظ التعديلات
        db.session.commit()

        flash("تم تحديث المنتج بنجاح", "success")
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تحديث المنتج: {str(e)}', 'error')

    return redirect(url_for('product_trader'))



@app.route('/update-product-status', methods=['POST'])
@login_required
def update_product_status():
    data = request.get_json()
    product_id = data.get('product_id')
    status = data.get('status')

    # تحقق من وجود المنتج
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'}), 404

    # تحديث الحالة
    try:
        product.status = status
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500




#------------------------------------notifications trader---------------------------------
#------------------------------------notifications trader---------------------------------
#------------------------------------notifications trader---------------------------------
#------------------------------------notifications trader---------------------------------


@app.route('/notifications_trader')
@login_required
def notifications_trader():
    seller_id = current_user.seller_id
    store_image = current_user.store_image

    con = sql.connect("instance/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM notifications WHERE seller_id = ?", (seller_id,))
    notifications = cur.fetchall()

    unread_count = Notification.query.filter_by(seller_id=seller_id, read_status=0).count()

    return render_template('Trader/notifications.html', notifications=notifications ,store_image=store_image ,unread_count=unread_count)


@app.route('/mark_as_read/<int:notification_id>', methods=['POST'])
def mark_as_read(notification_id):
    # تحديث حالة القراءة في قاعدة البيانات
    notification = Notification.query.get(notification_id)
    if notification:
        notification.read_status = 1
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Notification not found'}), 404



@app.route('/unread_notifications_count')
def unread_notifications_count():
    user_id = current_user.seller_id  # الحصول على user_id من الجلسة
    if user_id is None:
        return jsonify({'unread_count': 0})  # في حالة عدم وجود مستخدم مسجل دخول
    
    unread_count = Notification.query.filter_by(user_id=user_id, read_status=0).count()
    return jsonify({'unread_count': unread_count})



#===================================     القسم الفرعي    ============================================
#===================================     القسم الفرعي    ============================================


@app.route('/Subcategories', methods=['GET', 'POST'])
@login_required
def Subcategories():

    form = SubcategoryForm()

    if form.validate_on_submit():
        # جلب البيانات من النموذج
        name = form.name.data
        seller_id = current_user.seller_id

        # حفظ الصورة
        image_file = request.files['image']

        image_filename = None

        # تحقق من رفع صورة صاحب المتجر
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_filepath = os.path.join(app.config['SUBCATEGORIES_FOLDER'], image_filename)
            image_file.save(image_filepath)
        # إنشاء قسم فرعي جديد
        new_subcategory = Subcategory(
            name=name,
            image=image_filename,
            seller_id=seller_id
        )

        # حفظ البيانات في قاعدة البيانات
        db.session.add(new_subcategory)
        db.session.commit()

        flash('تم إضافة القسم الفرعي بنجاح!', 'success')
        return redirect(url_for('Subcategories'))
    
    subcategories = Subcategory.query.filter_by(seller_id=current_user.seller_id)
    store_category = current_user.store_category



    return render_template('Trader/Subcategories.html', form=form ,subcategories=subcategories , store_category=store_category)




#===================================    حذف القسم الفرعي    ============================================
#===================================    حذف القسم الفرعي    ============================================

@app.route('/delete_subcategories/<int:id>', methods=['GET'])
def delete_subcategories(id):
    # العثور على التخصص بناءً على ID
    subcategories = Subcategory.query.get_or_404(id)
    
    # حذف التخصص
    db.session.delete(subcategories)
    db.session.commit()
    
    # عرض رسالة بعد الحذف
    flash('تم حذف القسم بنجاح!', 'success')
    
    return redirect(url_for('Subcategories'))  # إعادة التوجيه إلى صفحة الفئات

#===================================    الطلبات الخاصه بالتاجر   ============================================
#===================================    الطلبات الخاصه بالتاجر   ============================================


@app.route('/Orders_trader')
@login_required
def Orders_trader():
    # جلب الطلبات مع التفاصيل الخاصة بالبائع الحالي
    orders = (
        db.session.query(Order, OrderDetail)
        .join(OrderDetail, Order.order_id == OrderDetail.order_id)
        .filter(OrderDetail.seller_name == current_user.seller_name).distinct()   # الطلبات الخاصة بالبائع الحالي
        .order_by(Order.order_date.desc())  # ترتيب حسب تاريخ الطلب
        .all()
    )


    # عدد الإشعارات غير المقروءة
    unread_count = Notification.query.filter_by(seller_id=current_user.seller_id, read_status=0).count()

    return render_template(
        'Trader/orders.html',
        orders=orders,
        unread_count=unread_count
    )


#===================================   تفاصيل الطلبات الخاصه بالتاجر   ============================================
#===================================   تفاصيل الطلبات الخاصه بالتاجر   ============================================



@app.route('/order_details_trader/<int:order_id>')
@login_required
def order_details_trader(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return redirect(url_for('dashboard_trader'))
    
    # إعداد QR Code
    page_url = f"http://127.0.0.1:5000/order_details_trader/{order_id}"
    qr_folder = app.config['UPLOAD_FOLDER_QRCODE']
    qr_filename = f'qrcode_order_{order_id}.png'
    qr_filepath = os.path.join(qr_folder, qr_filename)
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)
    if not os.path.exists(qr_filepath):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(page_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(qr_filepath)

    # جلب تفاصيل الطلب الخاصة بالبائع المسجل حاليًا
    result = db.session.query(Order, OrderDetail)\
        .join(OrderDetail, Order.order_id == OrderDetail.order_id)\
        .filter(OrderDetail.seller_name == current_user.seller_name,  # تحديد البائع المسجل حاليًا
                Order.order_id == order_id)\
        .all()

    order_details = []
    total_price = 0
    total_profit = 0
    seller_names = set()
    sellers = {}


    for order_data, detail in result:
        # جمع أسماء البائعين من تفاصيل الطلب
        if detail.seller_name:
            seller_names.add(detail.seller_name)

        # حساب السعر النهائي والربح
        final_price = detail.price * detail.quantity
        total_price += final_price


        detail.final_price = final_price
        order_details.append(detail)

    # جلب بيانات البائعين بناءً على seller_name
    if seller_names:
        seller_records = Seller.query.filter(Seller.seller_name.in_(seller_names)).all()
        for seller in seller_records:
            sellers[seller.seller_name] = {
                'seller_name': seller.seller_name,
                'phone': seller.phone,
                'address': f"{seller.governorate}, {seller.city}, {seller.village}, {seller.street_address or ''}",
                'store_name': seller.store_name
            }
    unread_count = Notification.query.filter_by(seller_id=current_user.seller_id, read_status=0).count()

    return render_template(
    'Trader/order_detail_trader.html',
    order=order,
    order_details=order_details,
    sellers=list(sellers.values()),  # تحويل القيم إلى قائمة
    total_price=total_price,
    unread_count=unread_count
    )







#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================
#======================================  start_Site   =======================================================



@app.route('/')
def home():
    # جلب المنتجات ومعلومات البائعين
    products = Product.query.options(joinedload(Product.seller)).filter(
        Product.status == 1, Product.seller.has(status=1)).all()

    # جلب البيانات الأخرى
    category = Category.query.all()
    productall = Product.query.all()
    banners = Banner.query.all()
    services = Services.query.filter_by(status=1).all()
    typeservice = Typesofservices.query.all()

    # جلب حالة المستخدم
    if current_user.is_authenticated:
        is_seller = current_user.is_seller
        last_login = current_user.last_login
    else:
        is_seller = False
        last_login = None

    formatted_last_login = format_datetime(last_login, format='d MMMM yyyy/ h:mm a', locale='ar') if last_login else "لم يتم تسجيل الدخول من قبل"

    # جلب العروض النشطة والمعتمدة
    active_offers = Offer.query.filter(
        Offer.status == 1,  # العرض نشط
        Offer.end_date >= datetime.now().date(),  # تاريخ انتهاء العرض مستقبلي
        Offer.approval_status == "approved"  # العرض معتمد
    ).distinct().all()

    # إعداد قائمة لحساب الوقت المتبقي لكل عرض
    offers_with_time_remaining = []

    for offer in active_offers:
        # تحويل تاريخ انتهاء العرض إلى datetime كامل
        offer_end_datetime = datetime.combine(offer.end_date, datetime.min.time())
        time_remaining = offer_end_datetime - datetime.now()

        # حساب الوقت المتبقي بالأيام والساعات والدقائق والثواني
        days_remaining = time_remaining.days
        hours_remaining = time_remaining.seconds // 3600
        minutes_remaining = (time_remaining.seconds % 3600) // 60
        seconds_remaining = time_remaining.seconds % 60

        # إضافة العرض مع الوقت المتبقي إلى القائمة
        offers_with_time_remaining.append({
            'offer': offer,
            'days_remaining': days_remaining,
            'hours_remaining': hours_remaining,
            'minutes_remaining': minutes_remaining,
            'seconds_remaining': seconds_remaining
        })

    # جلب المنتجات حسب الأقسام
    products_electronic = (
        db.session.query(Product)
        .join(Seller, Product.seller_id == Seller.seller_id)  # انضمام المنتجات مع البائعين
        .filter(Seller.store_category == 'أجهزه كهربائيه')  # فلترة القسم في جدول البائعين
        .all()
    )

    products_clothes = (
        db.session.query(Product)
        .join(Seller, Product.seller_id == Seller.seller_id)  # انضمام المنتجات مع البائعين
        .filter(Seller.store_category == 'ملابس')  # فلترة القسم في جدول البائعين
        .all()
    )

    products_phones = (
        db.session.query(Product)
        .join(Seller, Product.seller_id == Seller.seller_id)  # انضمام المنتجات مع البائعين
        .filter(Seller.store_category == 'الهواتف والإكسسوارات')  # فلترة القسم في جدول البائعين
        .all()
    )

    # تحليل البيانات باستخدام KMeans
    query = "SELECT product_id FROM order_details"  # تحديد جدول السلة أو الطلبات
    df = pd.read_sql(query, db.engine)  # استخدام محرك SQLAlchemy لجلب البيانات

    popular_products = []  # تعريف المتغير بقيمة افتراضية فارغة

    if not df.empty:
        # تجهيز البيانات للنموذج
        X = df[['product_id']].dropna()

        # تطبيق التجميع
        kmeans = KMeans(n_clusters=min(5, len(X)), random_state=0)
        df['cluster'] = kmeans.fit_predict(X)

        # الحصول على المجموعة الأكثر شيوعًا
        popular_cluster = df['cluster'].value_counts().idxmax()
        popular_products = df[df['cluster'] == popular_cluster]['product_id'].unique().tolist()

    # جلب تفاصيل المنتجات الأكثر شيوعًا
    if popular_products:
        placeholders = ", ".join([":p{}".format(i) for i in range(len(popular_products))])
        products_query = text(f"""
            SELECT * 
            FROM products 
            WHERE product_id IN ({placeholders})
        """)

        params = {f"p{i}": popular_products[i] for i in range(len(popular_products))}

        with db.engine.connect() as connection:
            result = connection.execute(products_query, params)
            productscommen = result.fetchall()
    else:
        productscommen = []

    # جلب المنتجات المفضلة
    if current_user.is_authenticated:
        user_id = current_user.seller_id  # الحصول على seller_id للمستخدم الحالي
        product_fav = db.session.query(Product).join(FavoriteProduct).filter(FavoriteProduct.seller_id == user_id).all()
    else:
        product_fav = [] 

    # تمرير البيانات إلى القالب
    return render_template(
        'site/home.html',
        products=products,
        category=category,
        services=services,
        typeservice=typeservice,
        is_seller=is_seller,
        banners=banners,
        productall=productall,
        last_login=formatted_last_login,
        offers_with_time_remaining=offers_with_time_remaining,
        products_electronic=products_electronic,
        products_clothes=products_clothes,
        popular_products=popular_products,  # تمرير المنتجات الشائعة إلى القالب
        productscommen=productscommen,
        products_phones=products_phones,
        product_fav=product_fav
    )





@app.route('/offers-with-products', methods=['GET'])
def offers_with_products():
    try:
        # جلب العروض النشطة فقط
        offers = Offer.query.filter_by(status=True).filter(Offer.end_date >= datetime.utcnow().date()).all()

        # لكل عرض، جلب المنتجات المرتبطة
        offers_with_products = []
        for offer in offers:
            products = [Product.query.get(op.product_id) for op in offer.products]
            offers_with_products.append({'offer': offer, 'products': products})

        return render_template('offers_with_products.html', offers_with_products=offers_with_products)

    except Exception as e:
        app.logger.error(f"Error loading offers with products: {e}")
        flash('حدث خطأ أثناء تحميل العروض.', 'error')
        return redirect(url_for('home'))




@app.route('/offer_details')
def offer_details():
    # جلب جميع العروض النشطة
    offers = Offer.query.filter_by(status=True).order_by(Offer.start_date.desc()).all()

    # التحقق من وجود عروض
    if not offers:
        return render_template('site/offer_details.html')

    # جلب المنتجات المرتبطة بكل عرض
    offer_products = {offer.offer_id: [op.product for op in offer.products] for offer in offers}

    banners = Banner.query.all()
    # جلب حالة المستخدم
    if current_user.is_authenticated:
        is_seller = current_user.is_seller
        last_login = current_user.last_login
    else:
        is_seller = False
        last_login = None

    return render_template(
        'site/offer_details.html',
        offers=offers,
        offer_products=offer_products,
        banners=banners,
        is_seller=is_seller
    )


#======================================  هنا اضافة المحافظات و المدن و الاحياء   ===================================
#======================================  هنا اضافة المحافظات و المدن و الاحياء   ===================================

# البيانات الارتباطية (محافظات -> مدن -> أحياء)
data = {
    'القليوبية': {
        'العبور': ['الحي الأول']
    },
    'الشرقية': {
        'الزقازيق': [' القوميه','الغشام','طلبه عويضه'],
        'ههيا': [' شارع السوق',' البحر','  المحكمه',],
    }
}

#======================================  Site_signup   =======================================================
#======================================  Site_signup   =======================================================



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = UserForm()  # إنشاء الكائن من النموذج
    
    if form.validate_on_submit():
        email = form.email.data

        # تحقق من وجود البريد الإلكتروني في قاعدة البيانات
        existing_seller = Seller.query.filter_by(email=email).first()
        if existing_seller:
            # عرض رسالة خطأ
            flash("هذا البريد الإلكتروني مسجل بالفعل . يرجى إدخال بريد إلكتروني مختلف.", "error")
            # مسح الحقول بعد الخطأ
            form.seller_name.data = ''
            form.email.data = ''
            form.phone.data = ''
            form.governorate.data = ''
            form.city.data = ''
            form.village.data = ''
            form.street_address.data = ''
            form.password.data = ''
            return render_template('site/signup.html', form=form)

        # أخذ البيانات من النموذج
        seller_name = form.seller_name.data
        email = form.email.data
        phone = form.phone.data
        governorate = form.governorate.data
        city = form.city.data
        village = form.village.data
        street_address = form.street_address.data
        password = form.password.data
        
        # تشفير كلمة المرور قبل تخزينها
        hashed_password = generate_password_hash(password)

        # إنشاء كائن جديد من Seller
        new_seller = Seller(
            seller_name=seller_name,
            email=email,
            phone=phone,
            governorate=governorate,
            city=city,
            village=village,
            street_address=street_address,
            password=hashed_password,  # كلمة المرور المشفرة
        )
        
        # إضافة البائع الجديد إلى قاعدة البيانات
        db.session.add(new_seller)
        db.session.commit()  # حفظ البيانات في قاعدة البيانات

        login_user(new_seller)

        flash(f"مرحباً {seller_name}، تم تسجيل دخولك بنجاح!", 'success')
        return redirect(url_for('home'))  # أو توجيه إلى الصفحة الرئيسية

    else:
        form.email.data = ''


    return render_template('site/signup.html', form=form, data=data)


@app.route('/get_cities', methods=['POST'])
def get_cities():
    governorate = request.json.get('governorate')  # استلام اسم المحافظة من AJAX
    cities = list(data.get(governorate, {}).keys())  # الحصول على المدن
    return jsonify(cities)

@app.route('/get_villages', methods=['POST'])
def get_villages():
    governorate = request.json.get('governorate')
    city = request.json.get('city')  # استلام اسم المدينة من AJAX
    villages = data.get(governorate, {}).get(city, [])  # الحصول على الأحياء
    return jsonify(villages)


#======================================  Site_is_seller   =======================================================
#======================================  Site_is_seller   =======================================================
@app.route('/is_seller', methods=['GET', 'POST'])
@login_required  # تأكد من أن المستخدم مسجل دخول
def is_seller():
    form = SellerForm()  # إنشاء كائن النموذج

    # تحميل قائمة الفئات من قاعدة البيانات وضبط الخيارات
    category = Category.query.all()
    form.store_category.choices = [(c.category_name, c.category_name) for c in category]

    # الحصول على البيانات من النموذج
    store_name = request.form.get('store_name')
    store_category = request.form.get('store_category')
    store_image = request.files.get('store_image')  # لتحميل الصورة
    owner_banner = request.files.get('owner_banner')  # لتحميل الصورة


    # تحديث الحالة is_seller بناءً على اسم المتجر
    if store_name:  # إذا كان اسم المتجر غير فارغ
        current_user.is_seller = 1
        current_user.status = 1
    else:  # إذا كان اسم المتجر فارغًا
        current_user.is_seller = 0
        current_user.status = 0

    # تحديث البيانات في قاعدة البيانات
    if store_image:
        # حفظ الصورة (إذا كانت موجودة)
        image_filename = secure_filename(store_image.filename)
        store_image.save(os.path.join(app.config['UPLOAD_FOLDER_TRADER_LOGO'], image_filename))

    if owner_banner:
        # حفظ الصورة (إذا كانت موجودة)
        imagebanner_filename = secure_filename(owner_banner.filename)
        owner_banner.save(os.path.join(app.config['UPLOAD_FOLDER_TRADER_BANNER'], imagebanner_filename))


        
    # تحديث بيانات المستخدم
        current_user.store_name = store_name
        current_user.store_category = store_category
        current_user.store_image = image_filename
        current_user.owner_banner = imagebanner_filename


        # حفظ التغييرات
        db.session.commit()




        flash("تم تحديث بياناتك كبائع بنجاح!", "success")
        return redirect(url_for('home'))  # إعادة التوجيه إلى الصفحة الرئيسية بعد التحديث
    
    else:
        flash("خطأ في التسجيل الرجاء المحاوله لاحقا", "error")



    # إعادة تحميل الصفحة مع النموذج في حالة عدم تقديم النموذج بنجاح
    return render_template('site/is_seller.html', form=form, category=category)


#======================================  Site_login   =======================================================
#======================================  Site_login   =======================================================


@app.route('/login', methods=['GET', 'POST'])
def login():
    if  current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        seller = Seller.query.filter_by(email=form.email.data).first()
        if seller:
            # فك تشفير كلمة المرور المخزنة في قاعدة البيانات
            if seller and check_password_hash(seller.password, form.password.data):
                # تحديث حقل last_login
                seller.last_login = datetime.now()
                db.session.commit()
                flash(f"مرحباً {seller.seller_name}، تم تسجيل دخولك بنجاح!", 'success')
                
                login_user(seller)
                next_page = request.args.get('next')
                if next_page and next_page.startswith('/'):  # تحقق من صحة الرابط
                    return redirect(next_page)
                return redirect(url_for('home'))

            else:
                flash('خطأ في البريد الإلكتروني أو كلمة المرور.', 'error')
        else:
            flash('خطأ في البريد الإلكتروني أو كلمة المرور.', 'error')
    
    return render_template('site/login.html', form=form)  # عرض نموذج تسجيل الدخول



#======================================== تسجيل الخروج   ==================================================

@app.route('/logout')
def logout():
    # تسجيل الخروج
    logout_user()

    # رسالة فلاش للتأكيد
    flash("تم تسجيل الخروج بنجاح.", "info")

    # إعادة التوجيه إلى صفحة تسجيل الدخول
    return redirect(url_for('home'))




#========================================  عربة التسوق   ==================================================
@app.route('/add-to-cart', methods=['POST'])
@login_required
@limiter.limit("1 per second")  # السماح بطلب واحد فقط لكل ثانية
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    seller_id = data.get('seller_id')

    if not product_id or not seller_id:
        return redirect(url_for('login'))

    try:
        # البحث عن المنتج
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'المنتج غير موجود'}), 404

        # حساب السعر القديم
        old_price = product.total_after_commission
        discounted_price = old_price
        new_offer_price = 0.0  # مبدئيًا سيكون صفرًا إذا لم يكن هناك عرض

        # التحقق من وجود خصومات مباشرة
        if product.discount and product.discount > 0:
            discounted_price = old_price - (old_price * (product.discount / 100))

        # التحقق من وجود عروض نشطة مرتبطة بالمنتج
        if product.has_active_offer():
            active_offer = next(
                (
                    offer_product.offer for offer_product in product.offers
                    if offer_product.offer.status
                    and offer_product.offer.approval_status == 'approved'
                    and offer_product.offer.start_date <= date.today()
                    and offer_product.offer.end_date >= date.today()
                ),
                None
            )
            if active_offer:
                # تطبيق الخصم بناءً على نوع العرض من السعر المخفض بعد الخصم العام
                if active_offer.typename == 'discount':  # خصم بالنسبة المئوية
                    offer_discounted_price = discounted_price - (discounted_price * (active_offer.discount_value / 100))
                elif active_offer.typename == 'value':  # خصم بقيمة ثابتة
                    offer_discounted_price = discounted_price - active_offer.discount_value
                else:
                    offer_discounted_price = discounted_price  # في حال نوع عرض غير معروف

                # اختيار السعر النهائي بعد خصم العرض
                new_offer_price = max(offer_discounted_price, 0.0)

        # التأكد من أن السعر المخفض لا يقل عن الصفر
        discounted_price = max(discounted_price, 0.0)

        # البحث عن المنتج في سلة العميل
        existing_cart_item = Cart.query.filter_by(product_id=product_id, seller_id=seller_id).first()

        if existing_cart_item:
            # إذا كان المنتج موجودًا، زيادة الكمية بمقدار واحد
            existing_cart_item.quantity += 1

            # تحديد السعر الإجمالي بناءً على الشروط
            if product.has_active_offer() and existing_cart_item.new_offer_price:
                total_price = existing_cart_item.new_offer_price * existing_cart_item.quantity
            elif product.discount and product.discount > 0:
                total_price = existing_cart_item.price * existing_cart_item.quantity
            elif product.discount == 0 and not product.has_active_offer():
                total_price = existing_cart_item.old_price * existing_cart_item.quantity
            else:
                total_price = 0

            # تحديث الأسعار
            existing_cart_item.old_price = old_price
            existing_cart_item.price = discounted_price
            existing_cart_item.new_offer_price = new_offer_price
            existing_cart_item.total_price = total_price
        else:
            # إذا كان المنتج غير موجود في السلة، إضافته كمنتج جديد
            if product.has_active_offer() and new_offer_price:
                total_price = new_offer_price
            elif product.discount and product.discount > 0:
                total_price = discounted_price
            elif product.discount == 0:
                total_price = old_price
            else:
                total_price = 0

            new_cart_item = Cart(
                seller_id=seller_id,
                product_id=product_id,
                quantity=1,
                old_price=old_price,
                price=discounted_price,
                new_offer_price=new_offer_price,
                total_price=total_price
            )
            db.session.add(new_cart_item)

        # حفظ التغييرات في قاعدة البيانات
        db.session.commit()

        return jsonify({'success': True, 'message': 'تم إضافة المنتج إلى السلة أو زيادة الكمية'})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء إضافة المنتج إلى السلة'})




@app.route('/cart', methods=['GET'])
@login_required
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    
    # استرداد جميع العناصر في السلة للمستخدم الحالي مع تفاصيل المنتج
    cart_items = (
        db.session.query(Cart, Product)
        .join(Product, Cart.product_id == Product.product_id)
        .filter(Cart.seller_id == current_user.seller_id)
        .all()
    )

    if not cart_items:
        return render_template('site/cart.html', cart_items=[], message="السلة فارغة حالياً.")
    
    # حساب إجمالي السعر القديم
    # حساب إجمالي السعر قبل الخصم مع تقريب إلى منزلتين عشريتين
    total_old_price = round(sum(
        cart_item.Cart.old_price * cart_item.Cart.quantity for cart_item in cart_items
    ), 2)

    # حساب الإجمالي بعد الخصم مع تقريب إلى منزلتين عشريتين
    total_after_discount = round(sum(
        cart_item.Cart.total_price for cart_item in cart_items
    ), 2)

    # حساب إجمالي الخصومات مع تقريب إلى منزلتين عشريتين
    total_discounts = round(total_old_price - total_after_discount, 2)


    offers = Offer.query.all()
    is_seller = current_user.is_seller

# جلب عدد المنتجات في سلة المستخدم الحالي
    if current_user.is_authenticated:
        user_id = current_user.seller_id  # أو current_user.seller_id إذا كنت تستخدم seller_id
        countproduct = Cart.query.filter_by(seller_id=user_id).count()
    else:
        countproduct = 0  # إذا لم يكن المستخدم مسجل الدخول، يكون العدد صفر    # تمرير البيانات إلى القالب
    return render_template(
    'site/cart.html', 
    cart_items=cart_items, 
    total_old_price=total_old_price, 
    total_discounts=total_discounts, 
    total_after_discount=total_after_discount,
    offers=offers,
    is_seller=is_seller,
    countproduct=countproduct
)



@app.route('/update-cart-totals', methods=['GET'])
@login_required
def update_cart_totals():
    # استرداد جميع العناصر في السلة للمستخدم الحالي مع تفاصيل المنتج
    cart_items = (
        db.session.query(Cart, Product)
        .join(Product, Cart.product_id == Product.product_id)
        .filter(Cart.seller_id == current_user.seller_id)
        .all()
    )

    # حساب إجمالي السعر القديم
    total_old_price = round(sum(
        cart_item.Cart.old_price * cart_item.Cart.quantity for cart_item in cart_items
    ), 2)

    # حساب الإجمالي بعد الخصم
    total_after_discount = round(sum(
        cart_item.Cart.total_price for cart_item in cart_items
    ), 2)

    # حساب إجمالي الخصومات
    total_discounts = round(total_old_price - total_after_discount, 2)

    # إعادة الإجماليات كـ JSON
    return jsonify({
        'total_old_price': total_old_price,
        'total_discounts': total_discounts,
        'total_after_discount': total_after_discount
    })





@app.route('/remove-from-cart/<int:cart_id>', methods=['GET', 'POST'])
@login_required
def remove_from_cart(cart_id):
    # محاولة العثور على العنصر في السلة بناءً على cart_id و معرف المستخدم
    cart_item = Cart.query.filter_by(cart_id=cart_id, seller_id=current_user.seller_id).first()

    if cart_item:
        # إذا تم العثور على العنصر، قم بحذفه
        db.session.delete(cart_item)
        db.session.commit()

    # بعد الحذف، أعد توجيه المستخدم إلى صفحة السلة أو أي مكان آخر
    return redirect(url_for('cart'))


@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    cart_id = data.get('cart_id')
    quantity = data.get('quantity')

    if not cart_id or not quantity:
        return jsonify({'success': False, 'message': 'بيانات غير مكتملة'}), 400

    try:
        # البحث عن العنصر في السلة
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return jsonify({'success': False, 'message': 'العنصر غير موجود في السلة'}), 404

        # تحديث الكمية
        cart_item.quantity = quantity

        # جلب المنتج المرتبط بهذا العنصر
        product = Product.query.get(cart_item.product_id)

        # تحديد السعر الذي سيتم ضرب الكمية فيه
        if product.has_active_offer() and cart_item.new_offer_price:  # خصم عرض
            total_price = cart_item.new_offer_price * cart_item.quantity
        elif product.discount and product.discount > 0:  # خصم عام
            total_price = cart_item.price * cart_item.quantity
        elif product.discount == 0 and not product.has_active_offer():  # لا يوجد خصم
            total_price = cart_item.old_price * cart_item.quantity
        else:
            total_price = 0  # إذا لم تكن هناك أسعار


        # تحديث حقل total_price في العنصر
        cart_item.total_price = total_price

        # حفظ التحديثات في قاعدة البيانات
        db.session.commit()


        # حساب إجمالي السعر القديم لجميع المنتجات للمستخدم الحالي
        all_cart_items = Cart.query.filter_by(seller_id=current_user.seller_id).all()
        
        # جمع إجمالي الأسعار (price / new_offer_price)
        total_price = sum(
            item.new_offer_price if item.new_offer_price else item.price for item in all_cart_items
        )
        
        # جمع إجمالي الأسعار القديمة (old_price)
        total_old_price = sum(
            item.old_price for item in all_cart_items
        )

        return jsonify({
            'success': True,
            'total_price': round(total_price, 2),
            'total_old_price': round(total_old_price, 2)
        })
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء تحديث الكمية'})
    


@app.route('/complete-order-with-location', methods=['POST'])
@login_required
def complete_order_with_location():
    try:
        # استرداد عناصر السلة
        cart_items = db.session.query(Cart, Product, Seller).join(
            Product, Cart.product_id == Product.product_id
        ).join(
            Seller, Product.seller_id == Seller.seller_id
        ).filter(
            Cart.seller_id == current_user.seller_id
        ).all()

        if not cart_items:
            return jsonify({'success': False, 'message': 'السلة فارغة. لا يوجد منتجات لإكمال الطلب.'}), 404

        # التحقق من توفر الكميات في المخزون
        for item in cart_items:
            if item.Product.stock_quantity < item.Cart.quantity:
                return jsonify({
                    'success': False,
                    'message': f"الكمية المتوفرة من المنتج {item.Product.product_name} غير كافية."
                }), 400

        total_after_discount = round(sum(
        cart_item.Cart.total_price for cart_item in cart_items
        ), 2)

        # البيانات من الطلب
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        payment_method = data.get('payment_method')

        if None in [latitude, longitude, payment_method, total_after_discount]:
            return jsonify({'success': False, 'message': 'بيانات الطلب غير مكتملة.'}), 400

        # حفظ الطلب
        new_order = Order(
            customer_name=current_user.seller_name,
            phone=current_user.phone,
            order_date=datetime.now(),
            order_status='pending',
            total_amount=total_after_discount,
            payment_method=payment_method,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(new_order)
        db.session.flush()  # الحصول على order_id قبل commit

        # تفاصيل الطلب
        for item in cart_items:
            # حساب الخصم بناءً على نوع الخصم
            if item.Product.has_active_offer() and item.Cart.new_offer_price:  # خصم عرض
                discounted_price_commission = item.Cart.new_offer_price
            elif item.Product.discount and item.Product.discount > 0:  # خصم عام
                discounted_price_commission = item.Cart.price
            elif item.Product.discount == 0 and not item.Product.has_active_offer():  # لا يوجد خصم
                discounted_price_commission = item.Cart.old_price
            else:
                discounted_price_commission = 0

            
            discounted_price_trader = item.Product.price  # السعر الأصلي

            # تطبيق الخصم العام (إن وجد)
            if item.Product.discount and item.Product.discount > 0:  # خصم عام
                discounted_price_trader = discounted_price_trader * (1 - item.Product.discount / 100)

            # التحقق من وجود خصم عرض (إن وجد)
            active_offer = next(
                (
                    offer_product.offer for offer_product in item.Product.offers
                    if offer_product.offer.status
                    and offer_product.offer.approval_status == 'approved'
                    and offer_product.offer.start_date <= date.today()
                    and offer_product.offer.end_date >= date.today()
                ),
                None
            )

            # تطبيق خصم العرض بعد الخصم العام
            if active_offer:
                if active_offer.typename == 'discount':  # خصم بنسبة مئوية
                    discounted_price_trader = discounted_price_trader - (
                        discounted_price_trader * (active_offer.discount_value / 100)
                    )
                elif active_offer.typename == 'value':  # خصم بقيمة ثابتة
                    discounted_price_trader = discounted_price_trader - active_offer.discount_value

            # التأكد من أن السعر النهائي لا يقل عن الصفر
            discounted_price_trader = max(discounted_price_trader, 0.0)
            
            order_detail = OrderDetail(
                order_id=new_order.order_id,
                product_id=item.Product.product_id,
                quantity=item.Cart.quantity,
                price=discounted_price_trader,
                product_name=item.Product.product_name,
                seller_name=item.Seller.seller_name,
                store_name=item.Seller.store_name,
                customer_name=current_user.seller_name,
                customer_address=f"{current_user.street_address}, {current_user.village}, {current_user.city}, {current_user.governorate}",
                customer_phone=current_user.phone,
                price_comition=discounted_price_commission
            )
            db.session.add(order_detail)

            # تحديث كمية المنتج في المخزون
            item.Product.stock_quantity -= item.Cart.quantity

        # حذف عناصر السلة
        Cart.query.filter_by(seller_id=current_user.seller_id).delete()

        # حفظ التغييرات في قاعدة البيانات
        db.session.commit()

        # تخزين بيانات الطلب في الجلسة
        session['order_id'] = new_order.order_id
        session['total_amount'] = total_after_discount

        # إرجاع بيانات النجاح مع رسالة نجاح
        return jsonify({'success': True, 'message': 'تم إكمال الطلب بنجاح.'})

    except Exception as e:
        db.session.rollback()  # التراجع عن التغييرات في حالة حدوث خطأ
        print(f"حدث خطأ: {e}")
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء إكمال الطلب.'}), 500



@app.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        total_amount = data.get('total_amount')

        # تحقق من صحة الطلب
        order = Order.query.filter_by(order_id=order_id, customer_name=current_user.seller_name).first()
        if not order:
            return jsonify({'success': False, 'message': 'الطلب غير موجود.'}), 404

        if order.payment_status:
            return jsonify({'success': False, 'message': 'تم دفع هذا الطلب بالفعل.'})

        # تحقق من تطابق المبلغ
        if float(total_amount) != float(order.total_amount):
            return jsonify({'success': False, 'message': 'المبلغ غير متطابق مع الطلب.'})

        # تحديث حالة الدفع
        order.payment_status = True
        db.session.commit()

        return jsonify({'success': True, 'message': 'تم الدفع بنجاح!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء معالجة الدفع.'}), 500



@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        # استقبال البيانات من النموذج
        order_id = request.form.get('order_id')
        total_price = request.form.get('price')
        phone = request.form.get('phone')

        # التحقق من صحة البيانات المدخلة
        if not order_id or not total_price or not phone:
            flash('يجب إدخال جميع البيانات المطلوبة.', 'error')
            return redirect(url_for('payment'))

        try:
            # جلب الطلب باستخدام order_id
            print(f"Received Order ID: {order_id}, Price: {total_price}, Phone: {phone}")
            order = Order.query.filter_by(order_id=int(order_id)).first()
            
            if not order:
                flash('الطلب غير موجود.', 'error')
                return redirect(url_for('payment'))
            
            # تحديث الحقول المرتبطة بالدفع
            order.payment_price = float(total_price)
            order.payment_phone = phone
            db.session.commit()  # حفظ التغييرات في قاعدة البيانات

            flash('تم حفظ بيانات الدفع بنجاح.', 'success')
            return redirect(url_for('my_orders'))

        except Exception as e:
            db.session.rollback()  # التراجع عن التغييرات في حالة وجود خطأ
            print(f"Error during payment save: {e}")  # طباعة الخطأ للمراجعة
            flash('حدث خطأ أثناء حفظ بيانات الدفع.', 'error')
            return redirect(url_for('payment'))

    # GET request - عرض صفحة الدفع
    order_id = session.get('order_id')
    total_amount = session.get('total_amount')

    if not order_id or not total_amount:
        return redirect('/')

    # جلب الطلب من قاعدة البيانات إذا كان order_id موجودًا
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        flash('الطلب غير موجود.', 'error')
        return redirect('/')

    is_seller = current_user.is_seller
    return render_template(
        'site/payment.html',
        total_amount=total_amount,
        is_seller=is_seller,
        order_id=order_id
    )




@app.route('/update-payment-status', methods=['POST'])
@login_required
def update_payment_status():
    data = request.get_json()
    order_id = data.get('order_id')
    payment_status = data.get('payment_status')  # قيمة Boolean

    if order_id is None or payment_status is None:
        return jsonify({'success': False, 'message': 'بيانات غير مكتملة'}), 400

    try:
        # جلب الطلب من قاعدة البيانات
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'success': False, 'message': 'الطلب غير موجود'}), 404

        # تحديث حالة الدفع
        order.payment_status = payment_status
        db.session.commit()  # حفظ التغييرات

        return jsonify({'success': True, 'message': 'تم تحديث حالة الدفع بنجاح'})
    except Exception as e:
        db.session.rollback()  # التراجع عن التغييرات عند حدوث خطأ
        print(e)  # لطباعة الخطأ أثناء التطوير
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء تحديث حالة الدفع'}), 500



@app.route('/update-order-status', methods=['POST'])
@login_required
def update_order_status():
    data = request.get_json()
    order_id = data.get('order_id')
    order_status = data.get('order_status')

    try:
        # جلب الطلب من قاعدة البيانات
        order = Order.query.get(order_id)
        if order:
            # تحديث حالة الطلب
            order.order_status = order_status
            db.session.commit()
            return jsonify({'success': True, 'message': 'تم تحديث حالة الطلب بنجاح'})
        else:
            return jsonify({'success': False, 'message': 'الطلب غير موجود'}), 404
    except Exception as e:
        db.session.rollback()
        print(e)  # لتصحيح الأخطاء
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء تحديث حالة الطلب'}), 500




@app.route('/my-orders')
@login_required
def my_orders():
    # جلب جميع الطلبات الخاصة بالمستخدم الحالي
    orders = (
        db.session.query(Order)
        .filter(Order.customer_name == current_user.seller_name)
        .order_by(Order.order_date.desc())
        .all()
    )
    is_seller = current_user.is_seller

    return render_template('site/my_orders.html', orders=orders,
                           is_seller=is_seller)




#================================================   order details   ===========================================
#================================================   order details   ===========================================


@app.route('/order_details/<int:order_id>')
@login_required
def order_details(order_id):
    # جلب الطلب والتحقق من أنه يخص المستخدم الحالي
    order = Order.query.filter_by(order_id=order_id, customer_name=current_user.seller_name).first()

    if not order:
        # إذا لم يتم العثور على الطلب، أو لم يكن يخص المستخدم الحالي
        return redirect(url_for('home')), 403  # إعادة التوجيه إلى الصفحة الرئيسية مع كود خطأ 403

    # عمل JOIN بين جدول الطلبات وتفاصيل الطلب
    result = db.session.query(Order, OrderDetail).join(OrderDetail, Order.order_id == OrderDetail.order_id)\
        .filter(Order.order_id == order_id).all()
    
    # تجهيز البيانات للإرسال للقالب
    order_details = []
    total_price = 0  # المتغير لحساب المجموع الكلي

    # جمع البيانات وحساب الأسعار
    for order_data, detail in result:
        # حساب السعر النهائي للمنتج (السعر * الكمية)
        final_price = detail.price_comition * detail.quantity
        total_price += final_price  # إضافة السعر النهائي إلى المجموع الكلي
        # إضافة السعر النهائي إلى التفاصيل
        detail.final_price = final_price
        order_details.append(detail)


    # تمرير البيانات إلى القالب
    return render_template('site/order_details.html', order=order, order_details=order_details, total_price=total_price )





@app.route('/delete_order', methods=['POST'])
@login_required
def delete_order():
    order_id = request.form.get('order_id')

    if not order_id:
        flash('لم يتم تحديد الطلب المراد حذفه.', 'error')
        return redirect(url_for('my_orders'))

    try:
        # البحث عن الطلب في قاعدة البيانات
        order = Order.query.filter_by(order_id=int(order_id)).first()

        if not order:
            flash('الطلب غير موجود.', 'error')
            return redirect(url_for('my_orders'))
        
        # حذف الطلب من قاعدة البيانات
        db.session.delete(order)
        db.session.commit()

        flash('تم حذف الطلب بنجاح.', 'success')
    except Exception as e:
        db.session.rollback()
        print(f"Error while deleting order: {e}")
        flash('حدث خطأ أثناء حذف الطلب.', 'error')

    return redirect(url_for('my_orders'))


#======================================  Site_about   =======================================================
#======================================  Site_about   =======================================================



@app.route('/about')
@login_required
def about():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template('site/about.html')  # عرض نموذج تسجيل الدخول



@app.route('/product_details/<int:product_id>')
def product_details(product_id):

    # جلب حالة المستخدم
    if current_user.is_authenticated:
        is_seller = current_user.is_seller
    else:
        is_seller = False   

    # جلب المنتج بناءً على product_id
    product = Product.query.filter_by(product_id=product_id).first()
    
    if not product:
        return "المنتج غير موجود", 404
    
     # جلب المنتجات في نفس الفئة (باستثناء المنتج الحالي)
    related_products = Product.query.filter_by(category_id=product.category_id).filter(Product.product_id != product_id).all()

    
    
    return render_template('site/product_details.html', product=product,
                                                        related_products=related_products,
                                                        is_seller=is_seller)  # عرض نموذج تسجيل الدخول



@app.route('/alltrader', methods=['GET'])
def alltrader():
    # جلب اسم البحث من الطلب
    search_query = request.args.get('search', '').strip()

    # جلب جميع المتداولين مع عدد المنتجات، متوسط التقييم، وعدد التقييمات لكل بائع
    query = (
        db.session.query(
            Seller,
            func.count(db.distinct(Product.product_id)).label('product_count'),  # عد المنتجات الفريدة
            func.avg(SellerReview.rating).label('avg_rating'),  # متوسط التقييم لكل بائع
            func.count(db.distinct(SellerReview.review_id)).label('review_count')  # عدد التقييمات الفريدة لكل بائع
        )
        .outerjoin(Product, Seller.seller_id == Product.seller_id)
        .outerjoin(SellerReview, Seller.seller_id == SellerReview.seller_id)
        .filter(Seller.is_seller != 0, Seller.status != 0)
    )

    # تصفية النتائج إذا تم إدخال نص للبحث
    if search_query:
        query = query.filter(Seller.seller_name.ilike(f'%{search_query}%'))

    # تنفيذ الاستعلام
    traders = query.group_by(Seller.seller_id).all()


    # معالجة البيانات لتنسيقها للنموذج
    formatted_traders = [
        {
            "seller": trader,
            "product_count": product_count,
            "avg_rating": round(avg_rating or 0, 1),  # متوسط التقييم (يصبح 0 في حالة عدم وجود تقييم)
            "review_count": review_count  # عدد التقييمات الفريدة
        }
        for trader, product_count, avg_rating, review_count in traders
    ]

    # جلب حالة المستخدم
    is_seller = current_user.is_authenticated and current_user.is_seller

    # تمرير البيانات إلى القالب
    return render_template(
        'site/alltrader.html',
        traders=formatted_traders,
        is_seller=is_seller,
        search_query=search_query
    )


@app.route('/filter-products', methods=['POST'])
def filter_products():
    try:
        criteria = request.json
        
        # بناء الاستعلام الأساسي
        query = Product.query

        # فلترة حسب المتاجر
        if criteria['stores']:
            query = query.filter(Product.seller_id.in_(criteria['stores']))

        # فلترة حسب الأقسام
        if criteria['categories']:
            query = query.filter(Product.category_id.in_(criteria['categories']))

        # فلترة حسب السعر
        if criteria['minPrice']:
            query = query.filter(Product.total_after_commission >= float(criteria['minPrice']))
        if criteria['maxPrice']:
            query = query.filter(Product.total_after_commission <= float(criteria['maxPrice']))

        # فلترة المنتجات المخفضة فقط
        if criteria['hasDiscount']:
            query = query.filter(Product.discount > 0)

        # تنفيذ الاستعلام
        products = query.all()

        # تحويل النتائج إلى JSON
        products_data = [{
            'product_id': p.product_id,
            'product_name': p.product_name,
            'image1': p.image1,
            'discount': p.discount,
            'original_price': float(p.total_after_commission),
            'final_price': float(p.total_after_commission * (1 - (p.discount / 100))) if p.discount else float(p.total_after_commission),
            'store_name': p.seller.store_name if p.seller else 'غير محدد'
        } for p in products]

        return jsonify({
            'success': True,
            'products': products_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500




@app.route('/trader/<int:seller_id>')
def trader_details(seller_id):
    # جلب تفاصيل التاجر
    trader = Seller.query.get_or_404(seller_id)

    # الحصول على القسم الفرعي (subcategory_id) إذا تم إرساله
    subcategory_id = request.args.get('subcategory_id', type=int)

    # جلب المنتجات الخاصة بالتاجر مع الفلترة بناءً على القسم الفرعي
    if subcategory_id:
        # فلترة المنتجات حسب قسم فرعي معين
        products = Product.query.filter_by(seller_id=seller_id, category_id=subcategory_id).all()
    else:
        # جلب جميع المنتجات الخاصة بالتاجر
        products = Product.query.filter_by(seller_id=seller_id).all()

    # حساب متوسط التقييمات الخاصة بالتاجر
    avg_rating = db.session.query(db.func.avg(SellerReview.rating)).filter_by(seller_id=seller_id).scalar()
    avg_rating = round(avg_rating or 0, 1)

    # جلب حالة المستخدم
    if current_user.is_authenticated:
        is_seller = current_user.is_seller
    else:
        is_seller = False

    # تمرير البيانات إلى القالب
    return render_template(
        'site/trader_details.html',
        trader=trader,
        products=products,
        avg_rating=avg_rating,
        is_seller=is_seller
    )





@app.route('/allproduct')
def all_product():
    products=Product.query.filter_by(status = 1).all()
    # جلب حالة المستخدم
    if current_user.is_authenticated:
        is_seller = current_user.is_seller
    else:
        is_seller = False   
    return render_template('site/all_product.html', products=products,
                                                    is_seller=is_seller,
                                                    )



@app.route('/rate-seller', methods=['POST'])
def rate_seller():
    try:
        data = request.get_json()
        customer_id = current_user.seller_id  # الحصول على معرف العميل
        seller_id = data.get('seller_id')  # الحصول على معرف البائع
        rating = data.get('rating')  # الحصول على التقييم
        comment = data.get('comment', '')  # التعليق اختياري

        if not seller_id or not rating or not customer_id:
            return jsonify({'success': False, 'message': 'يرجى توفير معرف العميل، البائع، والتقييم.'}), 400

        # الحصول على البائع من قاعدة البيانات
        seller = Seller.query.get(seller_id)
        if not seller:
            return jsonify({'success': False, 'message': 'البائع غير موجود.'}), 404

        # إنشاء التقييم الجديد في جدول seller_reviews
        new_review = SellerReview(
            rating=rating,
            comment=comment,
            customer_id=customer_id,
            seller_id=seller_id
        )
        
        db.session.add(new_review)  # إضافة التقييم الجديد إلى الجلسة
        db.session.commit()  # حفظ التقييم في قاعدة البيانات

        return jsonify({'success': True, 'message': 'تم إرسال التقييم بنجاح.'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'حدث خطأ أثناء إرسال التقييم.', 'error': str(e)}), 500



@app.route('/profile')
@login_required
def seller_profile():
    """عرض الملف الشخصي للبائع"""

    if not current_user.is_authenticated or not current_user.is_seller:
        flash('غير مصرح لك بالوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('home'))

    # حساب متوسط التقييمات
    avg_rating = db.session.query(db.func.avg(SellerReview.rating)).filter_by(seller_id=current_user.seller_id).scalar()
    avg_rating = round(avg_rating or 0, 1)

    # جلب التعليقات مع بيانات العملاء
    comments = db.session.query(SellerReview).filter(
        SellerReview.seller_id == current_user.seller_id,
        SellerReview.comment.isnot(None),
        SellerReview.comment != ""
    ).all()

    return render_template(
        'site/profile.html',
        seller=current_user,
        is_seller=current_user.is_seller,
        avg_rating=avg_rating,
        comments=comments
    )




@app.route('/update_seller_info', methods=['POST'])
def update_seller_info():
    data = request.json
    try:
        # افتراض وجود نموذج "Seller" في قاعدة البيانات
        seller = Seller.query.get(current_user.seller_id)

        # تحديث القيم بناءً على البيانات المستلمة
        seller.seller_name = data.get('seller_name', seller.seller_name)
        seller.store_name = data.get('store_name', seller.store_name)
        seller.store_category = data.get('store_category', seller.store_category)
        seller.email = data.get('email', seller.email)
        seller.phone = data.get('phone', seller.phone)

        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500






@app.route('/update-image/<int:seller_id>', methods=['POST'])
@login_required
def update_image(seller_id):
    seller = Seller.query.get_or_404(seller_id)
    image_type = request.form.get('image_type')  # تحديد نوع الصورة
    
    # الحصول على ملف الصورة من الطلب
    image_file = request.files.get('image_file')
    if image_file and image_file.filename != '':
        image_filename = secure_filename(image_file.filename)

        # تحديد المسار حسب نوع الصورة
        if image_type == 'store_image':
            image_filepath = os.path.join(app.config['UPLOAD_FOLDER_TRADER_LOGO'], image_filename)
            seller.store_image = image_filename  # تحديث الصورة في قاعدة البيانات
        elif image_type == 'banner_image':
            image_filepath = os.path.join(app.config['UPLOAD_FOLDER_TRADER_BANNER'], image_filename)
            seller.owner_banner = image_filename  # تحديث البانر
        elif image_type == 'profile_image':
            image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            seller.owner_image = image_filename  # تحديث صورة البروفايل
        else:
            flash("نوع الصورة غير معروف.", "error")
            return redirect(url_for('seller_profile'))
        
        # حفظ الصورة وتحديث قاعدة البيانات
        image_file.save(image_filepath)
        db.session.commit()

        flash(f"تم تحديث الصوره بنجاح!", "success")
    else:
        flash("يرجى اختيار صورة صالحة.", "error")
    
    return redirect(url_for('seller_profile'))


@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    try:
        # الحصول على بيانات المنتج والمستخدم من الطلب
        seller_id = current_user.seller_id
        product_id = request.json.get('product_id')

        # التحقق من صحة البيانات
        if not seller_id or not product_id:
            return jsonify({'message': 'Missing data'}), 400

        # التحقق إذا كان المنتج مضافًا مسبقًا
        existing_favorite = FavoriteProduct.query.filter_by(seller_id=seller_id, product_id=product_id).first()
        if existing_favorite:
            return jsonify({'message': 'Product is already in favorites'}), 200

        # إضافة المنتج إلى جدول المفضلة
        favorite = FavoriteProduct(seller_id=seller_id, product_id=product_id)
        db.session.add(favorite)
        db.session.commit()


    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500


@app.route('/favorites')
@login_required  # تأكد أن المستخدم مسجل الدخول
def favorites():
        # جلب المنتجات المفضلة بناءً على معرف المستخدم
        user_id = current_user.seller_id # إذا كنت تستخدم Flask-Login
        favorite_products = db.session.query(Product).join(FavoriteProduct).filter(FavoriteProduct.seller_id == user_id).all()

        # تمرير المنتجات المفضلة إلى القالب
        return render_template('site/favorites.html', favorite_products=favorite_products)



@app.route('/remove_favorite/<int:product_id>', methods=['POST'])
@login_required
def remove_favorite(product_id):
    try:
        seller_id = current_user.seller_id   # هوية المستخدم الحالي
        favorite = FavoriteProduct.query.filter_by(product_id=product_id, seller_id=seller_id).first()

        if not favorite:
            return jsonify({'message': 'Product not found in favorites'}), 404

        db.session.delete(favorite)
        db.session.commit()

        return redirect(url_for('favorites'))  # إعادة توجيه المستخدم إلى صفحة المفضلة
    except Exception as e:
        return f"An error occurred: {str(e)}", 500





@app.route('/category_products/<category_name>', methods=['GET'])
def category_products(category_name):
    # الحصول على المتاجر المرتبطة بهذا القسم
    sellers = Seller.query.filter_by(store_category=category_name).all()
    
    # الحصول على جميع المنتجات الخاصة بهذه المتاجر
    products = Product.query.filter(Product.seller_id.in_([seller.seller_id for seller in sellers])).all()
    

    return render_template('site/category_products.html', products=products, top_sellers=sellers)





#===================================== API_get ==================================================
#===================================== API_get ==================================================
#===================================== API_get ==================================================
#===================================== API_get ==================================================
#===================================== API_get ==================================================



@app.route('/get_sellers', methods=['GET'])
def get_sellers():
    sellers = Seller.query.all()
    result = []

    for seller in sellers:
        seller_data = {
            'seller_id': seller.seller_id,
            'seller_name': seller.seller_name,
            'store_name': seller.store_name,
            'store_category': seller.store_category,
            'email': seller.email,
            'phone': seller.phone,
            'governorate': seller.governorate,
            'city': seller.city,
            'village': seller.village,
            'store_image': seller.store_image,
            'owner_image': seller.owner_image,
            'owner_banner': seller.owner_banner,
            'registration_date': seller.registration_date.strftime('%Y-%m-%d %H:%M:%S') if seller.registration_date else None,
            'last_login': seller.last_login.strftime('%Y-%m-%d %H:%M:%S') if seller.last_login else None,
            'status': seller.status,
            'is_seller': seller.is_seller,
            'rating': seller.rating,
            'comment': seller.comment,
            'street_address': seller.street_address,
        }

        # 🔥 إزالة الحقول التي تحتوي على None أو قيم فارغة ("" أو [])
        filtered_data = {key: value for key, value in seller_data.items() if value not in [None, "", []]}

        result.append(filtered_data)

    return jsonify(result)

#===================================  api currnetuser    ===========================================
#===================================  api currnetuser    ===========================================

@app.route('/get_seller', methods=['GET'])
def get_seller():
    email = request.args.get('email')
    seller_id = request.args.get('seller_id')

    if email:
        seller = Seller.query.filter_by(email=email).first()
    elif seller_id:
        seller = Seller.query.filter_by(seller_id=seller_id).first()
    else:
        return jsonify({'error': 'يجب تقديم البريد الإلكتروني أو معرف البائع'}), 400

    if not seller:
        return jsonify({'error': 'البائع غير موجود'}), 404

    seller_data = {
        'seller_id': seller.seller_id,
        'seller_name': seller.seller_name,
        'store_name': seller.store_name,
        'store_category': seller.store_category,
        'email': seller.email,
        'phone': seller.phone,
        'governorate': seller.governorate,
        'city': seller.city,
        'village': seller.village,
        'store_image': seller.store_image,
        'owner_image': seller.owner_image,
        'owner_banner': seller.owner_banner,
        'registration_date': seller.registration_date.strftime('%Y-%m-%d %H:%M:%S') if seller.registration_date else None,
        'last_login': seller.last_login.strftime('%Y-%m-%d %H:%M:%S') if seller.last_login else None,
        'status': seller.status,
        'is_seller': seller.is_seller,
        'rating': seller.rating,
        'comment': seller.comment,
        'street_address': seller.street_address,
    }

    # 🔥 إزالة الحقول التي تحتوي على None أو قيم فارغة ("" أو [])
    filtered_data = {key: value for key, value in seller_data.items() if value not in [None, "", []]}

    return jsonify(filtered_data)




@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'product_id': product.product_id,
        'product_name': product.product_name,
        'price': product.price,
        'stock_quantity': product.stock_quantity,
        'seller_id': product.seller_id
    } for product in products])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    new_order = Order(
        customer_name=data['customer_name'],
        phone=data['phone'],
        total_amount=data['total_amount'],
        payment_method=data['payment_method']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/cart/<int:seller_id>', methods=['GET'])
def get_cart(seller_id):
    cart_items = Cart.query.filter_by(seller_id=seller_id).all()
    return jsonify([{
        'cart_id': item.cart_id,
        'product_id': item.product_id,
        'quantity': item.quantity,
        'total_price': item.total_price
    } for item in cart_items])





@app.route('/api_categories', methods=['GET'])
def get_categories():
    try:
        # جلب الأقسام المفعلة فقط
        categories = Category.query.filter_by(is_active=True).all()
        
        # تحويل البيانات إلى JSON
        categories_list = [
            {
                "category_id": cat.category_id,
                "category_name": cat.category_name,
                "image_category": cat.image_category if cat.image_category else None,
                "is_active": cat.is_active
            }
            for cat in categories
        ]
        
        return jsonify({"success": True, "categories": categories_list}), 200
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    


@app.route('/api_get_products', methods=['GET'])
def api_get_products():
    try:
        products = Product.query.all()
        product_list = []
        for product in products:
            # إنشاء قاموس للمنتج مع إزالة الحقول الفارغة
            product_data = {
                key: value for key, value in {
                    'product_id': product.product_id,
                    'category_id': product.category_id,
                    'seller_id': product.seller_id,
                    'product_name': product.product_name,
                    'description': product.description,
                    'price': product.price,
                    'stock_quantity': product.stock_quantity,
                    'product_category': product.product_category,
                    'status': product.status,
                    'rating': product.rating,
                    'discount': product.discount,
                    'net_profit': product.net_profit,
                    'total_after_commission': product.total_after_commission,
                    'image1': product.image1,
                    'image2': product.image2,
                    'image3': product.image3,
                    'image4': product.image4,
                    'image5': product.image5,
                    'has_active_offer': product.has_active_offer()
                }.items() if value is not None  # إزالة الحقول الفارغة
            }
            product_list.append(product_data)
        return jsonify(product_list), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
        
#=========================================   API_POST    ==============================
#=========================================   API_POST    ==============================
#=========================================   API_POST    ==============================
#=========================================   API_POST    ==============================
#=========================================   API_POST    ==============================
#=========================================   API_POST    ==============================


@app.route('/api_signup', methods=['POST'])
def api_signup():
    try:
        data = request.get_json()

        # التحقق من البيانات المطلوبة
        required_fields = ['seller_name', 'email', 'phone', 'governorate', 'city', 'password']
        if not all(field in data and data[field] for field in required_fields):
            return jsonify({"message": "يرجى ملء جميع الحقول المطلوبة!"}), 400

        # التحقق من صحة البريد الإلكتروني
        if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
            return jsonify({"message": "البريد الإلكتروني غير صالح!"}), 400

        # التحقق من صحة رقم الهاتف
        if not re.match(r"^01[0-2]{1}[0-9]{8}$", data['phone']):
            return jsonify({"message": "رقم الهاتف غير صالح!"}), 400

        # التحقق من وجود المستخدم مسبقًا
        if Seller.query.filter_by(email=data['email']).first():
            return jsonify({"message": "هذا البريد الإلكتروني مسجل بالفعل!"}), 409

        # تشفير كلمة المرور
        hashed_password = generate_password_hash(data['password'])

        # إنشاء مستخدم جديد
        new_seller = Seller(
            seller_name=data['seller_name'],
            email=data['email'],
            phone=data['phone'],
            governorate=data['governorate'],
            city=data['city'],
            village=data.get('village', ''),
            street_address=data.get('street_address', ''),
            password=hashed_password,
        )

        db.session.add(new_seller)
        db.session.commit()

        # تسجيل الدخول للمستخدم الجديد
        login_user(new_seller)

        # إنشاء JWT Token
        access_token = create_access_token(identity=new_seller.seller_id)

        return jsonify({
            "message": f"مرحباً {new_seller.seller_name}، تم تسجيل حسابك بنجاح!",
            "token": access_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "حدث خطأ أثناء إنشاء الحساب. حاول مرة أخرى لاحقاً."}), 500

        
#==========================================   api_login     ============================
#==========================================   api_login     ============================


@app.route('/api_login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Seller.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.seller_id)
        return jsonify({"message": "تم تسجيل الدخول بنجاح!", "token": access_token}), 200
    else:
        return jsonify({"message": "البريد الإلكتروني أو كلمة المرور غير صحيحة!"}), 401
