// تحديث حالة الطلب
function updateOrderStatus(selectElement, orderId) {
    const newStatus = selectElement.value;
    const orderRow = document.querySelector(`.order-row[data-order-id='${orderId}']`);
    const statusSpan = orderRow.querySelector('.status');

    // تحديث الحالة في واجهة المستخدم
    if (newStatus === 'completed') {
        statusSpan.textContent = 'مكتمل';
        statusSpan.classList.remove('pending', 'failed', 'canceled');
        statusSpan.classList.add('completed');
    } else if (newStatus === 'pending') {
        statusSpan.textContent = 'قيد الانتظار';
        statusSpan.classList.remove('completed', 'failed', 'canceled');
        statusSpan.classList.add('pending');
    } else if (newStatus === 'failed') {
        statusSpan.textContent = 'فاشل';
        statusSpan.classList.remove('completed', 'pending', 'canceled');
        statusSpan.classList.add('failed');
    } else if (newStatus === 'canceled') {
        statusSpan.textContent = 'ملغي';
        statusSpan.classList.remove('completed', 'pending', 'failed');
        statusSpan.classList.add('canceled');
    }
}

// طباعة الفاتورة
function printInvoice(orderId) {
    const orderRow = document.querySelector(`.order-row[data-order-id='${orderId}']`);
    const customerName = orderRow.querySelector('td:nth-child(1)').textContent;
    const orderDate = orderRow.querySelector('td:nth-child(2)').textContent;
    const totalAmount = orderRow.querySelector('td:nth-child(3)').textContent;
    const paymentMethod = orderRow.querySelector('td:nth-child(5)').textContent;
    const paymentStatus = orderRow.querySelector('td:nth-child(6)').textContent;

    // إنشاء محتوى الفاتورة
    const invoiceContent = `
        <h1>فاتورة الطلب</h1>
        <p><strong>اسم العميل:</strong> ${customerName}</p>
        <p><strong>تاريخ الطلب:</strong> ${orderDate}</p>
        <p><strong>المبلغ الإجمالي:</strong> ${totalAmount}</p>
        <p><strong>طريقة الدفع:</strong> ${paymentMethod}</p>
        <p><strong>حالة الدفع:</strong> ${paymentStatus}</p>
    `;
    
    // فتح نافذة للطباعة
    const printWindow = window.open('', '_blank', 'width=800,height=600');
    printWindow.document.write(`<html><body>${invoiceContent}</body></html>`);
    printWindow.document.close();
    printWindow.print();
}

// حذف الطلب
function deleteOrder(orderId) {
    const orderRow = document.querySelector(`.order-row[data-order-id='${orderId}']`);
    orderRow.remove();
}

// تصفية الطلبات بناءً على الحالة
function filterOrders(status) {
    const rows = document.querySelectorAll('.orders-table tbody tr');
    rows.forEach(row => {
        if (status === 'all') {
            row.style.display = '';
        } else {
            const orderStatus = row.getAttribute('data-status');
            if (orderStatus === status) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    });
}

