

<HTML><HEAD><TITLE></TITLE>
<link rel="stylesheet" href="/td.css" type="text/css">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrom=1">
  <title></title>
  <!-- Tell the browser to be responsive to screen width -->
  <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
  <!-- Bootstrap 3.3.6 -->
  <link rel="stylesheet" href="/admin/bootstrap/css/bootstrap.min.css">
  <!-- Font Awesome -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.5.0/css/font-awesome.min.css">
  <!-- Ionicons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/ionicons/2.0.1/css/ionicons.min.css">
  <!-- DataTables -->
  <link rel="stylesheet" href="/admin/plugins/datatables/dataTables.bootstrap.css">
  <!-- Theme style -->
  <link rel="stylesheet" href="/admin/dist/css/AdminLTE.min.css">
  <!-- AdminLTE Skins. Choose a skin from the css/skins
       folder instead of downloading all of them to reduce the load. -->
  <link rel="stylesheet" href="/admin/dist/css/skins/_all-skins.min.css">
</HEAD>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width=810 border=5 cellpadding="10" cellspacing="5" bordercolor="#DDDDDD" height="100%">
<tr bgcolor="#50C2FF"> 
      
    <td colspan=2 align=center height="40"><font size=5><b><font color="#FFFFFF"><left><a href='#'><font size=1><div align=left href="C:\Users\jaejin\Desktop\보노보노\VirtualEnterprise\frontend\main.html">bobmall</a></div></left>관리자페이지</font></b></font></td>
  
  </tr>
     
  
  <tr bgcolor="#FFFFFF"> 
  <td valign=top width="15%" bgcolor="#F2F2F2"> 
    <TABLE>
    <TR>
      <TD><a href='#'><font size=1>관리자정보변경</a></TD>
    </TR>
    <TR>
      <TD><a href='#'><font size=1>회원관리</a></TD>
    </TR>
    <TR>
      <TD><a href='#'><font size=1>카테고리관리</a></TD>
    </TR>
    <TR>
      <TD><a href='#'><font size=1>상품관리</a></TD>
    </TR>
    <TR>
      <TD><a href='#'><font size=1>삭제상품관리</a></TD>
    </TR>
    <TR>
      <TD><a href='#'><font size=1>주문관리</a></TD>
    </TR>

  <!-- 
    <TR>
      <TD><a href='/admin/banpum/index.asp'>반품/환불정보</a></TD>
    </TR>-->
    
    <TR>
      <TD><a href='/admin/popup/index.asp'><font size=1>팝업관리</a></TD>
    </TR>
    <TR>
      <TD><a href='/admin/statistics/counter.asp'><font size=1>기간별매출통계</a></TD>
    </TR>
    <TR>
      <TD><a href='/admin/statistics/goods.asp'><font size=1>기간별상품통계</a></TD>
    </TR>
    <TR>
      <TD><a href='/admin/counter/index.asp'><font size=1>접속통계</a></TD>
    </TR>
    <TR>
      <TD><a href='/admin/admin_logout.asp'><font size=1>관리자로그아웃</a></TD>
    </TR>
</TABLE>
  </TD>
  <td valign=top width="85%"><font size=1><b>[ 주문관리 ]<b><BR>
    
<script>
function order(stat,c_stat)
{ 
      location.replace("/admin/order/index.asp?cmd=list&stat="+stat+"&c_stat="+c_stat)
  
}

</script>
<table width="100%" border="0" cellspacing="0" cellpadding="0" align=center>
  <tr> 
    <td height="30" bgcolor="DEDBDE"><font size=1><strong>
    <INPUT 
      type=radio CHECKED value=all name=member onclick="javascript:order('yes','yes');">
        전체주문확인 
        <INPUT 
      type=radio  value=all name=member onclick="javascript:order('A','');">
        주문확인 
    <INPUT 
      type=radio  value=all name=member onclick="javascript:order('B','');">
        입금확인 
        <INPUT 
      type=radio  value=all name=member onclick="javascript:order('C','');">
        배송중 
        <INPUT 
      type=radio  value=all name=member onclick="javascript:order('D','');">
        배송완료 
        <INPUT 
      type=radio  value=all name=member onclick="javascript:order('','Y');">
        주문취소 </strong></td>
  </tr>
  <tr> 
    <td>&nbsp;</td>
  </tr>
  <tr> 
    <td height="30" bgcolor="DEDBDE"><font size=1><strong>[주문검색]</strong></td>
  </tr>
  <tr> 
    <td height="30">
    <TABLE cellSpacing=1 cellPadding=2 width="100%" align=center bgColor=#b8b8b8 border=0>
          <TR> 
            <TD height="60" bgColor=#FFFFFF><font size=1>
        <form name="form1" method="post" action="/admin/order/index.asp">
          <input type="hidden" name="cmd" value="list">
                <input type="hidden" name="sr" value="yes">
          <input type="hidden" name="stat" value="">
          <input type="hidden" name="c_stat" value="">
          <select name="k">
          <option value="mem_id" >ID선택</option>
                <option value="ordname" >이름선택</option>
                  </SELECT>
                  : <input type="text" name="w" value="" size="15" maxlength="8"><a href='javascript:document.form1.submit();'>검색</a>
                  </form>
          <form name="form2" method="post" action="/admin/order/index.asp">
          <input type="hidden" name="cmd" value="list">
          <input type="hidden" name="stat" value="">
          <input type="hidden" name="c_stat" value="">
                  <input type="hidden" name="ymd" value="yes">
                <input type="text" onkeypress='IsNumber()' name="buy_s_y" size="4" maxlength="4" value="2018"> 년 
          <select name="buy_s_m">
        <option value='01'>01</option><option value='02'>02</option><option value='03'>03</option><option value='04'>04</option><option value='05'>05</option><option value='06'>06</option><option value='07' selected>07</option><option value='08'>08</option><option value='09'>09</option><option value='10'>10</option><option value='11'>11</option><option value='12'>12</option>
                  </select>&nbsp;월
                  <select name="buy_s_d">
        <option value='01'>01</option><option value='02'>02</option><option value='03'>03</option><option value='04'>04</option><option value='05'>05</option><option value='06'>06</option><option value='07'>07</option><option value='08'>08</option><option value='09'>09</option><option value='10'>10</option><option value='11'>11</option><option value='12'>12</option><option value='13'>13</option><option value='14'>14</option><option value='15'>15</option><option value='16'>16</option><option value='17'>17</option><option value='18'>18</option><option value='19'>19</option><option value='20'>20</option><option value='21'>21</option><option value='22'>22</option><option value='23'>23</option><option value='24'>24</option><option value='25'>25</option><option value='26'>26</option><option value='27'>27</option><option value='28'>28</option><option value='29'>29</option><option value='30' selected>30</option><option value='31'>31</option>
                  </SELECT>&nbsp;일 ~ 
                  <input type="text" onkeypress='IsNumber()' name="buy_e_y" size="4" maxlength="4" value="2018">&nbsp;년
                   <select name="buy_e_m">
        <option value='01'>01</option><option value='02'>02</option><option value='03'>03</option><option value='04'>04</option><option value='05'>05</option><option value='06'>06</option><option value='07' selected>07</option><option value='08'>08</option><option value='09'>09</option><option value='10'>10</option><option value='11'>11</option><option value='12'>12</option>
                  </SELECT>&nbsp;월
                  <select name="buy_e_d">
        <option value='01'>01</option><option value='02'>02</option><option value='03'>03</option><option value='04'>04</option><option value='05'>05</option><option value='06'>06</option><option value='07'>07</option><option value='08'>08</option><option value='09'>09</option><option value='10'>10</option><option value='11'>11</option><option value='12'>12</option><option value='13'>13</option><option value='14'>14</option><option value='15'>15</option><option value='16'>16</option><option value='17'>17</option><option value='18'>18</option><option value='19'>19</option><option value='20'>20</option><option value='21'>21</option><option value='22'>22</option><option value='23'>23</option><option value='24'>24</option><option value='25'>25</option><option value='26'>26</option><option value='27'>27</option><option value='28'>28</option><option value='29'>29</option><option value='30' selected>30</option><option value='31'>31</option>
                  </SELECT>&nbsp;일 까지 <a href='javascript:document.form2.submit();'>검색</a>
          </TD></form>
          </TR>
      </TABLE></td>
  </tr>
  
  <tr> 
    <td height="40" align=right><div align=right><font size=1>
    
      오늘주문건수 : 0건 / 오늘의 배송 : 0건 
    
        / 주문금액 : 0원 / 결제금액 : 0원</div></td>
  </tr>
  <tr> 
    <td height="50" align=center>
     <TABLE width="100%" cellSpacing=1 cellPadding=1 align=center bgColor=#b8b8b8 border=0>
        <FORM name=myform2 method=post>
            <TR height=30> 
        <TD width="6%" height="25" bgColor=DEDBDE align=center><div align=center><font size=1><B>선택</B></div></TD>
              <TD width="10%" height="25" bgColor=DEDBDE align=center><div align=center><font size=1><B>주문번호</B></div></TD>
              <TD width="10%" height="25" bgColor=DEDBDE align=center><div align=center><font size=1><B>주문자</B></div></TD>      
              <TD width="15%" height="25" bgColor=DEDBDE align=center><div align=center><font size=1><B>결제방법&nbsp;/ &nbsp;상태</B></div></TD>
              <TD width="12%" height="25" bgColor=DEDBDE align=center><div align=center><font size=1><B>결제금액</B></div></TD>
        <TD width="15%" height="25" bgColor=DEDBDE align=center><div align=center><font size=1><B>주문일시</B></div></TD>
        
            </TR>

        <TR bgColor="#FFFFFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value='jaejin'>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='><center>183506</center></a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">최재진</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">무통장입금&nbsp;/ &nbsp;결제</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>50000</a>원</font></DIV>
            </TD>
        
            <TD align="center"> <font color="#333333" size="1" face="돋움">2018/05/06</div></font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              
            </TR>
            
                  
        </FORM>
      </TABLE></td>
  </tr>
 
</div></td>
  </tr>
</table>

  </TD>
</TR>
</TABLE>
</BODY>
</HTML>
