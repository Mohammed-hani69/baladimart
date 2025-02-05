function toggleis_active(id, is_active) {
    fetch('/update-banner-is_active', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}' // تأكد من أنك تستخدم الـ CSRF Token
        },
        body: JSON.stringify({
            banner_id: id,
            is_active: is_active // إرسل حالة الـ checkbox
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("is_active updated successfully");
        } else {
            console.error("Failed to update is_active:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));

    
}



