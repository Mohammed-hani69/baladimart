function toggleSettingsMenu() {
    const settingsMenu = document.getElementById('settings-menu');
    settingsMenu.classList.toggle('hidden');
}

function toggleLanguage() {
    const currentLanguage = document.getElementById('language-button').innerText;
    document.getElementById('language-button').innerText = currentLanguage === 'العربية' ? 'English' : 'العربية';
    // يمكنك هنا إضافة الكود لتغيير النصوص إلى اللغة المختارة
}

function toggleTheme() {
    document.body.classList.toggle('dark-theme');
}

//تنسيق رسالة الفلاش 

// إخفاء الرسائل بعد 5 ثوانٍ
setTimeout(() => {
    const flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        flashMessages.style.transition = "opacity 1s ease";
        flashMessages.style.opacity = "0";
        setTimeout(() => flashMessages.remove(), 1000); // إزالة العنصر نهائيًا
    }
}, 5000);

function toggleStatus(seller_id, url) {
    const isChecked = document.getElementById('status-toggle-' + seller_id).checked;
    const newStatus = isChecked;  // الحالة الجديدة بناءً على حالة الـ checkbox

    // إرسال الطلب إلى السيرفر لتحديث الحالة
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            seller_id: seller_id,
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // تحديث النص بعد التبديل
            const label = document.querySelector(`label[for='status-toggle-${seller_id}'] .status-label`);
            if (newStatus) {
                label.innerText = 'نشط';
            } else {
                label.innerText = 'غير نشط';
            }
        } else {
            alert('حدث خطأ أثناء تحديث الحالة.');
            // إعادة حالة الـ switch إلى الحالة الأصلية في حالة حدوث خطأ
            document.getElementById('status-toggle-' + seller_id).checked = !newStatus;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function toggleis_seller(seller_id, url) {
    const isChecked = document.getElementById('is_seller-toggle-' + seller_id).checked;
    const newis_seller = isChecked;  // الحالة الجديدة بناءً على حالة الـ checkbox

    // إرسال الطلب إلى السيرفر لتحديث الحالة
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            seller_id: seller_id,
            is_seller: newis_seller
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // تحديث النص بعد التبديل
            const label = document.querySelector(`label[for='is_seller-toggle-${seller_id}'] .is_seller-label`);
            if (newis_seller) {
                label.innerText = 'نشط';
            } else {
                label.innerText = 'غير نشط';
            }
        } else {
            alert('حدث خطأ أثناء تحديث الحالة.');
            // إعادة حالة الـ switch إلى الحالة الأصلية في حالة حدوث خطأ
            document.getElementById('is_seller-toggle-' + seller_id).checked = !newis_seller;
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('button[data-bs-target="#editSellerModal"]');

    editButtons.forEach(button => {
        button.addEventListener('click', function () {
            // استرداد البيانات من سمات الزر
            const sellerData = {
                id: this.getAttribute('data-id'),
                name: this.getAttribute('data-name'),
                store_name: this.getAttribute('data-store'),
                store_category: this.getAttribute('data-category'),
                email: this.getAttribute('data-email'),
                phone: this.getAttribute('data-phone'),
                address: this.getAttribute('data-address'),
            };

            // استدعاء الدالة لملء نموذج التعديل
            fillEditForm(sellerData);
        });
    });
});

// دالة ملء نموذج التعديل
function fillEditForm(sellerData) {
    const form = document.getElementById('editSellerForm'); // تأكد أن النموذج هو نموذج التعديل
    if (!form) {
        console.error('نموذج التعديل غير موجود');
        return;
    }

    // ملء الحقول في النموذج
    document.getElementById('seller_id').value = sellerData.id;
    document.getElementById('seller_name_edit').value = sellerData.name;
    document.getElementById('store_name_edit').value = sellerData.store_name;
    document.getElementById('store_category_edit').value = sellerData.store_category;
    document.getElementById('email_edit').value = sellerData.email; // البريد الإلكتروني
    document.getElementById('phone_edit').value = sellerData.phone;
    document.getElementById('address_edit').value = sellerData.address;


    // التأكد من أن البريد الإلكتروني غير قابل للتحرير
    document.getElementById('email').setAttribute('readonly', 'readonly');
}
