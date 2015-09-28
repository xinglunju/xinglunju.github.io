$(document).ready(function(){
	var slideHeight = 140; // px
	var defHeight1 = $('.wrap1').height();
	/*var defHeight1 = 565;*/
	if(defHeight1 >= slideHeight){
		$('.wrap1').css('height', slideHeight + 'px');
		$('.read-more1').append('<a href="#" class="class1">Click for more &#x25BC;</a>');
		$('.read-more1 a').click(function(){
			var curHeight1 = $('.wrap1').height();
			if(curHeight1 == slideHeight){
				$('.wrap1').animate({
					height: defHeight1
				}, "normal");
			$('.read-more1 a').html('Click to hide &#x25B2;');
			$('.gradient1').fadeOut();
			}else{
				$('.wrap1').animate({
					height: slideHeight
				}, "normal");
				$('.read-more1 a').html('Click for more &#x25BC;');
				$('.gradient1').fadeIn();
			}
		return false;
		});  
	}
});
