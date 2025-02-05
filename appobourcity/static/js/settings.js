// تبديل اللغة
document.getElementById('language-toggle').addEventListener('click', function() {
    let currentLang = document.documentElement.lang;
    if (currentLang === "ar") {
        document.documentElement.lang = "en";
        // تغيير النصوص أو الترجمة حسب اللغة
    } else {
        document.documentElement.lang = "ar";
        // تغيير النصوص أو الترجمة حسب اللغة
    }
});

// تبديل وضع الظلام
const themeToggle = document.getElementById('theme-toggle');
themeToggle.addEventListener('change', function() {
    if (themeToggle.checked) {
        document.body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    } else {
        document.body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    }
});

// استعادة وضع الظلام من التخزين المحلي
window.addEventListener('load', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggle.checked = true;
    } else {
        document.body.classList.remove('dark-theme');
        themeToggle.checked = false;
    }
});


document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".settings-form");
    const submitButton = form.querySelector(".submit-button");
    
    form.addEventListener("submit", function (e) {
        // منع إرسال النموذج حتى يتم التحقق من البيانات
        e.preventDefault();
        
        // مسح أي رسائل خطأ سابقة
        const errorMessages = form.querySelectorAll(".error-message");
        errorMessages.forEach(msg => msg.remove());

        let isValid = true;

        // التحقق من الحقول
        const requiredFields = form.querySelectorAll("input, select");
        requiredFields.forEach(function (input) {
            if (!input.value.trim()) {
                isValid = false;
                const errorMessage = document.createElement("div");
                errorMessage.classList.add("error-message");
                errorMessage.textContent = `${input.previousElementSibling.textContent} هو حقل مطلوب`;
                input.parentElement.appendChild(errorMessage);
            }
        });

        // إذا كانت جميع الحقول مكتملة، يتم إرسال النموذج
        if (isValid) {
            form.submit();
        }
    });
});
