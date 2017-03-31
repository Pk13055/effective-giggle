var register =function(){

	var user=$("#username").val()
	var email=$("#email").val()
	var org=$("#business").val()
	var location=$("#location").val()
	var role=$("#role").val()

	$.ajax({
		url:'/signup',
		type:'POST',
		async:false,
		data:{'user':user,'email':email,'org':org,'location':location,'role':role},
		success:function(response)
		{
			console.log("response",response)
		},
		
		error:function(response)
		{
		console.log("Error it doesn't works")
		}

	})
		 
};
			