

    <nav class="navbar fixed-bottom navbar-expand-sm navbar-dark bg-dark">

      <!-- Brand -->
      <a class="navbar-brand" href="/_('en_US')/">_('MERP')</a>


      <!-- Links -->


            <!-- PurchaseOrders -->
            <button onclick="OpenPurchaseOrders()" type="button" class="btn btn-light">_('PO')</button>
            &nbsp;
            <!-- Materials -->
            <button onclick="OpenMaterials()" type="button" class="btn btn-light">_('MT')</button>
            &nbsp;
            <!-- Suppliers -->
            <button onclick="OpenSuppliers()" type="button" class="btn btn-light">_('SP')</button>
            &nbsp;
            <!-- Products -->
            <button onclick="OpenProducts()" type="button" class="btn btn-light">_('PD')</button>

    </nav>

    <!-- YOUR CONTENT ENDS HERE -->

    <!-- JavaScript: placed at the end of the document so the pages load faster -->
    <!-- jQuery library -->
    <!--
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    -->
    <script src="/static/js/jquery-3.2.1.slim.min.js"></script>



    <!-- Popper -->
    <!--
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    -->

    <script src="/static/js/popper.min.js"></script>



    <!-- Latest compiled and minified Bootstrap JavaScript -->
    <!--
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    -->
    <script src="/static/js/bootstrap.min.js"></script>



    <script src="/static/js/bootstrap-select.js"></script>


    <script>
      function OpenPurchaseOrders(){

        window.location = "/_('en_US')/purchaseorders/"

      }
      function OpenSuppliers(){

        window.location = "/_('en_US')/suppliers/"

      }
      function OpenMaterials(){

        window.location = "/_('en_US')/materials/"

      }
      function OpenProducts(){

        window.location = "/_('en_US')/products/"

      }
    </script>


  </body>
  
</html>