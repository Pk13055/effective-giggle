function getCodeFunction(uid)
{
	// user=$("#user").val()

    $.ajax({
    	type:"GET",
    	url:'/solver/submission',
    	data:{'uid':uid},
  	  	success:function(response){
    		// console.log(response)
            $("#code_model").empty()    		            
    		$("#code_model").append(response)

    	},
    	error:function (response) {
    		// console.log("error")
    		// console.log(response)
            alert(JSON.parse(response))
        }
 
    })

    $('#getCode-modal').modal('open');

    // console.log("problem")

}
