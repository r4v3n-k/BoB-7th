<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST);

if (!preg_match("/^\d{3}\d{4}\d{4}$/", $w_phone)) Error("정확한 번호를 입력해주세요.", 2);
$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 2);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);


$sql = "insert into wholesaler(w_name, w_phone) values ('"
    .$db->real_escape_string($w_name)."', '"
    .$db->real_escape_string($w_phone)."')";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("등록되었습니다.", 2);
?>
