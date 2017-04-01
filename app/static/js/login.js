		$(function () {
			$("#submit").click(function () {
		password=$("#password").val()
		email=$('#email').val()

		console.log(email)

		$.ajax({
			type:"POST",
			url:"/signin",
			// async:false,
			data:{'email':email,'password':password},
			success:function(response){
				window.location.replace(response.redirect);

			},

		})



			});
		});	

