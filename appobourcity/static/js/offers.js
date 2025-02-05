function toggleStatus(offerId, status) {
    fetch('/update-offer-status', {
        method: 'POST',  // إرسال الطلب باستخدام POST
        headers: {
            'Content-Type': 'application/json',  // نوع البيانات المرسلة
            'X-CSRFToken': '{{ csrf_token() }}'  // إضافة CSRF Token إذا كان موجودًا
        },
        body: JSON.stringify({
            offer_id: offerId,  // معرف العرض
            status: status  // الحالة الجديدة (True أو False)
        })
    })
    .then(response => response.json())  // تحويل الاستجابة إلى JSON
    .then(data => {
        if (data.success) {
            console.log("Status updated successfully");
            // إذا تم التحديث بنجاح، نقوم بتحديث الـ checkbox
            let checkbox = document.getElementById("status-toggle-" + offerId);
            checkbox.checked = status;
        } else {
            console.error("Failed to update status:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));  // في حال حدوث خطأ
}


function updateApprovalStatus(offerId, status) {
    fetch('/update-approval-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // إذا كنت تستخدم حماية CSRF
        },
        body: JSON.stringify({
            offer_id: offerId,  // معرف العرض
            approval_status: status  // الحالة الجديدة (approved, pending, rejected)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Approval status updated successfully");
        } else {
            console.error("Failed to update approval status:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}



function saveNotes(offerId, notes) {
    fetch('/update-offer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'  // إذا كنت تستخدم CSRF للحماية
        },
        body: JSON.stringify({
            offer_id: offerId,
            notes: notes  // الملاحظات التي تم تعديلها
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Notes updated successfully");
        } else {
            console.error("Failed to update notes:", data.error);
        }
    })
    .catch(error => console.error("Error:", error));
}



// فتح نافذة تعديل العرض
function openEditModal(id) {
    const offer = offers.find(o => o.id === id);
    document.getElementById("editOfferCode").value = offer.code;
    document.getElementById("editOfferTitle").value = offer.title;
    document.getElementById("editOfferType").value = offer.type;
    document.getElementById("editOfferAmount").value = offer.amount;
    document.getElementById("editStartDate").value = offer.startDate;
    document.getElementById("editEndDate").value = offer.endDate;
    document.getElementById("editOfferId").value = offer.id; // حفظ ID العرض
    document.getElementById("editOfferModal").style.display = "block"; // فتح النافذة المنبثقة
}

// تحديث العرض
function updateOffer(event) {
    event.preventDefault();
    const id = parseInt(document.getElementById("editOfferId").value); // الحصول على ID العرض
    const index = offers.findIndex(o => o.id === id);
    if (index !== -1) {
        offers[index] = {
            code: document.getElementById("editOfferCode").value,
            title: document.getElementById("editOfferTitle").value,
            type: document.getElementById("editOfferType").value,
            amount: document.getElementById("editOfferAmount").value,
            startDate: document.getElementById("editStartDate").value,
            endDate: document.getElementById("editEndDate").value,
            id: id
        };
        localStorage.setItem("offers", JSON.stringify(offers)); // حفظ العروض في localStorage
        displayOffers();
        closeModal();
    }
}

// حذف العرض
function deleteOffer(id) {
    offers = offers.filter(o => o.id !== id);
    localStorage.setItem("offers", JSON.stringify(offers)); // حفظ العروض في localStorage
    displayOffers();
}

// إغلاق النافذة المنبثقة
function closeModal() {
    document.getElementById("editOfferModal").style.display = "none";
}

// البحث في العروض
document.getElementById("searchBtn").addEventListener("click", function() {
    const query = document.getElementById("searchBox").value.toLowerCase();
    const filteredOffers = offers.filter(offer => offer.title.toLowerCase().includes(query) || offer.code.toLowerCase().includes(query));
    displayFilteredOffers(filteredOffers);
});

function displayFilteredOffers(filteredOffers) {
    const tableBody = document.getElementById("offersTableBody");
    tableBody.innerHTML = ""; // إعادة تعيين الجدول
    filteredOffers.forEach(offer => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${offer.id}</td>
            <td>${offer.code}</td>
            <td>${offer.title}</td>
            <td>${offer.type}</td>
            <td>${offer.amount}</td>
            <td>${offer.startDate}</td>
            <td>${offer.endDate}</td>
            <td>نشط</td>
            <td>
                <button onclick="openEditModal(${offer.id})">تعديل</button>
                <button onclick="deleteOffer(${offer.id})">حذف</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// عرض العروض عند تحميل الصفحة
window.onload = displayOffers;
