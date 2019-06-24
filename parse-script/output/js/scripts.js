$(document).ready(function () {

	var dict = {
		"price":1,
		"name":2,
		"name":2,
	}

    $(".table").tablesorter({sortList: [[1,0]]});

    if($('.nav-item').length){

    	document.querySelector('.nav-item').scrollIntoView({ 
		  	behavior: 'smooth' 
		});

    }
    

	$('#myModal').on('shown.bs.modal', function () {
	  	//$('#myInput').trigger('focus')
	});

	$('.dropdown .dropdown-menu a').on("click", function(){
		console.log("here")
		$('.modal').modal('toggle');
	});
})

