		$(function () {
			problem_uid=$('#problem_uid').val()
			console.log(problem_uid)
			var csrf_token = '<%= token_value %>';

			$("#submit").click(function () {

		$.ajax({
			type:"POST",
			url:"/problems/"+problem_uid,
			// async:false,
			xhr.setRequestHeader('X-CSRF-Token', csrf_token);
			data:"",
			success:function(response){
				console.log("hello")
				window.location.replace(response.redirect);
			},

			error:function(response)
			{
			console.log("hi")
			console.log(response)
			alert(response.statusText)
			window.location.replace(response.redirect);
			}
		})

			});
		});	

