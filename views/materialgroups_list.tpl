	
	
    <!-- YOUR CONTENT STARTS HERE -->

    <nav class="navbar navbar-inverse navbar-light bg-faded">

      <button class="navbar-toggler mr-4" type="button" data-toggle="collapse" data-target="#nav-content" aria-controls="nav-content" aria-expanded="false" aria-label="Toggle navigation">

        <span class="navbar-toggler-icon"></span>

      </button>

      <!-- Brand -->
      <h2 class="navbar-brand">_('Material Groups')</h2>

      <button class="btn btn-outline-secondary ml-4" type="button" onclick="window.location='upsert/0'">
        <i class="fas fa-edit"></i>
      </button>


      <!-- Links -->
% include('hamburger_menu.tpl')

    </nav>

    <table class="table table-striped table-hover" style="cursor:pointer">
      <thead>
        <tr>
          <th colspan="3">_('All') <span class="badge badge-secondary badge-pill">{{items_count}}</span>
          </th>
        </tr>
      </thead>
      <tbody>

%for item in list_items:

        <tr onclick="window.location.assign('upsert/{{item._id}}');">
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

function initPage(){

}

</script>

    <!-- YOUR CONTENT ENDS HERE -->
