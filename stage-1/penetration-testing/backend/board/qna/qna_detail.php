<?php
header("content-type:text/html; charset=UTF-8");
include 'backend/lib/functions.php';
$member = member();
$db = dbconn();
extract($_GET);
if (!$member || empty($_GET)) Error("잘못된 접근입니다.", 2);
if (!is_numeric($_GET['b_id'])) Error("잘못된 접근입니다.", 2);
$m_id = $member['m_id'];

$sql = "select b_id, mem_id, m_name, reg_date, content from question_and_ans where b_id=$b_id;";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$detail = $res->fetch_assoc();
?>
