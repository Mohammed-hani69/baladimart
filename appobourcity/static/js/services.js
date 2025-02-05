function toggleStatus(serviceId, isChecked) {
    fetch('/toggle_services_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}' // إذا كنت تستخدم CSRF Token
        },
        body: JSON.stringify({
            service_id: serviceId,
            status: isChecked // true أو false
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("تم تحديث الحالة بنجاح");
        } else {
            alert("حدث خطأ أثناء تحديث الحالة.");
        }
    })
    .catch(error => console.error('Error:', error));
}

/*

    // فتح النافذة
    document.getElementById("edit-service-button").addEventListener("click", function(event) {
        event.preventDefault();  // منع الانتقال إلى الرابط
        document.getElementById("editServiceModal").style.display = "block";  // عرض النافذة
    });

    // إغلاق النافذة عند الضغط على زر X
    function closeModal() {
        document.getElementById("editServiceModal").style.display = "none";  // إخفاء النافذة
    }

    // إغلاق النافذة عند النقر خارج المحتوى
    window.onclick = function(event) {
        var modal = document.getElementById("editServiceModal");
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }*/