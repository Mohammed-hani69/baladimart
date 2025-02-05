function markAsRead(notificationId, button) {
    // إرسال طلب إلى الخادم لتحديث حالة القراءة
    fetch(`/mark_as_read/${notificationId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // إذا كنت تستخدم Flask مع CSRF
        }
    })
    .then(response => {
        if (response.ok) {
            // تحديث واجهة المستخدم
            button.parentElement.innerHTML = '<span style="color: green; font-weight: bold;">تم القراءة</span>';
        } else {
            console.error('Failed to mark notification as read');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}







function showNotificationDetails(notification) {
    // تفاصيل الإشعار
    const detailsHtml = `
        <p><strong>رقم الإشعار:</strong> ${notification.notification_id}</p>
        <p><strong>العنوان:</strong> ${notification.title}</p>
        <p><strong>الرسالة:</strong> ${notification.message}</p>
        <p><strong>تاريخ الإنشاء:</strong> ${notification.created_at}</p>
        <p><strong>حالة القراءة:</strong> ${notification.read_status === 0 ? 'لم يتم القراءة' : 'تمت القراءة'}</p>
    `;
    document.getElementById('notificationDetails').innerHTML = detailsHtml;

    // إظهار النموذج
    const modal = document.getElementById('notificationModal');
    modal.style.top = '50%';
    modal.style.display = 'block';
    document.getElementById('modalOverlay').style.display = 'block';

    // إنشاء قصاصات ورقية
    for (let i = 0; i < 20; i++) {
        const confetti = document.createElement('div');
        confetti.classList.add('confetti');
        confetti.style.setProperty('--confetti-color', getRandomColor());
        confetti.style.left = Math.random() * 100 + 'vw';
        document.body.appendChild(confetti);

        // إزالة القصاصات بعد نهاية الأنيميشن
        setTimeout(() => confetti.remove(), 2000);
    }
}

function closeModal() {
    const modal = document.getElementById('notificationModal');
    modal.style.top = '-100%';
    setTimeout(() => modal.style.display = 'none', 500); // تأخير الإخفاء
    document.getElementById('modalOverlay').style.display = 'none';
}

function getRandomColor() {
    const colors = ['#ffcc00', '#ff5733', '#33ff57', '#3357ff', '#ff33a1'];
    return colors[Math.floor(Math.random() * colors.length)];
}



// أسماء الأشهر باللغة العربية
const months = [
    "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
    "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
];

// دالة لتنسيق التاريخ
function formatDate(dateString) {
    const date = new Date(dateString);

    // استخراج التفاصيل
    const hours = date.getHours();
    const minutes = date.getMinutes().toString().padStart(2, "0");
    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();

    // تحويل الساعة إلى نظام 12 ساعة
    const period = hours >= 12 ? "م" : "ص";
    const formattedHours = hours % 12 || 12; // تحويل 0 إلى 12 في نظام 12 ساعة

    // تجميع التاريخ بالتنسيق المطلوب
    return `${formattedHours}:${minutes} ${period} ${day} ${month} ${year}`;
}

// استهداف جميع العناصر التي تحتوي على التاريخ
document.addEventListener("DOMContentLoaded", () => {
    const dateElements = document.querySelectorAll(".formatted-date");

    dateElements.forEach((element) => {
        const originalDate = element.getAttribute("data-date"); // الحصول على التاريخ الأصلي
        const formattedDate = formatDate(originalDate); // تنسيق التاريخ
        element.textContent = formattedDate; // تحديث النص داخل العنصر
    });
});
