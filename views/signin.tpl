	
    <!-- YOUR CONTENT STARTS HERE -->

      <div class="alert alert-danger alert-dismissible" role="alert" id="error-message">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
        <strong>_('Error! Username and/or password not found!')</strong>
      </div>


      <nav class="navbar navbar-inverse navbar-light bg-faded">

        <button class="navbar-toggler mr-4" type="button" data-toggle="collapse" data-target="#nav-content" aria-controls="nav-content" aria-expanded="false" aria-label="Toggle navigation">

          <span class="navbar-toggler-icon"></span>

        </button>

        <!-- Brand -->
        <h2 class="navbar-brand">{{page_title}}</h2>
        <h2 class="navbar-brand">MERP</h2>

        <!-- Links -->
% include('hamburger_menu_signin.tpl')

      </nav>

      <div class="container-fluid">

        <form method="post" name="#" class="needs-validation" novalidate onchange="validate_page();">

          <div class="form-group row">
            <label for="colFormLabel" class="col-sm-3 col-form-label">_('Username')</label>
            <div class="col-sm-9">
              <input required type="text" class="form-control" id="username" name="username"/>
            </div>
          </div>
          <div class="form-group row">
            <label for="colFormLabel" class="col-sm-3 col-form-label">_('Password')</label>
            <div class="col-sm-9">
              <input required type="password" class="form-control" id="password" name="password"/>
            </div>
          </div>

          <br/>

          <button type="submit" class="btn btn-primary btn-lg btn-block">_('Sign in')</button>
          <br/>

        </form>

      </div>


<script>

function populate_inputs(){


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



var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}




function validate_page(){


}

function hideErrorAlert(){

 setTimeout(function () {
                        $("#error-message").hide();
                        }, 
                    2000);

}


function initPage(){



if (getUrlParameter('error')==1) {

  hideErrorAlert();

} else {

$("#error-message").hide();
}



validate_page();


}



</script>

    <!-- YOUR CONTENT ENDS HERE -->
