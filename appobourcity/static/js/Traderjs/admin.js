 // إظهار الرسالة الفلاش ثم إخفائها بعد 5 ثوانٍ
 window.onload = function() {
    const flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.display = "block"; // إظهار الرسالة
        setTimeout(() => {
            flashMessage.classList.add('hide'); // إضافة الفئة لإخفائها
        }, 5000); // إخفاء الرسالة بعد 5 ثوانٍ
    }
}