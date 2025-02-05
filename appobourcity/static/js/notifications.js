function showNotificationDetails(notification) {
    const detailsHtml = `
        <p><strong>رقم الإشعار:</strong> ${notification.notification_id}</p>
        <p><strong>العنوان:</strong> ${notification.title}</p>
        <p><strong>الرسالة:</strong> ${notification.message}</p>
        <p><strong>تاريخ الإنشاء:</strong> ${notification.created_at}</p>
    `;
    document.getElementById('notificationDetails').innerHTML = detailsHtml;

    const modal = document.getElementById('notificationModal');
    modal.style.display = 'block';
    document.getElementById('modalOverlay').style.display = 'block';
}

function closeModal() {
    document.getElementById('notificationModal').style.display = 'none';
    document.getElementById('modalOverlay').style.display = 'none';
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
