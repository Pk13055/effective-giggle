		$(function () {
			problem_uid=$('#problem_uid').val()
			console.log(problem_uid)

			$("#submit").click(function () {

		$.ajax({
			type:"POST",
			url:"/problems/"+problem_uid,
			// async:false,
			data:"",
			success:function(response){
				window.location.replace('/solver/'+session.user_uid);
			},

			error:function(response)
			{
			console.log(response)
			alert(response.message)
			window.location.replace('/problems/'+problem_uid);

			}
		})



			});
		});	

