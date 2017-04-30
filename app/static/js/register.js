var message_password="";
var message_user="";
var message_email="";

//to validate proper email address firstname@lastname.com
function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

var check = function(id) 
	{
		if(id==='password')
		{
			var password = $("#https1").val();
				var confirmPassword = $("#https2").val();
				if (password != confirmPassword) {
						if(Materialize.toast === null)
					Materialize.toast('Passwords dont match', 4000)
					$("#password1_logo").addClass('red-text')
					$("#password2_logo").addClass('red-text')
					message_password =message_password.replace(message_password,"Passwords dont match");
				}				
				else{
				Materialize.toast('Passwords match', 4000)			
				$("#password1_logo").addClass('green-text')
				$("#password2_logo").addClass('green-text')
				message_password =message_password.replace(message_password,"");
					
				}
		}

		else if(id==='user' || id==='email')
		{
			var value=document.getElementById(id).value
			console.log(validateEmail(value))
				$.ajax({
					type:'GET',
					url:"/checks",
					// async:false,
					data:{'id':id,'value':value},
					success:function(response){
						if(id==="user"){
							if(value.length < 5)
								{	$("#user_logo").addClass('red-text').removeClass('green-text');	
							message_user =message_user.replace(message_user,"Username must have more than 5 characters")
						}
							
							else if(response.message===false) 
							{
								Materialize.toast('username already exists ', 5000);
								$("#user_logo").addClass('red-text').removeClass('green-text');
								message_user =message_user.replace(message_user,"Username already exists")
								
							}
							else if(response.message===true)
								{$("#user_logo").addClass('green-text');
									message_user =message_user.replace(message_user,"")
								}
						
						}
					
						else if(id==="email"){
							if(validateEmail(value)===false)
								{$("#email_logo").addClass('red-text').removeClass('green-text');
									message_email =message_email.replace(message_email,"Email not valid");

									}
							
							else if(response.message==false) 
							{
								Materialize.toast('Email already exists ', 5000);
								$("#email_logo").addClass('red-text').removeClass('green-text');
								message_email =message_email.replace(message_email,"Email already exists");
								
							}
							else if(response.message===true)
								{$("#email_logo").addClass('green-text');
									message_email =message_email.replace(message_email,"");
								}
						}

					},
					error:function(response)
					{
						console.log(response);
					}
				});
		}
	

		else
		{
			$("#"+id+"_logo").addClass('green-text');
		}


	}	


	$(function () {
			$("#submit_registration").click(function () {
				if (message_user!="") 
				{
					Materialize.toast(message_user,5000);		
					return false;
				}

				else if (message_email!="") 
				{
					Materialize.toast(message_email,5000);		
					return false;
				}
				
				else if (message_password!="") 
				{
					Materialize.toast(message_password,5000);		
					return false;
				}

				else
				{
					Materialize.toast("Redirecting",5000);
					return true;
				}
			
			});
	});