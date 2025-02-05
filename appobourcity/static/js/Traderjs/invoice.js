    // دالة لطباعة الفاتورة
    function printInvoice() {
        window.print();
    }

    // دالة للرجوع إلى صفحة الطلبات
    function goBackToOrders() {
        window.location.href = "orders.html"; // ضع الرابط المناسب لصفحة الطلبات
    }

    function printInvoice() {
        window.print();
        setTimeout(() => {
            window.location.href = "orders.html"; // عدّل الرابط لصفحة الطلبات
        }, 500); // مهلة قصيرة لضمان انتهاء عملية الطباعة
    }
    