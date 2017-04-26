	$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }

	})

		$(function () {
			problem_uid=$('#problem_uid').val()

			var csrftoken = $('#csrf_token').attr('content')
			console.log(problem_uid)
			console.log(csrftoken)
	
			$("#submit").click(function () {

		$.ajax({
			type:"POST",
			url:"/problems/"+problem_uid,
			// async:false,
			data:"",
			success:function(response){
				console.log("hello")
				window.location.replace(response.redirect);
			},

			error:function(response)
			{
			console.log("hi")
			console.log(response)
			// alert(response.statusText)
			window.location.replace(response.redirect);
			}
		})

			});
		});	

