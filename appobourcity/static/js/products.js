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
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
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
    }

    if (newPassword) {
        document.getElementById('password').textContent = '********'; // لتأمين كلمة المرور
    }

    closeEditModal();
}

// وظيفة تبديل حالة البائع
function toggleSellerStatus(checkbox) {
    if (checkbox.checked) {
        console.log('Seller activated');
    } else {
        console.log('Seller deactivated');
    }
}
function editUserInfo() {
    document.getElementById('editUserModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editUserModal').style.display = 'none';
}

document.addEventListener("DOMContentLoaded", () => {
    const toggleDarkMode = document.querySelector(".dark-mode-toggle");

    toggleDarkMode.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
    });
});



function toggleStatus(productId, status) {
    fetch('/update-product-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}' // إذا كنت تستخدم CSRF للحماية
        },
        body: JSON.stringify({
            product_id: productId,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Status updated successfully");
        } else {
            console.error("Failed to update status:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}