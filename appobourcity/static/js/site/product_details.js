function toggleShareModal(productName = '') {
    const modal = document.getElementById('share-modal');
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
  
    const currentUrl = encodeURIComponent(window.location.href);
    const message = encodeURIComponent(`✨ جرب الآن ${productName}! إنه المنتج الأفضل لك. 🚀 اطلبه قبل نفاد الكمية! 🌟`);
  
    // تحديث الروابط مع النص التحفيزي
    document.getElementById('twitter-share').href = `https://twitter.com/intent/tweet?url=${currentUrl}&text=${message}`;
    document.getElementById('facebook-share').href = `https://www.facebook.com/sharer/sharer.php?u=${currentUrl}&quote=${message}`;
    document.getElementById('linkedin-share').href = `https://www.linkedin.com/sharing/share-offsite/?url=${currentUrl}&summary=${message}`;
    document.getElementById('whatsapp-share').href = `https://api.whatsapp.com/send?text=${message}%20${currentUrl}`;
    document.getElementById('telegram-share').href = `https://t.me/share/url?url=${currentUrl}&text=${message}`;
    document.getElementById('email-share').href = `mailto:?subject=${productName}&body=${message}%20${currentUrl}`;
  }
  
  // إغلاق النافذة عند النقر خارج المحتوى
  window.onclick = function(event) {
    const modal = document.getElementById('share-modal');
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };
  