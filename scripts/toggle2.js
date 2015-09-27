$(document).ready(function(){
	var slideHeight = 105; // px
	var defHeight = $('.wrap2').height();
	if(defHeight >= slideHeight){
		$('.wrap2').css('height', slideHeight + 'px');
		$('.read-more2').append('<a href="#" class="class1">Click for more</a>');
		$('.read-more2 a').click(function(){
			var curHeight = $('.wrap2').height();
			if(curHeight == slideHeight){
				$('.wrap2').animate({
					height: defHeight
				}, "normal");
			$('.read-more2 a').html('Click to hide');
			$('.gradient').fadeOut();
			}else{
				$('.wrap2').animate({
					height: slideHeight
				}, "normal");
				$('.read-more2 a').html('Click for more');
				$('.gradient').fadeIn();
			}
		return false;
		});  
	}
});
