	
	
    <!-- YOUR CONTENT STARTS HERE -->

    <nav class="navbar navbar-inverse navbar-light bg-faded">

      <button class="navbar-toggler mr-4" type="button" data-toggle="collapse" data-target="#nav-content" aria-controls="nav-content" aria-expanded="false" aria-label="Toggle navigation">

        <span class="navbar-toggler-icon"></span>

      </button>

      <!-- Brand -->
      <h2 class="navbar-brand">_('Products')</h2>

      <h2 class="navbar-brand">_('Youzan')</h2>

      <!-- Links -->
% include('hamburger_menu.tpl')

    </nav>

    <table class="table table-striped table-hover" style="cursor:pointer">
      <thead>
        <tr>
          <th colspan="2" onclick="filter()">
            <form>
              <span><i class="fas fa-search"></i></span>
              <input id="search-string" onkeyup="filterList();" type="text" class="ml-2 mr-2"/>
              <span><i class="fas fa-clipboard-list"></i></span>
              <span id="list_count" class="badge badge-secondary badge-pill">{{items_count}}</span>
            </form>
          </th>
        </tr>
      </thead>
      <tbody>

%for item in list_items:


        <tr class="search-item" searchkey="{{item.id.lower()}}{{item.name.lower()}}">
          <td>{{item.id}}</td>
          <td>{{item.name}}</td>
        </tr>

%end

      </tbody>
    </table>


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
