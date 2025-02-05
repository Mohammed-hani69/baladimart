document.addEventListener("DOMContentLoaded", function () {
  // اختيار جميع أزرار "إضافة إلى السلة"
  const addToCartButtons = document.querySelectorAll(".add-to-cart");

  // إضافة مستمع الحدث لكل زر إذا لم يكن مضافًا بالفعل
  addToCartButtons.forEach(button => {
      button.removeEventListener("click", handleAddToCart); // إزالة أي مستمعات مكررة
      button.addEventListener("click", handleAddToCart);    // إضافة مستمع جديد
  });

  function handleAddToCart(event) {
      event.preventDefault(); // منع السلوك الافتراضي للرابط

      // الحصول على معرف المنتج ومعرف البائع
      const productId = this.getAttribute("data-product-id");
      const sellerId = this.getAttribute("data-seller-id");

      // إرسال الطلب لإضافة المنتج إلى السلة
      fetch('/add-to-cart', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product_id: productId, seller_id: sellerId })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              console.log("تمت إضافة المنتج إلى السلة.");
          } else {
              alert(`خطأ: ${data.message}`);
          }
      })
      .catch(error => {
          console.error("حدث خطأ أثناء إضافة المنتج إلى السلة:", error);
          window.location.href = '/login';
      });
  }
});



document.addEventListener("DOMContentLoaded", function () {
  const firstChildButton = document.querySelector(".product-action li:first-child");

  if (firstChildButton) {
      firstChildButton.addEventListener("click", function (event) {
          // إيقاف السلوك الافتراضي إذا كان الزر داخل <a> أو عنصر يسبب إعادة تحميل الصفحة
          event.preventDefault();

          // تغيير الفئة لتفعيل اللون الأحمر
          this.classList.toggle("active");
      });
  }
});




// استدعاء الفلتر عند تغيير أي من عناصر التصفية
document.addEventListener('DOMContentLoaded', function() {
  const filterElements = document.querySelectorAll('.store-filter, .category-filter, #hasDiscount');
  const priceInputs = document.querySelectorAll('#minPrice, #maxPrice');
  const resetButton = document.getElementById('resetFilters');

  // دالة تجميع معايير الفلترة
  function getFilterCriteria() {
      const criteria = {
          stores: Array.from(document.querySelectorAll('.store-filter:checked')).map(el => el.value),
          categories: Array.from(document.querySelectorAll('.category-filter:checked')).map(el => el.value),
          minPrice: document.getElementById('minPrice').value,
          maxPrice: document.getElementById('maxPrice').value,
          hasDiscount: document.getElementById('hasDiscount').checked
      };
      return criteria;
  }

  // دالة تحديث المنتجات
  function updateProducts(criteria) {
      fetch('/filter-products', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(criteria)
      })
      .then(response => response.json())
      .then(data => {
          const productsContainer = document.querySelector('.boxs2');
          productsContainer.innerHTML = ''; // مسح المنتجات الحالية

          data.products.forEach(product => {
              const productHTML = createProductElement(product);
              productsContainer.insertAdjacentHTML('beforeend', productHTML);
          });
      })
      .catch(error => console.error('Error:', error));
  }

  // دالة إنشاء عنصر المنتج
  function createProductElement(product) {
      return `
          <div class="box column product-item2 product-item custom-small-card">
              <div class="div-img2 div-img">
                  ${product.discount ? `<span class="discount">${product.discount}%</span>` : ''}
                  <a href="/product/${product.product_id}">
                      <img src="/static/uploads/products/${product.image1}" class="img-product">
                      <img src="/static/uploads/products/${product.image1}" class="hover-img">
                  </a>
                  <div class="product-btn" style="position: relative;">
                      <ul class="product-action">
                          <li style="position: absolute; top: 10px;">
                              <a href="#"><i class="fa-regular fa-heart"></i></a>
                          </li>
                          <li style="position: absolute; bottom: 10px; left: 10px;">
                              <a href="#" class="add-to-cart" data-product-id="${product.product_id}">
                                  <i class="fa-solid fa-cart-arrow-down"></i>
                              </a>
                          </li>
                      </ul>
                  </div>
              </div>
              <div class="content2">
                  <a href="/product/${product.product_id}" class="product-item-link">
                      ${product.product_name.length > 30 ? 
                        product.product_name.substring(0, 30) + '...' : 
                        product.product_name}
                  </a>
                  <div class="stars">
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star"></i>
                      <i class="fa-solid fa-star-half-stroke"></i>
                  </div>
                  <div class="price">
                      <span>${product.final_price} جنيه</span>
                      ${product.discount ? `<del>${product.original_price} جنيه</del>` : ''}
                  </div>
              </div>
          </div>
      `;
  }

  // إضافة مستمعي الأحداث
  filterElements.forEach(element => {
      element.addEventListener('change', () => {
          updateProducts(getFilterCriteria());
      });
  });

  priceInputs.forEach(input => {
      input.addEventListener('input', debounce(() => {
          updateProducts(getFilterCriteria());
      }, 500));
  });

  // زر إعادة تعيين الفلاتر
  resetButton.addEventListener('click', () => {
      document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => checkbox.checked = false);
      document.querySelectorAll('input[type="number"]').forEach(input => input.value = '');
      updateProducts(getFilterCriteria());
  });

  // دالة لتأخير تنفيذ البحث عند كتابة السعر
  function debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
          const later = () => {
              clearTimeout(timeout);
              func(...args);
          };
          clearTimeout(timeout);
          timeout = setTimeout(later, wait);
      };
  }
});










var swiper = new Swiper(".slide-swp", {
   pagination: {
     el: ".swiper-pagination",
     dynamicBullets: true,
     clickable:true
   },
   autoplay:{
       delay:2500,
       disableOnInteraction: false,

   },
   loop:true,
 });

 var swiper = new Swiper(".deals", {
   slidesPerView: 2,
   spaceBetween: 30,
     autoplay: {
       delay: 4000,
       disableOnInteraction: false,
     },
     navigation: {
       nextEl: ".swiper-button-next",
       prevEl: ".swiper-button-prev",
     },
     loop:true,
     breakpoints:{
       1200:{
         slidesPerView : 2,
       },
       990 : {
         slidesPerView : 1,
       },
       0 :{
         slidesPerView : 1,
       }
       
     }
 });



 var swiper = new Swiper(".sale-sec", {
   slidesPerView: 5,
   spaceBetween: 30,
     autoplay: {
       delay: 3000,
       disableOnInteraction: false,
     },
     navigation: {
       nextEl: ".swiper-button-next",
       prevEl: ".swiper-button-prev",
     },
     loop:true,
     breakpoints:{
       1400:{
         slidesPerView: 5,
       },
       1200:{
         slidesPerView : 4,
       },
       800:{
         slidesPerView : 3,
         spaceBetween: 30,
       },
       650 :{
         slidesPerView : 3,
         spaceBetween: 15,
       },
       0 :{
         slidesPerView : 2,
         spaceBetween: 10,
       }
       
     }
 });


 
 var swiper = new Swiper(".swip-with-img", {
   slidesPerView: 4,
   spaceBetween: 30,
     autoplay: {
       delay: 3000,
       disableOnInteraction: false,
     },
     navigation: {
       nextEl: ".swiper-button-next",
       prevEl: ".swiper-button-prev",
     },
     loop:true,
     breakpoints:{
       1400:{
         slidesPerView: 4,
       },
       1100:{
         slidesPerView : 3,
       },
       800:{
         slidesPerView : 2,
         spaceBetween: 30,
       },
       700 :{
         slidesPerView : 2,
         spaceBetween: 15,
       },
       0 :{
         slidesPerView : 2,
         spaceBetween: 10,
       }
       
     }
 });
 


 /* side bar in Resbonsive */

 let btnCloseSide = document.getElementById("btn-close");
 let sideBar = document.getElementById("side-bar");
 let btnOpenSide = document.getElementById("open-side");

 btnOpenSide.onclick = () => {
   sideBar.classList.add('active')
 }
 btnCloseSide.onclick = () => {
   sideBar.classList.remove('active')
 }









 let bigImage = document.getElementById('big-img')

       function myProduct(item){
           bigImage.src = item
       }


       // product page
       //buy fast order
       
       let divcretAcBuyF = document.querySelector('.creatacountfast')



const slider = document.getElementById('unique-slider');

// إضافة عملية سحب للماوس
slider.addEventListener('mousedown', (e) => {
 let isDragging = true;
 let startPos = e.clientX;
 let currentTranslate = 0;
 let prevTranslate = 0;

 slider.style.transition = 'none'; // إزالة التأثير عند السحب
 const mouseMove = (e) => {
   if (!isDragging) return;
   const currentPos = e.clientX;
   const diff = currentPos - startPos;
   currentTranslate = prevTranslate + diff;
   slider.style.transform = `translateX(${currentTranslate}px)`;
 };

 const mouseUp = () => {
   isDragging = false;
   prevTranslate = currentTranslate;
   slider.style.transition = 'transform 0.3s ease'; // إضافة تأثير الانتقال
   slider.removeEventListener('mousemove', mouseMove);
   slider.removeEventListener('mouseup', mouseUp);
 };

 slider.addEventListener('mousemove', mouseMove);
 slider.addEventListener('mouseup', mouseUp);
});

// إضافة سحب في الأجهزة الصغيرة (الهاتف)
if (window.innerWidth <= 768) {
 let touchStart = 0;
 let touchEnd = 0;

 slider.addEventListener('touchstart', (e) => {
   touchStart = e.touches[0].clientX;
 });

 slider.addEventListener('touchend', (e) => {
   touchEnd = e.changedTouches[0].clientX;
   if (touchEnd - touchStart > 50) {
     slider.scrollLeft -= 150; // السحب لليسار
   } else if (touchStart - touchEnd > 50) {
     slider.scrollLeft += 150; // السحب لليمين
   }
 });
}



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


var swiper1 = new Swiper('.mySwiper1', {
  slidesPerView: 1,
  spaceBetween: 10,
  loop: true,
  autoplay: {
      delay: 2000,  /* تقليل وقت الانتقال بين الصور */
      disableOnInteraction: false,
  },
  pagination: {
      el: '.swiper-pagination',
      clickable: true,
  },
  effect: 'slide',  /* تأثير الانتقال بين الصور */
  speed: 500,  /* تقليل سرعة الانتقال بين الصور */
});

var swiper2 = new Swiper('.mySwiper2', {
  slidesPerView: 1,
  spaceBetween: 10,
  loop: true,
  autoplay: {
      delay: 2000,
      disableOnInteraction: false,
  },
  pagination: {
      el: '.swiper-pagination',
      clickable: true,
  },
  effect: 'slide',
  speed: 500,
});

var swiper3 = new Swiper('.mySwiper3', {
  slidesPerView: 1,
  spaceBetween: 10,
  loop: true,
  autoplay: {
      delay: 2000,
      disableOnInteraction: false,
  },
  pagination: {
      el: '.swiper-pagination',
      clickable: true,
  },
  effect: 'slide',
  speed: 5000,
});





