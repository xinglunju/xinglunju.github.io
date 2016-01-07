$(document).ready(function(){
	var slideHeight = 320; // px
	var defHeight3 = $('.wrap3').height();
	/*var defHeight3 = 1424;*/
	if(defHeight3 >= slideHeight){
		$('.wrap3').css('height', slideHeight + 'px');
		$('.read-more3').append('<a href="#" class="class1">Click for more &#x25BC;</a>');
		$('.read-more3 a').click(function(){
			var curHeight3 = $('.wrap3').height();
			if(curHeight3 == slideHeight){
				$('.wrap3').animate({
					height: defHeight3
				}, "normal");
			$('.read-more3 a').html('Click to hide &#x25B2;');
			$('.gradient3').fadeOut();
			}else{
				$('.wrap3').animate({
					height: slideHeight
				}, "normal");
				$('.read-more3 a').html('Click for more &#x25BC;');
				$('.gradient3').fadeIn();
			}
		return false;
		});  
	}
});
