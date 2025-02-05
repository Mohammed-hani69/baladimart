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