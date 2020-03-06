<?php
header("content-type:text/html; charset=UTF-8");
include '../../lib/functions.php';
$db = dbconn();
$member = member();
extract($POST);
$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "update from reply set content='"
    .$db->real_escape_string($content)."' where b_id={$b_id} and bbs_id={$bbs_id}";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();

Error("수정되었습니다.", 0);
?>
