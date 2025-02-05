// دالة تصفية التجار بناءً على الاسم فقط
function filterTradersByName() {
    // جلب إدخال البحث
    const searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();

    // تصفية التجار بناءً على الاسم
    const filteredTraders = traders.filter(trader =>
        trader.name.toLowerCase().includes(searchQuery)
    );

    // تحديث عرض التجار باستخدام النتائج المصفاة
    displayFilteredTraders(filteredTraders);
}

// دالة لعرض التجار بعد التصفية
function displayFilteredTraders(filteredTraders) {
    const tradersContainer = document.getElementById('tradersContainer');
    tradersContainer.innerHTML = '';

    filteredTraders.forEach(trader => {
        const traderCard = `
            <div class="order-card trader-card">
                <a style="text-decoration:none;" href="${trader.url}" class="card-link">
                    <div class="banner">
                        <img src="${trader.banner}" alt="Banner">
                    </div>
                    <div class="logo-container">
                        <img src="${trader.logo}" alt="Logo" class="logo">
                    </div>
                    <div class="order-info">
                        <h5>${trader.name}</h5>
                        <hr>
                        <div class="details">
                            <div class="right-side">
                                <p><strong>عدد المنتجات:</strong> ${trader.productCount}</p>
                                <p><strong>التخصص:</strong> ${trader.category}</p>
                            </div>
                            <div class="divider"></div>
                            <div class="left-side">
                                <p><strong>تقييم البائع:</strong> (${trader.reviewCount})</p>
                                <div class="rating-stars">${generateStars(trader.rating)}</div>
                            </div>
                        </div>
                    </div>
                </a>
            </div>
        `;
        tradersContainer.innerHTML += traderCard;
    });

    // عرض رسالة "لا توجد نتائج" إذا كانت النتائج فارغة
    const noResultsMessage = document.getElementById('noResultsMessage');
    if (noResultsMessage) {
        if (filteredTraders.length === 0) {
            noResultsMessage.style.display = 'block';
        } else {
            noResultsMessage.style.display = 'none';
        }
    }
}
