	
	
  <!-- YOUR CONTENT STARTS HERE -->

    <div class="alert alert-success alert-dismissible" role="alert" id="success-message">

      <button type="button" class="close" data-dismiss="alert" aria-label="Close">

        <span aria-hidden="true">&times;</span>

      </button>

      <strong>_('Saved successfully!')</strong>

    </div>
	

    <div class="alert alert-danger alert-dismissible" role="alert" id="error-message">

      <button type="button" class="close" data-dismiss="alert" aria-label="Close">

        <span aria-hidden="true">&times;</span>

      </button>

      <strong>_('Error! Data was not saved!')</strong>

    </div>


    <nav class="navbar navbar-inverse navbar-light bg-faded justify-content-start">

<!--
      <button onclick="window.location='../'" type="button" class="btn btn-light mr-4">_('Cancel')</button>
-->
      <button onclick="window.location='../'" type="button" class="btn btn-outline-secondary mr-4">
        <i class="fas fa-arrow-alt-circle-left"></i>
      </button>

    
      <!-- Brand -->
      <h2 class="navbar-brand">{{page_title}}</h2>

    </nav>


    <div class="container-fluid">

      <form method="post" class="needs-validation" novalidate onchange="validate_page();">

        <input required type="hidden" class="form-control" id="_id" name="_id"/>
        <input required type="hidden" class="form-control" id="datetime" name="datetime" value="{{page_object.datetime}}" />

        <div class="form-group row">
          <label for="colFormLabel" class="col-sm-3 col-form-label">_('Supplier')</label>
          <div class="col-sm-9">

<!--
            <input required type="text" class="form-control" id="supplier_id" name="supplier_id" />
-->

        <select class="selectpicker form-control" id="supplier_id" name="supplier_id" data-container="body" data-live-search="true" title="Select a supplier" data-hide-disabled="true">
          
%for supplier in suppliers:

              <option value="{{supplier._id}}">{{supplier.name_cn if locale=='zh_CN' else supplier.name_en}}</option>

%end

        </select>


          </div>



        </div>


        <br/>

        <button type="submit" class="btn btn-primary btn-lg btn-block">_('Create')</button>

        <br/>

      </form>

      <br/>

    </div>


<script>

function populate_inputs(){


%if (submit_result=='error'):

%for attr, value in page_object.__dict__.iteritems():

  $("#{{attr}}")            .val(value = '{{value}}' );

%end

%end


}


// disabling form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch form to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();



function validate_page(){


}



function hideErrorAlert(){

 setTimeout(function () {
                        $("#error-message").hide();
                        }, 
                    2000);

}

function hideSuccessAlert(){

 setTimeout(function () {
                        $("#success-message").hide();
                        window.location.href = '../../purchaseorders/update/{{page_object._id}}'; 
                        }, 
                    1000);

}

        



function initPage(){


%if submit_result == 'success':
  $("#error-message").hide();
  hideSuccessAlert();
%elif submit_result == 'error':
  $("#success-message").hide();
  hideErrorAlert();
%else:
  $("#error-message").hide();
  $("#success-message").hide();
%end



populate_inputs();
validate_page();


}



</script>

    <!-- YOUR CONTENT ENDS HERE -->
