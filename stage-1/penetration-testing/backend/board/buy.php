<?php
header("charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
$member = member();
extract($_POST);
if (!$member['m_id']) Error("로그인 해주세요.", 0);

$sql = "select g_amt from goods where g_id=$g_id";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
$tmp = $res->fetch_assoc();
if ($tmp['g_amt'] < $g_cnt || $g_cnt < 1) Error("잘못된 입력입니다.", 0);

$pk = "";
for ($i=0; $i < 10; $i++) $pk .= rand(0, 9);
$pk .= '-';
for ($i=0; $i < 10; $i++) $pk .= rand(0, 9);
$total_discnt = $discnt;
if ($g_cnt >= 3 and $g_cnt < 6) $total_discnt += ($g_cnt * 0.1);
else if ($g_cnt >= 6 and $g_cnt < 8) $total_discnt += ($g_cnt * 0.2);
else if ($g_cnt >= 8 and $g_cnt < 10) $total_discnt += ($g_cnt * 0.3);
else if ($g_cnt >= 10) $total_discnt += ($g_cnt * 0.4);
$payment = ($g_price*$g_cnt)*(1-$total_discnt/100);
$_return = 0;
if ($return == 'on') $_return = 1;
$sql = "insert into purchase_list(p_id, mem_id, g_id, g_amt, payment, total_discnt, _return) values ('"
    .$db->real_escape_string($pk)
		."', {$member['id']}, {$g_id}, {$g_cnt}, {$payment}, {$total_discnt}, {$_return});";
$db->query($sql) or trigger_error($db->error."[$sql]");
$db->close();
Error("구매신청되었습니다. 구매내역은 '마이페이지'를 참조해주세요.", 2);
?>
