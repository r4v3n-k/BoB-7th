<?php
header("content-type:text/html; charset=UTF-8");
include '../../lib/functions.php';
$db = dbconn();
$member = member();
extract($_GET);
if (!$member || empty($_GET)) Error("로그인 후 이용가능합니다.", 0);
if (!is_numeric($b_id)) Error("정상적인 경로로 접근해주세요.", 0);
$m_id = $member['m_id'];
$sql = "delete from question_and_ans where b_id=$b_id and mem_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");

Error("삭제되었습니다.", 4);
?>
