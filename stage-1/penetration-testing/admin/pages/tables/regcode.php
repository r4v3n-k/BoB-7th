<?php require_once $_SERVER['DOCUMENT_ROOT']."/admin/php/connect.php"; ?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Aboda | /Admin/RegCode</title>
  <link rel="shortcut icon" href="/logoicon.png">
  <!-- Tell the browser to be responsive to screen width -->
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <!-- Bootstrap 3.3.6 -->
  <link rel="stylesheet" href="/admin/bootstrap/css/bootstrap.min.css">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
  <!-- Ionicons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/css/ionicons.min.css">
  <!-- DataTables -->
  <link rel="stylesheet" href="/admin/plugins/datatables/dataTables.bootstrap.css">
  <!-- Theme style -->
  <link rel="stylesheet" href="/admin/dist/css/AdminLTE.min.css">
  <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
  <link rel="stylesheet" href="/admin/dist/css/skins/_all-skins.min.css">

  <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
</head>
<body class="hold-transition skin-blue sidebar-mini">
<div class="wrapper">
  <?php require_once $_SERVER['DOCUMENT_ROOT']."/admin/pages/header.php"; ?>

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Register Code Table
        <small>code info</small>
      </h1>
      <ol class="breadcrumb">
        <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
        <li><a href="#">Tables</a></li>
        <li class="active">Free Consultation</li>
      </ol>
    </section>

    <!-- Main content -->
    <section class="content">
      <div class="row">
        <div class="col-xs-12">
          <div class="box">
            <div class="box-header">
              <h3 class="box-title">Hover Data Table</h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body">
              <table id="example2" class="table table-bordered table-hover">
                <thead>
                <tr>
                  <th>ID</th>
                  <th>Code</th>
                  <th>Group</th>
                  <th>Permission</th>
                  <th>삭제</th>
                </tr>
                </thead>
                <tbody class="regcode-table">
                <?php
                
                $result = $mysqli->query("SELECT * FROM `regcode`");
                while($row = mysqli_fetch_array($result)) {
                  echo "
                  <tr>
                    <td>$row[id]</td>
                    <td>$row[code]</td>
                    <td>$row[group]</td>
                    <td>$row[permission]</td>
                    <td><button class='btn btn-danger del-regcode' data-pdp-id='$row[id]'></button></td>
                  </tr>

                  ";
                }
                ?>
                </tbody>
                <tfoot>
                <tr>
                  <th>ID</th>
                  <th>Code</th>
                  <th>Group</th>
                  <th>Permission</th>
                  <th>삭제</th>
                </tr>
                </tfoot>
              </table>
            </div>
            <!-- /.box-body -->
          </div>
          <!-- /.box -->

          <div class="box">
            <div class="box-header">
              <h3 class="box-title">Register Code ADD</h3>
            </div>
            <div class="box-body">

              <form role="form" method="post" action="/admin/php/addRegcode.php">

                <div class="form-group">
                  <label>Count</label>
                  <input type="text" name="count" class="form-control" placeholder="Count" required>
                </div>

                <div class="form-group">
                  <label>Group</label>
                  <input type="text" name="group" class="form-control" placeholder="Group" required>
                </div>

                <div class="form-group">
                  <label>Permission</label>
                  <input type="text" name="per" class="form-control" placeholder="Permission" required>
                </div>

                <div class="box-footer">
                  <button type="submit" class="btn btn-primary">Submit</button>
                </div>
              </form>
            </div>
          </div>

        </div>
        <!-- /.col -->
      </div>
      <!-- /.row -->
    </section>
    <!-- /.content -->
  </div>
  <!-- /.content-wrapper -->

</div>
<!-- ./wrapper -->

<!-- jQuery 2.2.3 -->
<script src="/admin/plugins/jQuery/jquery-2.2.3.min.js"></script>
<!-- Bootstrap 3.3.6 -->
<script src="/admin/bootstrap/js/bootstrap.min.js"></script>
<!-- DataTables -->
<script src="/admin/plugins/datatables/jquery.dataTables.min.js"></script>
<script src="/admin/plugins/datatables/dataTables.bootstrap.min.js"></script>
<!-- SlimScroll -->
<script src="/admin/plugins/slimScroll/jquery.slimscroll.min.js"></script>
<!-- FastClick -->
<script src="/admin/plugins/fastclick/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="/admin/dist/js/app.min.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="/admin/dist/js/demo.js"></script>
<!-- page script -->
<script>
  $(function () {
    $('#example2').DataTable({
      "paging": true,
      "lengthChange": true,
      "searching": true,
      "ordering": true,
      "info": true,
      "autoWidth": true
    });
  });

  $('button.del-regcode').click(function() {
    if(confirm('Is ture Delete Consultation?')) {
      $('body').append('<form id="del-form" method="post" action="/admin/php/delRegcode.php"><input name="id" value="'+$(this).attr('data-pdp-id')+'"></form>');
      $('#del-form').submit();
    }
  })
</script>
</body>
</html>