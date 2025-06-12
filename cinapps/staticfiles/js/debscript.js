//navbar 

const burgerMenu = document.querySelector('.burger-menu');
const menuItems = document.querySelector('.menu-items');

burgerMenu.addEventListener('click', () => {
  menuItems.classList.toggle('active');
});


// animate on scroll // wow et animate
$(function(){
  new WOW().init();
})

// comment utiliser les plugin wow et animate:
// rajoutez simplement les class suivantes :
// "wow" si vous voulez que l'élément s'affiche au moment du scroll
// "animated" pour si vous souhaitez une animation : bounceInUp ou fadeInUp ou fadeInDown, zoomOut ou zoomIn, fadeInLeft/Right etc... voir sinon la doc wow.js
// on peut rajouter des attributs comme le delay ou la durée

// exemple d'utilisation avec les deux ensembles : <h1 class="wow animated bounceInRight" data-wow-duration="1s" data-wow-delay="1s">TITRE 1 exemple</h1>


document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".star-rating").forEach(function (rating) {
    const stars = rating.querySelectorAll("label");
    stars.forEach((star) => {
      star.addEventListener("mouseover", function () {
        const current = this;
        stars.forEach((s) => {
          s.style.color = s.compareDocumentPosition(current) & Node.DOCUMENT_POSITION_FOLLOWING ? "#ccc" : "orange";
        });
      });
      rating.addEventListener("mouseleave", function () {
        stars.forEach((s) => s.style.color = "");
      });
    });
  });
});



