<?php
include'../backend/lib/functions.php';
$db = dbconn();
$member = member();

$m_id = $member['m_id'];
if (!$member) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "select p_id, mem_id, g_id, g_amt, payment, total_discnt, waybill_number, _return, p_date from purchase_list order by p_date desc";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
?>
