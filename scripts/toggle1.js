$(document).ready(function(){
	var slideHeight = 140; // px
	var defHeight = $('.wrap1').height();
	console.log('defheight=',defHeight);
	if(defHeight >= slideHeight){
		$('.wrap1').css('height', slideHeight + 'px');
		$('.read-more1').append('<a href="#" class="class1">Click for more</a>');
		$('.read-more1 a').click(function(){
			var curHeight = $('.wrap1').height();
			if(curHeight == slideHeight){
				$('.wrap1').animate({
					height: defHeight
				}, "normal");
			$('.read-more1 a').html('Click to hide');
			$('.gradient').fadeOut();
			}else{
				$('.wrap1').animate({
					height: slideHeight
				}, "normal");
				$('.read-more1 a').html('Click for more');
				$('.gradient').fadeIn();
			}
		return false;
		});  
	}
});
