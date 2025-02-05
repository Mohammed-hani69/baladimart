document.getElementById("confirm-payment").addEventListener("click", function () {
    const wallet = document.getElementById("wallet").value;
    const phone = document.getElementById("phone").value.trim();
    const errorMessage = document.getElementById("error-message");

    // التحقق من إدخال البيانات
    if (!wallet || !phone || !/^\d{11}$/.test(phone)) {
        errorMessage.style.display = "block";
        errorMessage.textContent = "يرجى إدخال جميع الحقول بشكل صحيح.";
        return;
    }

    errorMessage.style.display = "none";

    // إرسال البيانات إلى الخادم
    fetch("/process-payment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ wallet, phone, amount: 200 }) // تعديل المبلغ حسب الطلب
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("تم الدفع بنجاح! رقم العملية: " + data.transaction_id);
            window.location.href = "/order-summary"; // توجيه إلى صفحة ملخص الطلب
        } else {
            alert("حدث خطأ أثناء الدفع: " + data.message);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("تعذر الاتصال بالخادم.");
    });
});