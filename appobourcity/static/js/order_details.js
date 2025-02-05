document.addEventListener('DOMContentLoaded', () => {
    const printButton = document.getElementById('print-invoice');
    const whatsappButton = document.getElementById('share-location'); // تم تعديل المعرف هنا

document.getElementById("print-invoice").addEventListener("click", function () {
    // Elements to hide during printing
    const sidebar = document.querySelector(".sidebar");
    const navbar = document.querySelector("nav");
    const orderAndShippingInfo = document.querySelectorAll(".order-box")[1];
    const customerInfo = document.querySelectorAll(".order-box")[2];
    const shippingAddress = document.querySelectorAll(".order-box")[3];
    const billingAddress = document.querySelectorAll(".order-box")[4];
    const sellerInfo = document.querySelectorAll(".order-box")[5];
    const printButton = document.getElementById("print-invoice");
    const shareButton = document.getElementById("share-location");

    // Hide elements
    sidebar.style.display = "none";
    navbar.style.display = "none";
    orderAndShippingInfo.style.display = "none";
    shippingAddress.style.display = "none";
    billingAddress.style.display = "none";
    sellerInfo.style.display = "none";
    printButton.style.display = "none";
    shareButton.style.display = "none";

    // Print only the visible content (Order Details)
    window.print();

    // Restore visibility after printing
    sidebar.style.display = "block";
    navbar.style.display = "flex";
    orderAndShippingInfo.style.display = "block";
    customerInfo.style.display = "block";
    shippingAddress.style.display = "block";
    billingAddress.style.display = "block";
    sellerInfo.style.display = "block";
    printButton.style.display = "inline-block";
    shareButton.style.display = "inline-block";
});


    // وظيفة لمشاركة الموقع عبر WhatsApp
    whatsappButton.addEventListener('click', () => {
        const orderDetails = `
            Order Number: 100098
            Product: Abu Doyl Shoes
            Total Price: 7,000.00 EGP
            Delivery Address: Al-Haddad Street, Obour
        `;
        
        const message = encodeURIComponent(orderDetails); // تشفير الرسالة
        const whatsappUrl = `https://api.whatsapp.com/send?text=${message}`; // رابط WhatsApp

        window.open(whatsappUrl, '_blank'); // فتح الرابط في نافذة جديدة
    });
});
const toggleSwitch = document.getElementById('toggle-mode');

toggleSwitch.addEventListener('change', () => {
    document.body.classList.toggle('dark-mode');
});
