<?php
header("charset=UTF-8");
$db = dbconn();
$member = member();
extract($_GET);

if (!$member) $member['id']=0;
if (empty($_GET)) Error("잘못된 접근입니다.",2);
if (!is_numeric($_GET['g_id'])) Error("잘못된 접근입니다.", 2);
$sql = "select g_id, g_name, g_price, g_amt, g_img from goods where g_id=$g_id";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$detail = $res->fetch_assoc();
if (empty($detail)) Error("잘못된 접근입니다.", 2);
$sql2 = "select g_amt from purchase_list where mem_id={$member['id']} and g_id={$g_id} order by p_date desc limit 1";
$res2 = $db->query($sql2) or trigger_error($db->error."[$sql2]");
$list = $res2->fetch_assoc();
$amt = $list['g_amt'];
$accu_discnt = 0;
if ($amt >= 3 and $amt < 6) $accu_discnt = 1.5;
else if ($amt >= 6 and $amt < 8) $accu_discnt = 5;
else if ($amt >= 8 and $amt < 10) $accu_discnt = 7.5;
else if ($amt >= 10) $accu_discnt = 8.6;
?>
