<?php
include '../backend/lib/functions.php';
$db = dbconn();
$member = member();

$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$level = $res->fetch_assoc();
if ($level['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "select t_id, ws_id, gd_id, g_amt, g_price, g_in_date, g_out_date from trading_list order by t_id asc";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
//while($list = $res->fetch_assoc());
//$list['column_name'] --> w_id, g_id
?>
