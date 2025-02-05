document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('editButton');
    const saveButton = document.getElementById('saveButton');
    const infoGrid = document.getElementById('infoGrid');

    // عند الضغط على زر "تعديل"
    editButton.addEventListener('click', function () {
        const infoValues = infoGrid.querySelectorAll('.info-value');
        infoValues.forEach(valueElement => {
            const text = valueElement.textContent.trim();
            const key = valueElement.getAttribute('data-key');

            // تحويل النص إلى حقل إدخال
            valueElement.innerHTML = `<input type="text" name="${key}" value="${text}" class="edit-input">`;
        });

        // إظهار زر الحفظ وإخفاء زر التعديل
        saveButton.style.display = 'block';
        editButton.style.display = 'none';
    });

    // عند الضغط على زر "حفظ"
    saveButton.addEventListener('click', function () {
        const infoInputs = infoGrid.querySelectorAll('.edit-input');
        const updatedData = {};

        // جمع البيانات المعدلة
        infoInputs.forEach(input => {
            updatedData[input.name] = input.value;
        });

        // إرسال البيانات إلى الخادم
        fetch('/update_seller_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedData),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {

                    // تحديث القيم وإزالة حقول الإدخال
                    infoInputs.forEach(input => {
                        const parent = input.parentElement;
                        parent.textContent = input.value;
                    });

                    // إظهار زر التعديل وإخفاء زر الحفظ
                    saveButton.style.display = 'none';
                    editButton.style.display = 'block';
                } else {
                    alert('حدث خطأ أثناء تحديث البيانات.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('تعذر تحديث البيانات.');
            });
    });
});


document.querySelectorAll('.info-value[onlyread]').forEach(element => {
    element.addEventListener('keydown', (e) => e.preventDefault()); // منع إدخال النص
    element.addEventListener('input', (e) => e.preventDefault()); // منع تحرير النص
});
