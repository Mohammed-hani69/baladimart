

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



document.addEventListener("DOMContentLoaded", function () {
    // استمع لجميع الأزرار التي تفتح المودال
    const editButtons = document.querySelectorAll("[data-bs-toggle='modal'][data-bs-target='#editOfferModal']");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // اجلب قيم البيانات من الزر
            const offerId = button.getAttribute("data-id");
            const name = button.getAttribute("data-name");
            const discountValue = button.getAttribute("data-discount");
            const typename = button.getAttribute("data-typename");
            const code = button.getAttribute("data-code");
            const startDate = button.getAttribute("data-start");
            const endDate = button.getAttribute("data-end");
            const description = button.getAttribute("data-description");
            const image = button.getAttribute("data-image");
            const products = button.getAttribute("data-products");

            // ضع القيم في الحقول داخل المودال
            document.getElementById("offer_id").value = offerId;
            document.getElementById("name_edit").value = name;
            document.getElementById("discount_value_edit").value = discountValue;
            document.getElementById("typename_edit").value = typename;
            document.getElementById("code_edit").value = code;
            document.getElementById("start_date_edit").value = startDate;
            document.getElementById("end_date_edit").value = endDate;
            document.getElementById("description_edit").value = description;
            document.getElementById("image_edit").value = image;

            // في حالة أن المنتجات تحتاج معالجة إضافية
            const productsField = document.querySelector("#editOfferModal #products");
            if (productsField && products) {
                productsField.value = products.split(",").map(product => product.trim()).join(", ");
            }
        });
    });
});
