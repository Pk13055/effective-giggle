			$(function () {
			$("#submit").click(function () {
		password=$("#password").val()
		email=$('#email').val()
		

	var csrftoken = $('meta[name=csrf-token]').attr('content')

		$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
    }
	})


		$.ajax({
			type:"POST",
			url:"/signin",
			// async:false,
			data:{'email':email,'password':password},
			success:function(response){
				window.location.replace(response.redirect);
					// console.log(response)
			},

			error:function(response)
			{
			// console.log(response)
				Materialize.toast(JSON.parse(response.responseText).message, 4000)
				// if(JSON.parse(response.responseText).message=="Register First")
					// window.location.replace('/signup');
			}
		})



			});
		});	

