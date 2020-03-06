<?php
include '../backend/lib/functions.php';
$db = dbconn();
$member = member();

$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "select g_id, g_class, g_name, g_price, g_amt, g_in_date, g_out_date, wh_id from goods";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$sql2 = "select h_id, h_phone, h_addr from warehouse";
$res2 = $db->query($sql2) or trigger_error($db->error."[$sql2]");
$warehouse = [];
while($list2 = $res2->fetch_assoc()) {
	array_push($warehouse, $list2);
}
?>
