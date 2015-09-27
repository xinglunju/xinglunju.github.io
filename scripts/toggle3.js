$(document).ready(function(){
	var slideHeight = 120; // px
	var defHeight = $('.wrap3').height();
	console.log('defheight=',defHeight);
	if(defHeight >= slideHeight){
		$('.wrap3').css('height', slideHeight + 'px');
		$('.read-more3').append('<a href="#" class="class1">Click for more</a>');
		$('.read-more3 a').click(function(){
			var curHeight = $('.wrap3').height();
			if(curHeight == slideHeight){
				$('.wrap3').animate({
					height: defHeight
				}, "normal");
			$('.read-more3 a').html('Click to hide');
			$('.gradient').fadeOut();
			}else{
				$('.wrap3').animate({
					height: slideHeight
				}, "normal");
				$('.read-more3 a').html('Click for more');
				$('.gradient').fadeIn();
			}
		return false;
		});  
	}
});
