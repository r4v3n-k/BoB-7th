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

$sql = "select w_id, w_name, w_phone from wholesaler";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
//while($list = $res->fetch_assoc());
//$list['column_name']
?>
