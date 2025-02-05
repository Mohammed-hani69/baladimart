// تعريف المتغيرات الخاصة بالمنتجات والعروض
const products = document.querySelectorAll('.product-card');
const offers = document.querySelectorAll('.offer-card');
const productsPerPage = 5;  // عدد المنتجات أو العروض في كل مرة
let currentProductIndex = 0;
let currentOfferIndex = 0;

// عرض المنتجات
function displayProducts() {
    products.forEach((product, index) => {
        product.style.display = (index >= currentProductIndex && index < currentProductIndex + productsPerPage) ? 'block' : 'none';
    });
}

// عرض العروض
function displayOffers() {
    offers.forEach((offer, index) => {
        offer.style.display = (index >= currentOfferIndex && index < currentOfferIndex + productsPerPage) ? 'block' : 'none';
    });
}

// التنقل بين المنتجات
function prevProducts() {
    if (currentProductIndex > 0) {
        currentProductIndex -= productsPerPage;
        displayProducts();
    }
}

function nextProducts() {
    if (currentProductIndex + productsPerPage < products.length) {
        currentProductIndex += productsPerPage;
        displayProducts();
    }
}

// التنقل بين العروض
function prevOffers() {
    if (currentOfferIndex > 0) {
        currentOfferIndex -= productsPerPage;
        displayOffers();
    }
}

function nextOffers() {
    if (currentOfferIndex + productsPerPage < offers.length) {
        currentOfferIndex += productsPerPage;
        displayOffers();
    }
}

// إضافة أحداث الأزرار للتنقل بين المنتجات والعروض
document.getElementById('prev-btn-products').addEventListener('click', prevProducts);
document.getElementById('next-btn-products').addEventListener('click', nextProducts);
document.getElementById('prev-btn-offers').addEventListener('click', prevOffers);
document.getElementById('next-btn-offers').addEventListener('click', nextOffers);

// عند تحميل الصفحة، نظهر أول 5 منتجات وأول 5 عروض
window.onload = () => {
    displayProducts();
    displayOffers();
};
