<?php
header("content-type:text/html; charset=UTF-8");
include '../../lib/functions.php';
$db = dbconn();
$member = member();
extract($POST);
$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "insert into reply(mem_id, m_name, content, bbs_id) values ('"
    .$db->real_escape_string($mem_id)."', '"
    .$db->real_escape_string($m_name)."', '"
    .$db->real_escape_string($content)."', {$bbs_id})";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();

Error("완료되었습니다.", 0);
?>
