// ملف script.js
document.querySelectorAll('.thumbnail-images img').forEach((thumb) => {
    thumb.addEventListener('click', function () {
      const mainImage = document.querySelector('.main-image');
      mainImage.src = this.src;
    });
  });
  