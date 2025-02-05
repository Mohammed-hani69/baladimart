document.addEventListener('DOMContentLoaded', function () {
   var swiper = new Swiper('.swiper-container', {
      loop: false,  // إيقاف التكرار التلقائي لضمان التحكم الكامل
      autoplay: {
         delay: 4000,  // تأخير الوقت بين كل سلايد (بالملي ثانية)
         disableOnInteraction: false,  // إبقاء الـ autoplay يعمل بعد التفاعل مع السلايدر
      },
      pagination: {
         el: '.swiper-pagination',
         clickable: true,
      },
      navigation: {
         nextEl: '.swiper-button-next',
         prevEl: '.swiper-button-prev',
      },
      effect: 'slide',  // تأثير الانتقال بين الشرائح
      on: {
         slideChange: function () {
            // تحقق من الشريحة الحالية
            const activeIndex = this.activeIndex;
            
            // إذا كنا في الشريحة الأخيرة (الشريحة الثالثة)، ننتقل إلى الشريحة الثانية
            if (activeIndex === 2) {
               setTimeout(() => {
                  swiper.slideTo(1);  // العودة إلى الشريحة الثانية
               }, 4000); // تأخير وقت الانتقال قليلاً لتفعيل التكرار العكسي
            }
            // إذا كنا في الشريحة الثانية، نعود إلى الشريحة الأولى
            else if (activeIndex === 1) {
               setTimeout(() => {
                  swiper.slideTo(0);  // العودة إلى الشريحة الأولى
               }, 4000); // تأخير وقت الانتقال
            }

            // تحديث النصوص المتوافقة مع السلايد النشط
            updateSlideText(this.activeIndex);
         },
      },
   });

   // دالة لتحديث النصوص المتوافقة مع كل سلايد
   function updateSlideText(index) {
      const slideTexts = [
         {
            title: "أفضل المنتجات في متناول يدك",
            description: "استكشف مجموعة مختارة من المنتجات ذات الجودة العالية في مختلف الفئات."
         },
         {
            title: "التسوق الإلكتروني بسهولة وراحة",
            description: "اكتشف كيفية تسوق أكثر ذكاءً عبر موقعنا الإلكتروني المتطور. تسوق عبر الإنترنت بكل سهولة من خلال واجهة مستخدم مريحة وعملية."
         },
         {
            title: "خدمات ما بعد البيع الاحترافية",
            description: "نحن نقدم خدمات ما بعد البيع التي تشمل الدعم الفني، الضمانات الممتدة، وخدمات الصيانة."
         }
      ];

      const titleElement = document.querySelector(".slider__text h2");
      const descriptionElement = document.querySelector(".slider__text p");

      // التأكد من أن الفهرس صحيح
      if (slideTexts[index]) {
         titleElement.innerText = slideTexts[index].title;
         descriptionElement.innerText = slideTexts[index].description;
      }
   }
});
