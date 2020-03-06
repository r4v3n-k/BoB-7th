<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST);

$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "";
if (empty($g_in_date)) {
$sql = "insert into goods(g_class, g_name, g_price, g_amt, wh_id) values ({$g_class}, '"
    .$db->real_escape_string($g_name)."', {$g_price}, {$g_amt}, {$wh_id})";
} else {
$sql = "insert into goods(g_class, g_name, g_price, g_amt, g_in_date, g_out_date, wh_id) values ({$g_class}, '"
    .$db->real_escape_string($g_name)."', {$g_price}, {$g_amt}, {$g_in_date}, {$g_out_date}, {$wh_id});";
}
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("물품이 등록되었습니다.", 2);
?>
