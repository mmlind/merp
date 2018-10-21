	
	
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

        <div class="form-group row">

          <label for="colFormLabel" class="col-sm-3 col-form-label">_('ID')</label>

          <div class="col-sm-9">

            <input required type="hidden" class="form-control" id="_id" name="_id"/>
            <input required type="text" class="form-control" id="id" name="id"/>

          </div>

        </div>

        <div class="form-group row">
          <label for="colFormLabel" class="col-sm-3 col-form-label">_('Chinese Name')</label>
          <div class="col-sm-9">
            <input required type="text" class="form-control" id="name_cn" name="name_cn" />
          </div>
        </div>

        <div class="form-group row">
          <label for="colFormLabel" class="col-sm-3 col-form-label">_('English Name')</label>
          <div class="col-sm-9">
            <input required type="text" class="form-control" id="name_en" name="name_en" />
          </div>
        </div>

        <br/>

        <button type="submit" class="btn btn-primary btn-lg btn-block">_('Save')</button>
        <br/>

      </form>


      <button id="deleteButton" type="button" class="btn btn-danger btn-block" data-toggle="modal" data-target="#deleteItem">_('Delete')</button>

      <!-- The modal -->
      <div class="modal fade" id="deleteItem" tabindex="-1" role="dialog" aria-labelledby="modalLabelSmall" aria-hidden="true">
        <div class="modal-dialog modal-sm">
          <div class="modal-content">

            <div class="modal-header">
              <h3 class="modal-title" id="modalLabelSmall">⚠️ _('ATTENTION! This item will be permanently deleted!')</h3>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
              </button>
            </div>

            <div class="modal-body">

              <button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="Close">_('Keep')</button>

              <button onclick="redirectToDelete()" type="button" class="btn btn-danger">_('Delete')</button>

            </div>

          </div>
        </div>
      </div>

    </div>


<script>

function populate_inputs(){


%if (page_mode=='insert' and submit_result=='error') or (page_mode=='update'):

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
                        window.location.href = '../../materialgroups/'; 
                        }, 
                    2000);

}

        

function redirectToDelete(){

  var url = window.location.toString();

  window.location = url.replace('upsert', 'delete');

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


%if page_mode=='insert':
  $("#deleteButton").hide();
%end


populate_inputs();
validate_page();


}



</script>

    <!-- YOUR CONTENT ENDS HERE -->
