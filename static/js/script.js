/*$(window).on('load', function() {

	$('.status').delay(400).fadeOut();

	$('.preloader').delay(500).fadeOut({
		'duration': 400,
		'speed': 'fast',
		'complete': function() {
			$('body').removeClass('loading');
		}
	});

});
*/

//EDIT AFTER THIS

$(document).ready(function() {

	//Add scrollspy to <body>
	//this is already done in the body opening tag
	//$('body').scrollspy({target: ".navbar", offset: $('.navbar').height()}); 
	//offset:50/70 ?

	//initialize all tooltips
	$('[data-toggle="tooltip"]').tooltip();

	// Add smooth scrolling to all links in navbar + footer link
	$(".navbar a, footer a[href='#myPage'], #learn-more-button").on('click', function(event) {
		// Make sure this.hash has a value before overriding default behavior
		if (this.hash !== "") {
			// Prevent default anchor click behavior
			event.preventDefault();

			// Store hash
			var hash = this.hash;

			// Using jQuery's animate() method to add smooth page scroll
			// The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
			$('html, body').animate({
				scrollTop: $(hash).offset().top - 69
					//if you want to change the 49 to 50, try uncommenting the scrollspy js code at the top and removing the scrollspy stuff in the body opening tag
			}, 900, function() {

				// Add hash (#) to URL when done scrolling (default click behavior)
				window.location.hash = hash;
			});
		} // End if
	}); //end onclick
	
	//AJAX for "Sign In" button click
	/*
	$('#sign-in-button').click(function(){
		var user = $('#email').val();
		var pass = $('#password').val();
		$.ajax({
			url: '/login',
			data: $('#login-form').serialize(),
			type: 'POST',
			//this stuff was used for debugging
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
*/
	




});





