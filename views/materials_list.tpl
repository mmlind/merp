	
	
    <!-- YOUR CONTENT STARTS HERE -->

    <nav class="navbar navbar-inverse navbar-light bg-faded">

      <button class="navbar-toggler mr-4" type="button" data-toggle="collapse" data-target="#nav-content" aria-controls="nav-content" aria-expanded="false" aria-label="Toggle navigation">

        <span class="navbar-toggler-icon"></span>

      </button>

      <!-- Brand -->
      <h2 class="navbar-brand">_('Materials')</h2>

      <button class="btn btn-outline-secondary ml-4" type="button" onclick="window.location='upsert/0'">
        <i class="fas fa-edit"></i>
      </button>


      <!-- Links -->
% include('hamburger_menu.tpl')

    </nav>





    <nav id="scrollspy-nav" class="navbar navbar-default">


      <div class="btn-group-toggle" data-toggle="buttons">

%for mg in mgs:
        <label class="btn btn-primary">
          <input type="checkbox" id="{{mg._id}}" autocomplete="off"/>
{{mg.name_cn if locale=='zh_CN' else mg.name_en}}
        </label>
%end

      </div>


    </nav>







    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th colspan="3">
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

        <tr class="search-item" searchkey="{{item.id.lower()}}{{item.name_cn.lower()}}{{item.name_en.lower()}}" searchgroup="{{item.mg_id}}" onclick="window.location.assign('upsert/{{item._id}}');">
          <td>{{item.id}}</td>
          <td>{{item.name_cn}}</td>
          <td>{{item.name_en}}</td>
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

var numberOfChecked = $('input:checkbox:checked').length;
var totalCheckboxes = $('input:checkbox').length;


if (numberOfChecked>0 || ss!="") {

  
    $('tr.search-item').hide();

    $("tr.search-item").each(function() {

      var mgid = $(this).attr('searchgroup');

      if (mgid) {

        var mg_selected = ($('#'+mgid).prop('checked'))

        // alert($(this).attr('searchkey')+'==='+mg_selected+'==='+$(this).attr('searchkey').includes(ss));

        if ((mg_selected || numberOfChecked==0) && ($(this).attr('searchkey').includes(ss) || ss=='' )) {
          $(this).show()
        } 


      }


    });


} else {
  $('tr.search-item').show();  
}




updateResultCount();

}


function initPage(){

  $('input[type=checkbox]').change(function() {
    filterList();
})

}


</script>

    <!-- YOUR CONTENT ENDS HERE -->
