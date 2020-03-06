<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
extract($_POST);
$db = dbconn();
$member = member();
$m_id = $member['m_id'];
if (!$m_id) Error("로그인 후 이용해주세요.", 0);
if (!$m_phone || !$m_email || !$m_addr) Error("빈 칸을 모두 채워주세요.",0);
if ((strlen($m_name) < 2)) Error("이름은 2자 이상이어야 합니다.", 0);
if (!preg_match("/^\d{3}\d{3,4}\d{4}$/", $m_phone)) Error("정확한 휴대폰 번호를 입력해주세요.", 0);
if (!preg_match("/\w+@\w+\.\w+/", $m_email)) Error("이메일 형식을 맞춰주세요.", 0);

if (!$m_pw and !$chk_pw) {
$sql = "update member set m_name='"
.$db->real_escape_string($m_name)."', m_phone='"
.$db->real_escape_string($m_phone)."', m_email='"
.$db->real_escape_string($m_email)."', m_addr='"
.$db->real_escape_string($m_addr)."' where id={$member['id']}";
} else {
	if (strlen($m_pw) < 10) Error("비밀번호는 최소 10자 이상이어야 합니다.", 0);
	if (!preg_match("/^[a-zA-Z0-9]{10,15}$/",$m_pw)) Error("비밀번호는 숫자와 영문자 조합으로 10~15자리를 사용해야 합니다.", 0);
	if (strcmp($m_pw, $chk_pw) !== 0) 
	    Error("입력하신 비밀번호와 확인용 비밀번호가 일치하지 않습니다.", 0);
	$sql = "update member set m_name='"
	.$db->real_escape_string($m_name)."', m_pw='"
	.$db->real_escape_string(md5($m_pw))."', m_phone='"
	.$db->real_escape_string($m_phone)."', m_email='"
	.$db->real_escape_string($m_email)."', m_addr='"
	.$db->real_escape_string($m_addr)."' where id={$member['id']}";
}

$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("수정되었습니다.", 2);
?>
