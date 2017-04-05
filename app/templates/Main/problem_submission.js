	var func=function (user_uid) {
		
		if ( $("#user_uid").val() ==='undefined')
		{
			alert("Register First")
			window.location.replace('/signin')
		}

		$.ajax({
			type:"POST",
			url:"/problem/"+problem_uid,
			async:false,
			data:{'user_uid':user_uid},
			success:function(response){
				window.location.replace(response.redirect);

			},

			error:function(response)
			{
				console.log(response)
				// alert(JSON.parse(response.responseText).message)
				
			}
		})
	}
