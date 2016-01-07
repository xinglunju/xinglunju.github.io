$(document).ready(function(){
	var slideHeight = 320; // px
	var defHeight2 = $('.wrap2').height();
	/*var defHeight2 = 1082;*/
	if(defHeight2 >= slideHeight){
		$('.wrap2').css('height', slideHeight + 'px');
		$('.read-more2').append('<a href="#" class="class1">Click for more &#x25BC;</a>');
		$('.read-more2 a').click(function(){
			var curHeight2 = $('.wrap2').height();
			if(curHeight2 == slideHeight){
				$('.wrap2').animate({
					height: defHeight2
				}, "normal");
			$('.read-more2 a').html('Click to hide &#x25B2;');
			$('.gradient2').fadeOut();
			}else{
				$('.wrap2').animate({
					height: slideHeight
				}, "normal");
				$('.read-more2 a').html('Click for more &#x25BC;');
				$('.gradient2').fadeIn();
			}
		return false;
		});  
	}
});
