$(document).ready(function() {
	$('#banner img:gt(0)').hide();
	setInterval(function() {
		$('#banner :first-child').fadeOut()
			.next('img').fadeIn()
			.end().appendTo('#banner');
	}, 2);
});