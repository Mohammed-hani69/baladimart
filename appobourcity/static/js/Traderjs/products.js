function toggleStatus(productId, status) {
    fetch('/update-product-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}' // إذا كنت تستخدم CSRF للحماية
        },
        body: JSON.stringify({
            product_id: productId,
            status: status
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Status updated successfully");
        } else {
            console.error("Failed to update status:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}

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
    const editButtons = document.querySelectorAll("[data-bs-toggle='modal'][data-bs-target='#editProductModal']");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // اجلب قيم البيانات من الزر
            const productId = button.getAttribute("data-id");
            const productName = button.getAttribute("data-name");
            const description = button.getAttribute("data-description");
            const category = button.getAttribute("data-category");
            const price = button.getAttribute("data-price");
            const discount = button.getAttribute("data-discount");
            const quantity = button.getAttribute("data-quantity");
            const image1 = button.getAttribute("data-imageone");
            const image2 = button.getAttribute("data-imagetwo");
            const image3 = button.getAttribute("data-imagethree");
            const image4 = button.getAttribute("data-imagefour");
            const image5 = button.getAttribute("data-imagefive");

            // ضع القيم في الحقول داخل المودال
            document.getElementById("product_id").value = productId;
            document.getElementById("product_name_edit").value = productName;
            document.getElementById("description_edit").value = description;
            document.getElementById("product_category_edit").value = category;
            document.getElementById("price_edit").value = price;
            document.getElementById("discount_edit").value = discount;
            document.getElementById("stock_quantity_edit").value = quantity;

            // الصور: تعيين القيم للأدوات أو تنظيفها
            document.getElementById("image1_edit").value = image1 || "";
            document.getElementById("image2_edit").value = image2 || "";
            document.getElementById("image3_edit").value = image3 || "";
            document.getElementById("image4_edit").value = image4 || "";
            document.getElementById("image5_edit").value = image5 || "";
        });
    });
});
