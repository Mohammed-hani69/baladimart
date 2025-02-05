function processPayment(orderId, totalAmount) {
    // التأكد من صحة البيانات
    if (!orderId || !totalAmount) {
        alert("تفاصيل الطلب غير مكتملة!");
        return;
    }

    // إرسال البيانات إلى الخادم
    fetch("/process-payment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ order_id: orderId, total_amount: totalAmount }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // توجيه المستخدم إلى صفحة تأكيد الدفع
                window.location.href = "/my-orders";
            } else {
                alert(`خطأ: ${data.message}`);
            }
        })
        .catch(error => {
            console.error("حدث خطأ أثناء معالجة الدفع:", error);
            alert("فشل الدفع. حاول مرة أخرى.");
        });
}



function filterOrdersByInvoice() {
    // الحصول على إدخال البحث
    const searchQuery = document.getElementById('searchInvoiceInput').value.toLowerCase().trim();

    // الحصول على جميع الطلبات من الكروت
    const orders = document.querySelectorAll('.order-card');

    // التصفية وإخفاء/إظهار الطلبات بناءً على رقم الفاتورة
    let hasResults = false;
    orders.forEach(order => {
        const orderId = order.querySelector('h5').textContent.toLowerCase();
        if (orderId.includes(searchQuery)) {
            order.style.display = 'block'; // إظهار الطلب
            hasResults = true;
        } else {
            order.style.display = 'none'; // إخفاء الطلب
        }
    });

    // عرض رسالة "لا توجد نتائج" إذا لم يتم العثور على طلبات
    const noResultsMessage = document.getElementById('noResultsMessage');
    if (noResultsMessage) {
        noResultsMessage.style.display = hasResults ? 'none' : 'block';
    }
}
