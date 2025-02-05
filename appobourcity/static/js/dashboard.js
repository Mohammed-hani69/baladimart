// تفعيل الرابط النشط في الشريط الجانبي
const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        });
        li.classList.add('active');
    });
});

// تفعيل إظهار وإخفاء الشريط الجانبي عند النقر على قائمة القائمة
const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

// تفعيل زر البحث
const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault();
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

// إعادة تعيين الشريط الجانبي وزر البحث عند تغيير حجم النافذة
window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

// تفعيل الوضع الليلي
const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    document.body.classList.toggle('dark', this.checked);
});

// وظائف تعديل معلومات المستخدم
function editUserInfo() {
    document.getElementById('editUserModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editUserModal').style.display = 'none';
}

function previewProfilePic(event) {
    const img = document.getElementById('user-profile-pic');
    img.src = URL.createObjectURL(event.target.files[0]);
}

function saveUserInfo() {
    const newUsername = document.getElementById('edit-username').value;
    const newPassword = document.getElementById('edit-password').value;

    if (newUsername) {
        document.getElementById('username').textContent = newUsername;
        localStorage.setItem('username', newUsername); // حفظ اسم المستخدم في localStorage
    }

    if (newPassword) {
        document.getElementById('password').textContent = '********'; // لتأمين كلمة المرور
        localStorage.setItem('password', newPassword); // حفظ كلمة المرور في localStorage
    }

    closeEditModal();
    alert('User info updated successfully!');
}

// وظيفة تبديل حالة البائع
function toggleSellerStatus(checkbox) {
    const status = checkbox.checked ? "Activated" : "Deactivated";
    console.log(`Seller status changed to: ${status}`);
}

// تحديد العناصر
const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;
const welcomeHeading = document.querySelector('.welcome-user h2');
const recentOrdersHeading = document.querySelector('.recent-orders h2');
const sellerInfoHeading = document.querySelector('.seller-info h2');

// نصوص اللغة
const texts = {
    en: {
        welcome: "Welcome, User!",
        recentOrders: "Recent Orders",
        sellerInfo: "Seller Information",
        editUsername: "Edit Username",
        editPassword: "Edit Password",
        save: "Save",
        status: "Status"
    },
    ar: {
        welcome: "أهلاً بك، المستخدم!",
        recentOrders: "الطلبات الأخيرة",
        sellerInfo: "معلومات البائع",
        editUsername: "تعديل اسم المستخدم",
        editPassword: "تعديل كلمة المرور",
        save: "حفظ",
        status: "الحالة"
    }
};

// تغيير النصوص
function changeLanguage(lang) {
    welcomeHeading.textContent = texts[lang].welcome;
    recentOrdersHeading.textContent = texts[lang].recentOrders;
    sellerInfoHeading.textContent = texts[lang].sellerInfo;
}

// إضافة حدث لتغيير اللغة
document.getElementById('languageToggle').addEventListener('change', (event) => {
    const selectedLanguage = event.target.value; // "en" أو "ar"
    changeLanguage(selectedLanguage);
});

// إعدادات أولية
changeLanguage('ar'); // تعيين اللغة الافتراضية

// عرض النافذة المنبثقة
function showPopup() {
    document.getElementById('editPopup').style.display = 'flex';
}

// إغلاق النافذة المنبثقة
function closePopup() {
    document.getElementById('editPopup').style.display = 'none';
}

// تحديث معلومات المستخدم
function updateUserInfo(event) {
    event.preventDefault(); // منع تقديم النموذج بشكل افتراضي

    const profilePicInput = document.getElementById('profilePic');
    const newUsername = document.getElementById('newUsername').value;
    const newPassword = document.getElementById('newPassword').value;

    // تحديث اسم المستخدم
    if (newUsername) {
        document.getElementById('username').textContent = newUsername;
        localStorage.setItem('username', newUsername); // حفظ الاسم الجديد
    }

    // تحديث الصورة
    if (profilePicInput.files && profilePicInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('user-profile-pic').src = e.target.result; // تعيين المصدر للصورة
            localStorage.setItem('profilePic', e.target.result); // حفظ الصورة في localStorage
        };
        reader.readAsDataURL(profilePicInput.files[0]); // قراءة الصورة
    }

    // حفظ كلمة المرور في localStorage إذا لزم الأمر
    if (newPassword) {
        localStorage.setItem('password', newPassword);
    }

    alert('User info updated successfully!');
    closePopup(); // إغلاق النافذة المنبثقة بعد الحفظ
}

// Close popup when clicking outside of it
window.onclick = function (event) {
    const popup = document.getElementById('editPopup');
    if (event.target == popup) {
        closePopup();
    }
};

// عند تحميل الصفحة، استرجع البيانات من localStorage
document.addEventListener('DOMContentLoaded', () => {
    const savedUsername = localStorage.getItem('username');
    const savedPassword = localStorage.getItem('password');
    const savedProfilePic = localStorage.getItem('profilePic');

    if (savedUsername) {
        document.getElementById('username').textContent = savedUsername;
        document.getElementById('newUsername').value = savedUsername; // لملء حقل الاسم
    }

    if (savedPassword) {
        document.getElementById('newPassword').value = savedPassword; // لملء حقل كلمة المرور
    }

    if (savedProfilePic) {
        document.getElementById('user-profile-pic').src = savedProfilePic; // تعيين الصورة المحفوظة
    }
});
function toggleSellerStatus(checkbox) {
    if (checkbox.checked) {
        console.log("البائع مفعل");
    } else {
        console.log("البائع معطل");
    }
}
var animation = bodymovin.loadAnimation({
    container: document.getElementById('lottie-animation'), // العنصر الذي سيتم تحميل الرسوم المتحركة فيه
    path: 'path/to/your-animation.json', // مسار ملف الرسوم المتحركة
    renderer: 'svg',
    loop: true,
    autoplay: true,
});
document.addEventListener('DOMContentLoaded', () => {
    const notifBtn = document.getElementById('notif-btn');
    const notifModal = document.getElementById('notif-modal');
    const closeBtn = document.querySelector('.close-btn');

    // عرض نموذج الإشعارات عند الضغط على الزر
    notifBtn.onclick = function () {
        notifModal.style.display = 'block';
    };

    // إغلاق نموذج الإشعارات عند الضغط على زر الإغلاق
    closeBtn.onclick = function () {
        notifModal.style.display = 'none';
    };

    // إغلاق النموذج عند الضغط خارج المحتوى
    window.onclick = function (event) {
        if (event.target == notifModal) {
            notifModal.style.display = 'none';
        }
    };
});


        // التحقق من حالة تسجيل الدخول
        if (sessionStorage.getItem('loggedIn') !== 'true') {
            // إذا لم يكن المستخدم مسجلاً الدخول، يتم توجيهه إلى صفحة تسجيل الدخول
            window.location.href = 'admin.html';
        }

        // تسجيل الخروج
        document.getElementById('logoutButton').addEventListener('click', function() {
            // إزالة حالة تسجيل الدخول من الجلسة
            sessionStorage.removeItem('loggedIn');
            // إعادة توجيه المستخدم إلى صفحة تسجيل الدخول
            window.location.href = 'admin.html';
        });
        document.addEventListener("DOMContentLoaded", function () {
            const notificationButton = document.getElementById("notificationButton");
            const notificationList = document.getElementById("notificationList");
        
            notificationButton.addEventListener("click", function() {
                notificationList.classList.toggle("show");
            });
        
            // إغلاق قائمة الإشعارات إذا تم النقر خارجها
            document.addEventListener("click", function(event) {
                if (!notificationButton.contains(event.target) && !notificationList.contains(event.target)) {
                    notificationList.classList.remove("show");
                }
            });
        });
        // إضافة أو إزالة فئة "collapsed" عند الضغط على أيقونة القائمة
document.querySelector('.bx-menu').addEventListener('click', function() {
    document.querySelector('.sidebar').classList.toggle('collapsed');
});
