<?php
 if (!$member) Error("로그인 후 이용가능합니다.", 0);
$sql = "select b_id, mem_id, m_name, reg_date, content, num_of_replys from question_and_ans order by reg_date asc";
$res = $db->query($sql) or trigger_error($db->error."[$sql]");
?>
