<?php
header("content-type:text/html; charset=UTF-8");
include '../../lib/functions.php';
$db = dbconn();
$member = member();
extract($POST);
$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "delete from reply where b_id={$b_id}";
$db->query($sql) or trigger_error($db->error."[$sql]");
$sql = "update from question_and_ans set num_of_reply=num_of_reply-1";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("수정되었습니다.", 0);
?>
