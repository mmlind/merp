	
	
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

      <form id="po_form" method="post" class="needs-validation" novalidate onchange="validate_page();">

        <div class="form-group row">
          <label for="colFormLabel" class="col-sm-3 col-form-label">_('Date')</label>

          <div class="col-sm-9">
            <input disabled type="text" class="form-control" value="{{page_object.datetime}}"/>
          </div>

        </div>

        <div class="form-group row">
          <label for="colFormLabel" class="col-sm-3 col-form-label">_('Supplier')</label>

          <div class="col-sm-9">
            <input disabled type="text" class="form-control" value="{{page_object.supplier.name_cn if locale=='zh_CN' else page_object.supplier.name_en}}"/>
          </div>
        </div>


        <div class="form-group row">
          <label for="colFormLabel" class="col-sm-3 col-form-label">_('Materials')</label>
          <div class="col-sm-9">

            <select multiple onchange="updateList()" class="selectpicker form-control" id="material_ids" name="material_ids" data-container="body" data-live-search="true" title="Select materials" data-hide-disabled="true"
            data-actions-box="true" data-virtual-scroll="false">
              
                  %for material in materials:

                  <option value="{{material._id}}">{{material.name_cn if locale=='zh_CN' else material.name_en}}</option>

                  %end

            </select>

          </div>
        </div>
        <br/>



        <table class="table table-striped table-hover" style="cursor:pointer">
          <thead>
            <tr>
              <th align="left" >_('Material')</th>
              <th align="right">_('Quantity')</th>
              <th align="left" >_('Unit')</th>
              <th align="right">_('Price')</th>
              <th align="left" >_('Unit')</th>
              <th align="right">_('Total')</th>
            </tr>
          </thead>
          <tbody>

%from language import _

            %for item in items:

            %i18n_base_unit  = _(item.material.base_unit)
            %i18n_pack_unit  = _(item.material.pack_unit)
            %i18n_order_unit = _(item.material.order_unit)

            %i18n_qty_unit   = _(item.qty_unit)
            %i18n_price_unit = _(item.price_unit)

            <tr data-toggle="modal" 
            item-material-sid="{{item.material._id}}" 
            item-qty       ="{{item.qty}}" 
            item-qty-unit  ="{{item.qty_unit}}" 
            item-price     ="{{item.price}}" 
            item-price-unit="{{item.price_unit}}" 
            item-total     ="{{item.total}}"
            item-pack-unit ="{{item.material.pack_unit}}"
            item-order-unit="{{item.material.order_unit}}"
            item-pack-unit-qty ="{{item.material.pack_unit_qty}}"
            item-order-unit-qty="{{item.material.order_unit_qty}}"
            data-units     ='{"{{item.material.order_unit}}":"{{i18n_order_unit}}","{{item.material.pack_unit}}" :"{{i18n_pack_unit}}", "{{item.material.base_unit}}" :"{{i18n_base_unit}}"}' 
            item-title="{{item.material.name_cn if locale=='zh_CN' else item.material.name_en}} ({{item.material.id}})" 
            item-sizes="{{item.material.order_unit_qty}} {{i18n_pack_unit}} / {{i18n_order_unit}}, {{item.material.pack_unit_qty}} {{i18n_base_unit}} / {{i18n_pack_unit}}" 
            data-target="#orderModal">
              <td class="col_name"       align="left" >{{item.material.name_cn if locale=='zh_CN' else item.material.name_en}}</td>
              <td class="col_qty"        align="right">{{item.qty}}</td>
              <td class="col_qty_unit"   align="left" >{{i18n_qty_unit}}</td>
              <td class="col_price"      align="right">{{item.price}} 元</td>
              <td class="col_price_unit" align="left" >{{i18n_price_unit}}</td>
              <td class="col_total"      align="right">{{item.total}} 元</td>
            </tr>

            %end

            <tfoot>
              <tr>
                <th>_('Total')</th>
                <th colspan="5" align="right" class="text-right" id="order-total">{{page_object.total}} 元</th>
              </tr>
            </tfoot>


          </tbody>
        </table>

        <br/>

        <button type="submit" class="btn btn-primary btn-lg btn-block">_('Save')</button>

        <br/>
      </form>


      <button id="deleteButton" type="button" class="btn btn-danger btn-block" data-toggle="modal" data-target="#deleteItem">_('Delete')</button>

      <br/>
      <br/>
      <br/>




      <!-- ITEM-DETAILS modal -->

      <div class="modal fade" id="orderModal" tabindex="-1" role="dialog" aria-labelledby="Modal2" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h3 class="modal-title" id="modal_item_title"></h3>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div id="order_details" class="modal-body">

              <span>_('Units'): </span>
              <h4 id="modal_item_sizes"></h4>

              <table style="width:100%;border:none">
              <thead>
              </thead>
              <tbody class="table">
                <tr>

                  <td class="col-sm-6">_('Quantity')</td>
                  <td class="col-sm-6" colspan="2">
                    <input onchange="updateItemTotal()" required type="number" step="0.01" id="modal_item_qty" style="text-align:right" />
                  </td>

                </tr>
                <tr>

                  <td class="col-sm-6">_('Order Unit')</td>
                  <td class="col-sm-6" colspan="2">
                    <select onchange="updateItemTotal()" required class="custom-select" id="modal_item_qty_unit" >
                    </select>
                  </td>

                </tr>
                <tr>

                  <td class="col-sm-6">_('Price')</td>
                  <td class="col-sm-3">
                    <input onchange="updateItemTotal()" required type="number" step="0.01" id="modal_item_price" style="text-align:right" />
                  </td>
                  <td class="col-sm-3">元</td>

                </tr>
                <tr>

                  <td class="col-sm-6">_('Price Unit')</td>
                  <td class="col-sm-6" colspan="2">
                    <select onchange="updateItemTotal()" required class="custom-select" id="modal_item_price_unit" >
                    </select>
                  </td>

                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <th class="col-sm-6">_('Total')</th>
                  <th class="col-sm-3" id="modal_item_total" style="text-align:right;">0.00</th>
                  <th class="col-sm-3" style="font-style: bold">元</th>
                </tr>
              </tfoot>
              </table>

              
            </div>
            <div class="modal-footer">

              <p>_('Input order amount and price for this material, specifying the correct order and price units.')</p>

              <button type="button" class="btn btn-secondary" data-dismiss="modal">_('Cancel')</button>
              <button onclick="updateItemFromModal()" type="button" data-dismiss="modal" class="btn btn-success">_('Confirm')</button>

            </div>
          </div>
        </div>
      </div>


      <!-- DELETE modal -->
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

              <button type="button" class="btn btn-secondary" data-dismiss="modal" aria-label="_('Keep')">_('Keep')</button>

              <button onclick="redirectToDelete()" type="button" class="btn btn-danger">_('Delete')</button>

            </div>

          </div>
        </div>
      </div>

    </div>


<script>




function populate_inputs(){


var material_ids = [];

%for item in page_object.items:

material_sid = '{{item.material._id}}';
qty          = '{{item.qty}}';
qty_unit     = '{{item.qty_unit}}';
price        = '{{item.price}}';
price_unit   = '{{item.price_unit}}';
total        = '{{item.total}}';


material_ids.push(material_sid);


updateItem(material_sid, qty, qty_unit, price, price_unit, total);

%end


$("#material_ids").selectpicker('val',material_ids);
// $("#material_ids").selectpicker('refresh')



// $("#material_ids").selectpicker('val',['5b9bc8dd2652c287a690baca', '5b9c725b2652c29bd4155b97'])
// alert('multiple selected');





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





}







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
                        window.location.href = '../../purchaseorders/'; 
                        }, 
                    50);

}

        

function redirectToDelete(){

  var url = window.location.toString();

  window.location = url.replace('update', 'delete');

}



function updateList(){


  var sel_ids = $("#material_ids").val();

  var order_total = 0;

  // hide all
  // $("tr[data-toggle='modal'").hide()
  $("tr[item-material-sid]").hide()


  // show selected materials
  for (var i in sel_ids){
    var sel_id = sel_ids[i]
    $("tr[item-material-sid='"+sel_id+"']").show()
    var item_total = parseFloat($("tr[item-material-sid='"+sel_id+"']").attr("item-total"));

    order_total = order_total + item_total;

  }

  $('#order-total').text(order_total.toFixed(2) + " 元");




}


function updateItemTotal(){

  // get values from the modal
  var qty        = $("#modal_item_qty").val()
  var qty_unit   = $('#modal_item_qty_unit').val()
  var price      = $("#modal_item_price").val()
  var price_unit = $('#modal_item_price_unit').val()

  // get row of the item thats currently shown in the modal 
  // var row_id = $("#order_details").attr("item-row-id");
  // var $row = $("tr[item-row-id='"+row_id+"'");
  var sid = $("#order_details").attr("item-material-sid");
  var $row = $("tr[item-material-sid='"+sid+"']");

  // get unit conversion factors
  var pack_unit      = $row.attr("item-pack-unit");
  var pack_unit_qty  = $row.attr("item-pack-unit-qty");
  var order_unit     = $row.attr("item-order-unit");
  var order_unit_qty = $row.attr("item-order-unit-qty");


  var price_per_base_unit = 0;

  if (price_unit == pack_unit) {
    price_per_base_unit = price/pack_unit_qty;
  } else 
  if (price_unit == order_unit) {
    price_per_base_unit = price/pack_unit_qty/order_unit_qty;
  } else {
    price_per_base_unit = price;
  }


  var qty_per_base_unit = 0;

  if (qty_unit == pack_unit) {
    qty_per_base_unit = qty * pack_unit_qty;
  } else 
  if (qty_unit == order_unit) {
    qty_per_base_unit = qty * pack_unit_qty * order_unit_qty;
  } else {
    qty_per_base_unit = qty;
  }


  var total = (Math.round(qty_per_base_unit * price_per_base_unit * 100) / 100).toFixed(2);

  // update the row attributes (to store the values for saving or further changes)
  $('#modal_item_total').text(total);

  return total;
}




function updateItem(material_sid, qty, qty_unit, price, price_unit, total){

  // var $row = $("tr[item-row-id='"+row_id+"'");
  var $row = $("tr[item-material-sid='"+material_sid+"']");

  // get units dictionary which includes translated unit values
  var units = $row.data("units");

  // update the order items on the main page
  $row.children('td.col_qty').text(qty);
  $row.children('td.col_qty_unit').text(units[qty_unit]);
  $row.children('td.col_price').text(parseFloat(price).toFixed(2) + " 元");
  $row.children('td.col_price_unit').text(units[price_unit]);
  $row.children('td.col_total').text(parseFloat(total).toFixed(2) + " 元");

  // update the row attributes (to store the values for saving or further changes)
  $row.attr("item-qty",qty);
  $row.attr("item-qty-unit",qty_unit);
  $row.attr("item-price",price);
  $row.attr("item-price-unit",price_unit);
  $row.attr("item-total",total);

  updateList();

}



function updateItemFromModal(){

  // get values from the modal
  var qty        = $("#modal_item_qty").val()
  var qty_unit   = $('#modal_item_qty_unit').val()
  var price      = $("#modal_item_price").val()
  var price_unit = $('#modal_item_price_unit').val()
  var total      = $("#modal_item_total").text()


  // get row of the item thats currently shown in the modal 
  // var row_id = $("#order_details").attr("item-row-id");
  var material_sid = $("#order_details").attr("item-material-sid");
  // var $row = $("tr[item-row-id='"+row_id+"'");

  // get units dictionary which includes translated unit values
  // var units      = $row.data("units");


  // update the order items on the main page
  // $row.children('td.col_qty').text(qty);
  // $row.children('td.col_qty_unit').text(units[qty_unit]);
  // $row.children('td.col_price').text(price + " 元");
  // $row.children('td.col_price_unit').text(units[price_unit]);
  // $row.children('td.col_total').text(total + " 元");

  // update the row attributes (to store the values for saving or further changes)

  updateItem(material_sid, qty, qty_unit, price, price_unit, total);

  // $row.attr("item-qty",qty);
  // $row.attr("item-qty-unit",qty_unit);
  // $row.attr("item-price",price);
  // $row.attr("item-price-unit",price_unit);
  // $row.attr("item-total",total);

}




function updateItemInModal(row){

  // var row_id     = $(row).attr("item-row-id");
  var material_sid = $(row).attr("item-material-sid");
  var title      = $(row).attr("item-title");
  var qty        = $(row).attr("item-qty");
  var qty_unit   = $(row).attr("item-qty-unit");
  var price      = $(row).attr("item-price");
  var price_unit = $(row).attr("item-price-unit");
  var units      = $(row).data("units");
  var sizes      = $(row).attr("item-sizes");



  $("#modal_item_title").text(title);

  $('#modal_item_qty').val(qty);
  $('#modal_item_price').val(price);

  $("#modal_item_sizes").text(sizes);

  var $sel_qty_unit   = $("#modal_item_qty_unit");
  var $sel_price_unit = $("#modal_item_price_unit");

  $sel_qty_unit.empty(); // remove all options
  $sel_price_unit.empty(); // remove all options

  $.each(units, function(key,val) {

    var is_selected = ""
    if (qty_unit == key) {is_selected = ' selected'} 
    $sel_qty_unit.append($("<option"+is_selected+"></option>").attr("value", key).text(val));

    var is_selected = ""
    if (price_unit == key) {is_selected = ' selected'} 
    $sel_price_unit.append($("<option"+is_selected+"></option>").attr("value", key).text(val));

  });


  // $('#order_details').attr('item-row-id', row_id);
  $('#order_details').attr('item-material-sid', material_sid);

  updateItemTotal();

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


$("input[type='number']").click(function () {
  this.select();
});


$("tr[data-toggle='modal']").click(function () { 

    var obj = $(this)[0];

    updateItemInModal(obj);

});



// add all items that were selected via hidden input fields to the submit form

  $("#po_form").submit( function(eventObj) {


    var sel_ids = $("#material_ids").val();


    var item_qtys        = []
    var item_prices      = []
    var item_qty_units   = []
    var item_price_units = []
    var item_totals      = []

    var order_total = 0;

    for (var i in sel_ids){

      var row = $("tr[item-material-sid='"+sel_ids[i]+"']");

      var item_qty        = $(row).attr("item-qty");
      var item_qty_unit   = $(row).attr("item-qty-unit");
      var item_price      = $(row).attr("item-price");
      var item_price_unit = $(row).attr("item-price-unit");
      var item_total      = $(row).attr("item-total");


      item_qtys.push(item_qty);
      item_prices.push(item_price);
      item_qty_units.push(item_qty_unit);
      item_price_units.push(item_price_unit);
      item_totals.push(item_total);

      order_total = order_total + parseFloat(item_total);

    }


      $('<input />').attr('type', 'hidden')
          .attr('name', "item_qtys")
          .attr('value', item_qtys)
          .appendTo('#po_form');

      $('<input />').attr('type', 'hidden')
          .attr('name', "item_prices")
          .attr('value', item_prices)
          .appendTo('#po_form');

      $('<input />').attr('type', 'hidden')
          .attr('name', "item_qty_units")
          .attr('value', item_qty_units)
          .appendTo('#po_form');

      $('<input />').attr('type', 'hidden')
          .attr('name', "item_price_units")
          .attr('value', item_price_units)
          .appendTo('#po_form');

      $('<input />').attr('type', 'hidden')
          .attr('name', "item_totals")
          .attr('value', item_totals)
          .appendTo('#po_form');


      $('<input />').attr('type', 'hidden')
          .attr('name', "total")
          .attr('value', order_total.toFixed(2))
          .appendTo('#po_form');



      return true;
  });



}



</script>

    <!-- YOUR CONTENT ENDS HERE -->
