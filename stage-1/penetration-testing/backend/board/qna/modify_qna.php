<?php
header("content-type:text/html; charset=UTF-8");
include '../../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST);
$m_id = $member['m_id'];
if (!$m_id) Error("로그인 후 이용가능합니다.", 0);
if (empty($content)) Error("내용을 입력해주세요",0);
$content = strip_tags($content);
$sql = "update question_and_ans set content='".$db->real_escape_string($content)."' where b_id=$b_id and mem_id='".$db->real_escape_string($m_id)."'";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("수정되었습니다.", 4);
?>
