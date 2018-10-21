	
	
    <!-- YOUR CONTENT STARTS HERE -->

    <nav class="navbar navbar-inverse navbar-light bg-faded">

      <button class="navbar-toggler mr-4" type="button" data-toggle="collapse" data-target="#nav-content" aria-controls="nav-content" aria-expanded="false" aria-label="Toggle navigation">

        <span class="navbar-toggler-icon"></span>

      </button>

      <!-- Brand -->
      <h2 class="navbar-brand">_('Purchase Orders')</h2>

      <button class="btn btn-outline-secondary ml-4" type="button" onclick="window.location='insert/0'">
        <i class="fas fa-edit"></i>
      </button>


      <!-- Links -->
% include('hamburger_menu.tpl')

    </nav>

    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th colspan="4">
            <form>
              <span><i class="fas fa-search"></i></span>
              <input id="search-string" onkeyup="filterList();" type="text" class="ml-2 mr-2"/>
              <span><i class="fas fa-clipboard-list"></i></span>
              <span id="list_count" class="badge badge-secondary badge-pill">{{items_count}}</span>
            </form>
          </th>
        </tr>
      </thead>
      <tbody style="cursor:pointer">

%for item in list_items:


        <tr class="search-item" searchkey="{{item.status}}" onclick="window.location.assign('update/{{item._id}}');">
          <td class="text-left">{{item.datetime}}</td>
          <td class="text-left">{{item.status}}</td>
          <td class="text-left">{{item.supplier.name_cn if locale=='zh_CN' else item.supplier.name_en}}</td>
          <td class="text-right">{{item.total}} 元</td>
        </tr>

%end

      </tbody>
    </table>
    <br/>
    <br/>


<script>       



function updateResultCount(){
  
  var items_count = $('tr.search-item:visible').length;

  $('#list_count').text(items_count);

}



function filterList(){

var ss = $('#search-string').val().toLowerCase()

if (ss=="") {
  $('tr.search-item').show();
} else {
  $('tr.search-item').hide();
  $('tr[searchkey*="'+ss+'"]').show()  
}



updateResultCount();

}


function initPage(){

}

</script>

    <!-- YOUR CONTENT ENDS HERE -->
