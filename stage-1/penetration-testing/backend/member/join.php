<?php
header("charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
extract($_POST);

if (!$m_name || !$m_email || !$m_pw || !$m_pwchk || !$m_addr || !$m_phone)
    Error("빈 칸을 모두 채워주세요.", 0);
if ((strlen($m_name) < 2)) Error("이름은 2자 이상이어야 합니다.", 0);
if (strlen($m_id) < 6 || $m_id > 20) Error("아이디는 길이가 6자~20자 사이어야 합니다.", 0);
else if (!preg_match("/[a-z]\w+[0-9]/", $m_id)) Error("아이디는 숫자와 영문자 조합으로 사용해야 합니다.", 0);
$sql = "select m_id from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
if ($res->num_rows) Error("이미 존재하는 아이디입니다.", 0);
if (!preg_match("/^\d{3}\d{3,4}\d{4}$/", $m_phone)) Error("정확한 휴대폰 번호를 입력해주세요.", 0);
if (!preg_match("/\w+@\w+\.\w+/", $m_email)) Error("이메일 형식을 맞춰주세요.", 0);
if (strlen($m_pw) < 10) Error("비밀번호는 최소 10자 이상이어야 합니다.", 0);
if (!preg_match("/^[a-zA-Z0-9]{10,15}$/",$m_pw)) Error("비밀번호는 숫자와 영문자 조합으로 10~15자리를 사용해야 합니다.", 0);
if (strcmp($m_pw, $m_pwchk) !== 0) 
    Error("입력하신 비밀번호와 확인용 비밀번호가 일치하지 않습니다.", 0);
// addr preg match..--> ??
$ip = getenv("REMOTE_ADDR");
$query = "insert into member(m_name, m_id, m_pw, m_email, m_addr, m_phone) values ('"
    .$db->real_escape_string($m_name)."', '"
    .$db->real_escape_string($m_id)."', '"
    .$db->real_escape_string(md5($m_pw))."', '"
    .$db->real_escape_string($m_email)."', '"
    .$db->real_escape_string($m_addr)."', '"
    .$db->real_escape_string($m_phone)."')";
$db->query($query) or trigger_error($db->error."[$query]");
$db->close();
Error($m_name."님, 회원가입이 완료되었습니다.", 5);
?>
