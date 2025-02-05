
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