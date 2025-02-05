



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



 // تحديث قائمة المدن بناءً على المحافظة
 document.getElementById('governorate').addEventListener('change', function () {
    const governorate = this.value;
    fetch('/get_cities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ governorate: governorate })
    })
    .then(response => response.json())
    .then(cities => {
        const citySelect = document.getElementById('city');
        citySelect.innerHTML = '<option value="" disabled selected>اختر المدينة</option>';
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
    });
});

// تحديث قائمة الأحياء بناءً على المدينة
document.getElementById('city').addEventListener('change', function () {
    const governorate = document.getElementById('governorate').value;
    const city = this.value;
    fetch('/get_villages', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ governorate: governorate, city: city })
    })
    .then(response => response.json())
    .then(villages => {
        const villageSelect = document.getElementById('village');
        villageSelect.innerHTML = '<option value="" disabled selected>اختر الحي</option>';
        villages.forEach(village => {
            const option = document.createElement('option');
            option.value = village;
            option.textContent = village;
            villageSelect.appendChild(option);
        });
    });
});