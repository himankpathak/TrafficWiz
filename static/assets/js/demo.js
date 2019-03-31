var big_image;

demo = {

    verticalDots: function(){

    	var contentSections = $('.cd-section'),
    		navigationItems = $('#cd-vertical-nav a');

    	updateNavigation();
    	$(window).on('scroll', function(){
    		updateNavigation();
    	});

    	//smooth scroll to the section
    	navigationItems.on('click', function(event){
            event.preventDefault();
            smoothScroll($(this.hash));
        });
        //smooth scroll to second section
        $('.cd-scroll-down').on('click', function(event){
            event.preventDefault();
            smoothScroll($(this.hash));
        });

        //open-close navigation on touch devices
        $('.touch .cd-nav-trigger').on('click', function(){
        	$('.touch #cd-vertical-nav').toggleClass('open');

        });
        //close navigation on touch devices when selectin an elemnt from the list
        $('.touch #cd-vertical-nav a').on('click', function(){
        	$('.touch #cd-vertical-nav').removeClass('open');
        });

    	function updateNavigation() {
    		contentSections.each(function(){
    			$this = $(this);
    			var activeSection = $('#cd-vertical-nav a[href="#'+$this.attr('id')+'"]').data('number') - 1;
    			if ( ( $this.offset().top - $(window).height()/2 < $(window).scrollTop() ) && ( $this.offset().top + $this.height() - $(window).height()/2 > $(window).scrollTop() ) ) {
    				navigationItems.eq(activeSection).addClass('is-selected');
    			}else {
    				navigationItems.eq(activeSection).removeClass('is-selected');
    			}
    		});
    	}

    	function smoothScroll(target) {
            $('body,html').animate(
            	{'scrollTop':target.offset().top},
            	600
            );
    	}
    }
}

$(document).ready(function(){

    demo.verticalDots();
});

$('a[data-scroll="true"]').click(function(e){
    var scroll_target = $(this).data('id');
    var scroll_trigger = $(this).data('scroll');

    if(scroll_trigger == true && scroll_target !== undefined){
        e.preventDefault();

        $('html, body').animate({
             scrollTop: $(scroll_target).offset().top - 50
        }, 1000);
    }

});


// onScroll animation

if( $('body').hasClass('presentation-page') ){

    $(function() {

      var $window           = $(window),
          isTouch           = Modernizr.touch;

      if (isTouch) { $('.add-animation').addClass('animated'); }

      $window.on('scroll', revealAnimation);

      function revealAnimation() {

        // Showed...
        $(".add-animation:not(.animated)").each(function () {
          var $this     = $(this),
              offsetTop = $this.offset().top,
              scrolled = $window.scrollTop(),
              win_height_padded = $window.height();
          if (scrolled + win_height_padded > offsetTop) {
              $this.addClass('animated');
          }
        });
        // Hidden...
       $(".add-animation.animated").each(function (index) {
          var $this     = $(this),
              offsetTop = $this.offset().top;
              scrolled = $window.scrollTop(),
              win_height_padded = $window.height() * 0.8;
          if (scrolled + win_height_padded < offsetTop) {
            $(this).removeClass('animated')
          }
        });
      }

      revealAnimation();
    });
}
