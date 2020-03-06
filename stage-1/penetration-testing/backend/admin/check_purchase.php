<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST); // --> mem_id, p_id, g_id, g_amt, waybill_number

if (!$member) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "update purchase_list set waybill_number='"
    .$db->real_escape_string($waybill_number)."' where p_id='"
		.$db->real_escape_string($p_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$sql = "update goods set g_amt=g_amt-$g_amt where g_id=$g_id";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
Error("입금확인되었습니다.", 2);
?>
