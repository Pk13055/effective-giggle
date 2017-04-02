		$(function () {
			$("#submit").click(function () {
		
		problem_uid=$("#uid").val()

		console.log(email)

		$.ajax({
			type:"POST",
			url:"/problem/"+problem,
			async:false,
			data:{'uid':problem_uid},
			success:function(response){
				window.location.replace(response.redirect);

			},

			error:function(response)
			{
				if(confirm(JSON.parse(response.responseText).message))
				window.location.replace('/signin');
				else{}
			}
		})



			});
		});	

