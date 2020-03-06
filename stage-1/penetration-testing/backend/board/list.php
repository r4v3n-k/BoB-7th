<?php
header("content-type:text/html; charset=UTF-8");
$sql = "select g_id, g_class, g_name, g_price, g_img from goods";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
?>
