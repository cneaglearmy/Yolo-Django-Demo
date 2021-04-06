$(function(){
	$('form').submit(function(){
		if ($('[name=myfile]').val() != "")
			$('.loading').css('display','block');
	});
});