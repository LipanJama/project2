
var backgrounds = ['url("pg1.jpg")', 'url("pg2.jpg")', 'url("pg3.jpg")']; // Add your

var currentIndex = 0;
var backgroundSlider = document.getElementById("background-slider");
var sliderBtns = document.querySelectorAll(".slider-btn");

// Function to change the background image
function changeBackground(index) {
    backgroundSlider.style.backgroundImage = backgrounds[index];
    // Remove active class from all buttons
    sliderBtns.forEach((btn) => btn.classList.remove("active"));
    // Add active class to the clicked button
    sliderBtns[index].classList.add("active");
}

// Change background when a slider button is clicked
sliderBtns.forEach((btn, index) => {
    btn.addEventListener("click", function () {
        changeBackground(index);
    });
});

// Auto change background every 5 seconds
setInterval(function () {
    currentIndex = (currentIndex + 1) % backgrounds.length;
    changeBackground(currentIndex);
}, 5000);

// Initialize with the first background
changeBackground(currentIndex);

//image slider ends here


// faqs

const faqs =document.querySelectorAll(".faq");

faqs.forEach(faq => {
    faq.addEventListener("click",() =>{
        const faqactive = document.querySelector('.faq.active')
        if(faqactive && faqactive != faq ){
            faqactive.classList.toggle('active');
            faqactive.nextElementSibling.style.maxHeigh=0;
        }
        faq.classList.toggle("active");
    })
})


let click =document.querySelector('.left-faq');

let pop =document.querySelector('.pop');
  click.onclick=function(){
      click.classList.add('active')
      pop.classList.add('active')
  }