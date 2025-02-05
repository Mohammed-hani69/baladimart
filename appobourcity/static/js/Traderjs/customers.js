// بيانات العملاء مع التقييمات والتعليقات
let customers = [
    { id: 1, name: 'أحمد محمد', rating: 4.5, comment: 'عميل مميز جدًا، دائمًا يشتري المنتجات عالية الجودة.' },
    { id: 2, name: 'سارة أحمد', rating: 3.2, comment: 'تعليق عادي حول المنتجات، لم تقم بشراء الكثير مؤخرًا.' },
    { id: 3, name: 'محمد علي', rating: 5, comment: 'عميل دائم الشراء ويقدم تعليقات إيجابية باستمرار.' },
    { id: 4, name: 'ليلى جاد', rating: 2.0, comment: 'منتجات غير جيدة، لم أكن راضية عن الجودة.' },
    { id: 5, name: 'محمود عبد الله', rating: 4.0, comment: 'جودة المنتجات جيدة، لكن بعض الأشياء كانت غير متوفرة في المخزن.' },
    { id: 6, name: 'نورا علي', rating: 5.0, comment: 'منتجات رائعة وخدمة عملاء ممتازة.' },
    { id: 7, name: 'سامي حسن', rating: 3.5, comment: 'الخدمة كانت جيدة، لكن البطء في التوصيل كان مزعجًا.' },
    { id: 8, name: 'فاطمة الزهراء', rating: 2.5, comment: 'المنتجات كانت سيئة الجودة ولم تلبِّ توقعاتي.' },
    { id: 9, name: 'عادل رشاد', rating: 4.8, comment: 'منتجات عالية الجودة وخدمة ممتازة.' },
    { id: 10, name: 'خالد عبد الرحمن', rating: 3.0, comment: 'جودة المنتجات جيدة لكن التأخير في التوصيل كان غير مقبول.' },
    { id: 11, name: 'جميلة يوسف', rating: 4.9, comment: 'أعجبتني المنتجات كثيرًا وسأعيد الشراء بالتأكيد.' },
    { id: 12, name: 'محمود سعيد', rating: 3.0, comment: 'منتجات جيدة، لكن أحتاج لمزيد من التنوع في الخيارات.' },
    { id: 13, name: 'رندا حسين', rating: 4.2, comment: 'المنتجات ممتازة، ولكن الأسعار مرتفعة بعض الشيء.' },
    { id: 14, name: 'طارق علي', rating: 1.8, comment: 'منتجات سيئة جدًا، ولن أشتري مجددًا.' },
    { id: 15, name: 'هناء عبد الله', rating: 4.0, comment: 'التسوق كان جيدًا لكن تحتاج الخدمة لتحسين بسيط.' },
    { id: 16, name: 'سامي علي', rating: 2.2, comment: 'منتجات رديئة للغاية ولا أظن أنني سأعيد الشراء.' },
    { id: 17, name: 'ياسمين صلاح', rating: 4.6, comment: 'منتجات رائعة وبأسعار معقولة.' },
    { id: 18, name: 'أحمد محمد', rating: 4.5, comment: 'منتجات رائعة! بالتأكيد سأعود مجددًا.' },
    { id: 19, name: 'سارة أحمد', rating: 3.5, comment: 'الخدمة كانت مقبولة لكن السعر كان مرتفع.' },
    { id: 20, name: 'محمد علي', rating: 4.7, comment: 'جودة عالية جدًا لكن توصيل سريع يمكن أن يتحسن.' }
];

// عرض العملاء في الجدول
function showCustomers() {
    const tbody = document.querySelector('.customers-table tbody');
    tbody.innerHTML = ''; // مسح الجدول قبل إضافة العملاء

    customers.forEach(customer => {
        const row = document.createElement('tr');
        row.classList.add('customer-row');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = customer.name;
        
        const ratingCell = document.createElement('td');
        ratingCell.textContent = `${customer.rating} / 5`;
        
        const commentCell = document.createElement('td');
        commentCell.textContent = customer.comment;
        
        const deleteCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-btn');
        deleteButton.textContent = 'حذف';
        deleteButton.addEventListener('click', () => deleteComment(customer.id));
        
        deleteCell.appendChild(deleteButton);
        
        row.appendChild(nameCell);
        row.appendChild(ratingCell);
        row.appendChild(commentCell);
        row.appendChild(deleteCell);
        
        tbody.appendChild(row);
    });
}

// دالة لتصفية العملاء حسب التقييم
function filterCustomers(rating) {
    let filteredCustomers;

    if (rating === 'all') {
        filteredCustomers = customers; // عرض جميع العملاء
    } else if (rating === 'below3') {
        filteredCustomers = customers.filter(customer => customer.rating < 3);
    } else {
        filteredCustomers = customers.filter(customer => customer.rating == rating);
    }

    // تحديث الجدول بالعملاء المفلترين
    const tbody = document.querySelector('.customers-table tbody');
    tbody.innerHTML = ''; // مسح الجدول قبل إضافة العملاء

    filteredCustomers.forEach(customer => {
        const row = document.createElement('tr');
        row.classList.add('customer-row');
        
        const nameCell = document.createElement('td');
        nameCell.textContent = customer.name;
        
        const ratingCell = document.createElement('td');
        ratingCell.textContent = `${customer.rating} / 5`;
        
        const commentCell = document.createElement('td');
        commentCell.textContent = customer.comment;
        
        const deleteCell = document.createElement('td');
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete-btn');
        deleteButton.textContent = 'حذف';
        deleteButton.addEventListener('click', () => deleteComment(customer.id));
        
        deleteCell.appendChild(deleteButton);
        
        row.appendChild(nameCell);
        row.appendChild(ratingCell);
        row.appendChild(commentCell);
        row.appendChild(deleteCell);
        
        tbody.appendChild(row);
    });
}

// دالة لحذف التعليق
function deleteComment(customerId) {
    // العثور على العميل باستخدام الـ id وحذف التعليق
    const customer = customers.find(c => c.id === customerId);
    if (customer) {
        customer.comment = ''; // حذف التعليق
    }
    showCustomers(); // إعادة عرض العملاء بعد الحذف
}

// استدعاء دالة عرض العملاء عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', showCustomers);
