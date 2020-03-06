<?php
header("content-type:text/html; charset=UTF-8");
include '../lib/functions.php';
$db = dbconn();
extract($_POST);

$query = "select m_id, m_pw from member where m_id='".$db->real_escape_string($m_id)."'";
$result = $db->query($query);
$login = $result->fetch_assoc();

if (!$m_id || !$m_pw || ($login['m_pw'] != md5($m_pw)))
    Error("아이디/비밀번호가 일치하지 않습니다.", 0);
else if ($login['m_id'] != $m_id)
    Error("존재하지 않는 아이디입니다.", 0);

if (($m_id == $login['m_id']) && ($login['m_pw'] == md5($m_pw))) {
    $tmp = $login['m_id'].",".$login['m_pw'];
    setcookie("COOKIES", $tmp, time()+60*60*24, "/");
}

$result->free();
$db->close();
?>

<script>
    location.href="../../index.html";
</script>
