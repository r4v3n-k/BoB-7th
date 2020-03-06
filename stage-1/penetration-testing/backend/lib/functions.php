<?php
function dbconn() {
    $db = new mysqli("localhost", "root", "bob7&virtual&enterprise", "bob7");
    if ($db->connect_errno) die("Database Connect Failed.");
    return $db;
}

function Error($msg, $errno=1) {
    if ($errno == 1) {
        echo $msg; // just print message
				exit;
    } 
		echo "<script> window.alert(\"{$msg}\");</script>";
		if ($errno == 2) {
				echo "<script> window.location.href=document.referrer; </script>";
		}
		else if ($errno == 3) {
				echo "<script> location.href('login.html'); </script>";
		} else if ($errno == 4) {
				echo "<script> location.href='../../../qna.html'; </script>";
		} else if ($errno == 5) {
				echo "<script> location.href='../../login.html'; </script>";
		}
		else if ($errno == 6) {
				echo "<script> location.href='www.google.com';</script>";
		}
		else {
        echo "<script> history.back(1); </script>";
    }
		exit;
}

function member() {
    global $db;
    if (empty($_COOKIE["COOKIES"])) return null;
    $cookie = explode(",", $_COOKIE["COOKIES"]);
    // cookie[0] -> id
    // cookie[1] -> pw
    $query = "select id, m_name, m_id, m_pw, m_email, m_addr, m_phone  from member where m_id='{$cookie[0]}'";
    $result = $db->query($query) or trigger_error($db->error."[$query]");
    $member = $result->fetch_assoc();
		if ($member['m_pw'] != $cookie[1]) Error("로그인 후 이용해주세요.", 6);
    return $member;
}
$db = dbconn()
?>
