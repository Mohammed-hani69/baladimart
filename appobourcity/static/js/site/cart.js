function updateQuantity(action, cartId) {
    var quantityInput = document.getElementById('product-quantity-' + cartId);
    var totalPriceElement = document.getElementById('total-price-' + cartId); 
    var originalPriceElement = document.getElementById('original-price-' + cartId); 
    var totalAmountElement = document.getElementById('total-amount'); 
    var totalDiscountElement = document.getElementById('total-discounts'); 
    var totalAfterDiscountElement = document.getElementById('total-after-discount'); 

    var currentQuantity = parseInt(quantityInput.value);
    var newQuantity = action === 'increase' ? currentQuantity + 1 : currentQuantity - 1;

    if (newQuantity < 1) {
        alert("الكمية لا يمكن أن تكون أقل من 1.");
        return;
    }

    fetch('/update-quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            cart_id: cartId,
            quantity: newQuantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // تحديث الكمية في الواجهة
            quantityInput.value = newQuantity;

            // تحديث السعر بناءً على البيانات المحدثة
            if (data.updated_price) {
                totalPriceElement.innerText = `${(data.updated_price).toFixed(2)} `;
            }

            if (data.total_after_discount) {
                totalAfterDiscountElement.innerText = `${(data.total_after_discount).toFixed(2)}`;
            }

            if (data.original_price) {
                originalPriceElement.innerText = `${(data.original_price).toFixed(2)}`;
            }

            if (data.total_old_price) {
                totalAmountElement.innerText = `${(data.total_old_price).toFixed(2)}`;
            }

            if (data.total_discounts) {
                totalDiscountElement.innerText = `${(data.total_discounts).toFixed(2)}`;
            }
        } else {
            alert(data.message);
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    // إضافة مستمع الحدث عند تحميل الصفحة
    const completeOrderButton = document.querySelector("#complete-order-button");

    // تحقق من وجود الزر قبل إضافة مستمع الحدث
    if (completeOrderButton) {
        completeOrderButton.addEventListener("click", getLocation);
    } else {
        console.error("لم يتم العثور على زر إتمام الطلب");
    }
});

function getLocation() {
    const statusElement = document.getElementById("location-status");
    const loadingIndicator = document.getElementById("loading-indicator");

    // إظهار علامة التحميل
    if (loadingIndicator) loadingIndicator.style.display = "block";

    // التحقق من دعم المتصفح لخدمة الموقع
    if (!navigator.geolocation) {
        statusElement.innerText = "الموقع الجغرافي غير مدعوم في متصفحك.";
        if (loadingIndicator) loadingIndicator.style.display = "none"; // إخفاء علامة التحميل
        return;
    }

    // جلب الموقع الجغرافي
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            // إرسال الموقع والبيانات الأخرى إلى الخادم
            saveOrderDataToServer(latitude, longitude);
        },
        (error) => {
            if (loadingIndicator) loadingIndicator.style.display = "none"; // إخفاء علامة التحميل

            switch (error.code) {
                case error.PERMISSION_DENIED:
                    statusElement.innerText = "تم رفض إذن الوصول إلى الموقع.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    statusElement.innerText = "الموقع غير متاح.";
                    break;
                case error.TIMEOUT:
                    statusElement.innerText = "انتهت مهلة الحصول على الموقع.";
                    break;
                default:
                    statusElement.innerText = "حدث خطأ غير متوقع.";
            }
        }
    );
}

function saveOrderDataToServer(latitude, longitude) {
    const statusElement = document.getElementById("location-status");
    const loadingIndicator = document.getElementById("loading-indicator");

    const paymentMethod = document.getElementById("payment-method").value;

    const totalAfterDiscountElement = document.getElementById("total-after-discount");
    const totalAfterDiscount = totalAfterDiscountElement ? totalAfterDiscountElement.innerText.trim() : null;

    if (!latitude || !longitude || !paymentMethod || !totalAfterDiscount || isNaN(totalAfterDiscount)) {
        if (loadingIndicator) loadingIndicator.style.display = "none"; // إخفاء علامة التحميل
        alert(`البيانات غير مكتملة أو غير صحيحة.`);
        return;
    }

    const orderData = {
        latitude: latitude,
        longitude: longitude,
        payment_method: paymentMethod,
        total_after_discount: totalAfterDiscount,
    };

    // إظهار علامة التحميل
    if (loadingIndicator) loadingIndicator.style.display = "block";

    // تعيين مهلة لمدة 10 ثواني
    const timeoutId = setTimeout(() => {
        if (loadingIndicator) loadingIndicator.style.display = "none";
        alert("الاتصال بالإنترنت ضعيف أو لا يوجد اتصال");
    }, 6000); // 10 ثواني

    // إرسال البيانات إلى الخادم
    fetch("/complete-order-with-location", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderData),
    })
    .then((response) => response.json())
    .then((data) => {
        clearTimeout(timeoutId); // إلغاء المهلة إذا استجاب الخادم قبل الوقت المحدد
        if (loadingIndicator) loadingIndicator.style.display = "none"; // إخفاء علامة التحميل

        console.log("Response data:", data); // تأكيد البيانات المستلمة
        if (data.success) {
            setTimeout(() => {
                if (paymentMethod === "cod") {
                    // توجيه إلى صفحة "طلباتي"
                    window.location.href = '/my-orders';
                } else if (paymentMethod === "online") {
                    // توجيه إلى صفحة "الدفع"
                    window.location.href = '/my-orders';
                } else {
                    alert("طريقة الدفع غير معروفة.");
                }
            }, 3000); // انتظار لمدة ثانية قبل التوجيه
        } else {
            alert(`خطأ: ${data.message}`);
        }
    })
    .catch((error) => {
        clearTimeout(timeoutId); // إلغاء المهلة في حالة حدوث خطأ
        if (loadingIndicator) loadingIndicator.style.display = "none"; // إخفاء علامة التحميل
        alert("حدث خطأ أثناء الاتصال بالخادم. الرجاء المحاولة لاحقًا.");
    });
}


// دالة لإظهار النافذة المنبثقة وإخفائها بعد ثانيتين
function showPopup(popupId) {
    console.log("محاولة إظهار النافذة: " + popupId); // فحص
    const popup = document.getElementById(popupId);
    if (popup) {
        popup.classList.add('visible');
        setTimeout(function() {
            popup.classList.remove('visible');
        }, 2000);
    } else {
        console.error("لم يتم العثور على النافذة: " + popupId); // فحص
    }
}

// تشغيل الدالة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // افترض أن cart_item.cart_id متاح في السياق
    const popupId = 'popup-{{ cart_item.cart_id }}';
    showPopup(popupId);
});


function updateCartTotals() {
    fetch('/update-cart-totals', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            // تحديث العناصر في DOM
            document.getElementById('total-amount').innerText = data.total_old_price.toFixed(2);
            document.getElementById('total-discounts').innerText = data.total_discounts.toFixed(2);
            document.getElementById('total-after-discount').innerText = data.total_after_discount.toFixed(2);
        })
        .catch(error => console.error('Error updating cart totals:', error));
}

// استدعاء الدالة تلقائيًا كل 5 ثوانٍ
setInterval(updateCartTotals, 1000);


// تحديث الإجماليات العامة للصفحة
function updateCartTotals() {
    fetch('/update-cart-totals', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            // تحديث الإجماليات في DOM
            document.getElementById('total-amount').innerText = data.total_old_price.toFixed(2);
            document.getElementById('total-discounts').innerText = data.total_discounts.toFixed(2);
            document.getElementById('total-after-discount').innerText = data.total_after_discount.toFixed(2);
        })
        .catch(error => console.error('Error updating cart totals:', error));
}