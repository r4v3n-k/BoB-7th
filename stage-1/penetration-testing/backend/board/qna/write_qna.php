<?php
header("content-type:text/html; charset=UTF-8");
include '../../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST);
$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);
if (empty($content)) Error("내용을 입력해주세요.", 0);
$content = strip_tags($content);
$sql = "insert into question_and_ans(mem_id, m_name, content) values ('"
    .$db->real_escape_string($m_id)."', '"
    .$db->real_escape_string($member['m_name'])."', '"
    .$db->real_escape_string($content)."')";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("완료되었습니다.", 2);
?>
