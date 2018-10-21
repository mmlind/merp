	
	
    <!-- YOUR CONTENT STARTS HERE -->

      <div class="alert alert-success alert-dismissible" role="alert" id="success-message">

        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>

        <strong>_('The item was successfully deleted!')</strong>

      </div>
	
      <div class="alert alert-danger alert-dismissible" role="alert" id="error-message">

        <button type="button" class="close" data-dismiss="alert" aria-label="Close">

          <span aria-hidden="true">&times;</span>

        </button>

        <strong>_('Error! The item was not deleted!')</strong>

      </div>



<script>

function hideErrorAlert(){

 setTimeout(function () {
                        $("#error-message").hide();
                        var url = window.location.toString();
                        window.location = url.replace('delete', 'upsert');
                        }, 
                    2000);

}

function hideSuccessAlert(){

 setTimeout(function () {
                        $("#success-message").hide();
                        window.location.href = '../../materials/'; 
                        }, 
                    2000);

}

        


function initPage(){


%if delete_result == 'success':
  $("#error-message").hide();
  hideSuccessAlert();
%elif delete_result == 'error':
  $("#success-message").hide();
  hideErrorAlert();
%else:
  $("#error-message").hide();
  $("#success-message").hide();
%end


}


</script>

    <!-- YOUR CONTENT ENDS HERE -->
