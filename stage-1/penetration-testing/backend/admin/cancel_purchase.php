<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST); // --> p_id

$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "delete from purchase_list where p_id='".$db->real_escape_string($p_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
Error("주문이 취소되었습니다.", 2);
?>
