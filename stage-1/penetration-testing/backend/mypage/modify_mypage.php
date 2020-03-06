<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
extract($_POST);
$db = dbconn();
$member = member();
$m_id = $member['m_id'];
if (!$m_id) Error("로그인 후 이용해주세요.", 0);
if (!$m_phone || $m_email || $m_addr) Error("빈 칸을 모두 채워주세요.",0);
if (!preg_match("/^\d{3}\d{3,4}\d{4}$/", $m_phone)) Error("정확한 휴대폰 번호를 입력해주세요.", 0);
if (!preg_match("/\w+@\w+\.\w+/", $m_email)) Error("이메일 형식을 맞춰주세요.", 0);

$sql = "update member set m_phone='"
.$db->real_escape_string($m_phone)."', m_email='"
.$db->real_escape_string($m_email)."', m_addr='"
.$db->real_escape_string($m_addr)."' where id={$member['id']}";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("수정되었습니다.", 2);
?>
