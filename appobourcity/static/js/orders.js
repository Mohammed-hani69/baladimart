

function filterOrders(status) {
    const rows = document.querySelectorAll(".order-row"); // اختيار كل الصفوف ذات الطلبات
    
    rows.forEach(row => {
        // عرض الصف إذا كان مطابقًا للحالة أو إذا كانت الحالة "الكل"
        if (status === "all" || row.getAttribute("data-status") === status) {
            row.style.display = ""; // عرض الصف
        } else {
            row.style.display = "none"; // إخفاء الصف
        }
    });
}



function updatePaymentStatus(orderId, status) {
    // تحويل حالة "paid" و"unpaid" إلى Boolean
    const paymentStatus = status === "paid";

    fetch('/update-payment-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            order_id: orderId,
            payment_status: paymentStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('تم تحديث حالة الدفع بنجاح');
        } else {
            console.error('حدث خطأ أثناء تحديث حالة الدفع:', data.message);
        }
    })
    .catch(error => console.error('حدث خطأ:', error));
}


function updateOrderStatus(orderId, status) {
    fetch('/update-order-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            order_id: orderId,
            order_status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('تم تحديث حالة الطلب بنجاح');
        } else {
            console.error('حدث خطأ أثناء تحديث حالة الطلب');
        }
    })
    .catch(error => console.error('حدث خطأ:', error));
}
