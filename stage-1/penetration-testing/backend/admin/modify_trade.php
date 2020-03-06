<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
$member = member();
extract($POST);
$m_id = $member['m_id'];
if (!$m_id) Error("정상적인 경로로 접근해주세요.", 0);
$sql = "select m_level from member where m_id='".$db->real_escape_string($m_id)."'";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$list = $res->fetch_assoc();
if ($list['m_level'] != 0) Error("정상적인 경로로 접근해주세요.", 0);

$sql = "update goods set g_name='".$db->real_escape_string($g_name)
."', g_price=$g_price, g_amt=$g_mat where g_id=$gd_id";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$sql = "update trading_list set g_amt=$g_amt, g_price=$g_price, g_in_date='".$db->real_escape_string($g_in_date)
."', g_out_date='".$db->real_escape_string($g_out_date)."' where t_id=$t_id";

Error("데이터가 삭제되었습니다.", 2);
?>
