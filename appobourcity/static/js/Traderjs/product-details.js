document.addEventListener('DOMContentLoaded', () => {
    const printButton = document.getElementById('print-invoice');
    const whatsappButton = document.getElementById('share-location');
    const toggleSwitch = document.getElementById('toggle-mode');

    // حدث طباعة التفاصيل
    printButton.addEventListener("click", function () {
        // العناصر التي سيتم إخفاؤها أثناء الطباعة
        const sidebar = document.querySelector(".sidebar");
        const navbar = document.querySelector("nav");
        const productDetailsContainer = document.querySelector(".product-details-container");
        const actions = document.querySelector(".actions");  // يحتوي على الأزرار مثل طباعة ومشاركة
        const productBox = document.querySelectorAll(".order-box");  // الصناديق التي تحتوي على تفاصيل المنتج، البائع، والتقييمات
        const printButton = document.getElementById("print-invoice");
        const shareButton = document.getElementById("share-location");

        // إخفاء العناصر غير المهمة
        sidebar.style.display = "none";
        navbar.style.display = "none";
        actions.style.display = "none"; // إخفاء الأزرار
        productBox.forEach(box => {
            box.style.display = "block";  // التأكد من أن كافة التفاصيل الظاهرة سيتم طباعتها
        });

        // طباعة المحتوى الحالي
        window.print();

        // إعادة إظهار العناصر بعد الطباعة
        sidebar.style.display = "block";
        navbar.style.display = "flex";
        actions.style.display = "block";  // إظهار الأزرار مرة أخرى
        productBox.forEach(box => {
            box.style.display = "block"; // إظهار كافة الصناديق بعد الطباعة
        });
    });

    // وظيفة لمشاركة الموقع عبر WhatsApp
    whatsappButton.addEventListener('click', () => {
        const productName = "أحذية أبو دويـل";  // اسم المنتج
        const totalPrice = "750.00 ج.م";  // السعر
        const orderNumber = "PRD123456";  // رمز التعريف
        const deliveryAddress = "شارع الحداد، العبور";  // عنوان التسليم

        const orderDetails = `
            رقم الطلب: ${orderNumber}
            المنتج: ${productName}
            السعر الإجمالي: ${totalPrice}
            عنوان التسليم: ${deliveryAddress}
        `;
        
        const message = encodeURIComponent(orderDetails); // تشفير الرسالة
        const whatsappUrl = `https://api.whatsapp.com/send?text=${message}`; // رابط WhatsApp

        window.open(whatsappUrl, '_blank'); // فتح الرابط في نافذة جديدة
    });

    // وظيفة التبديل بين الوضعين الداكن والفاتح
    toggleSwitch.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode');
    });
});
