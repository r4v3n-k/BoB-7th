

<HTML><HEAD><TITLE>[ADMIN]Camel007</TITLE>
<link rel="stylesheet" href="/td.css" type="text/css">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
</HEAD>
<body leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
<table width=810 border=5 cellpadding="10" cellspacing="5" bordercolor="#DDDDDD" height="100%">
<tr bgcolor="#50C2FF"> 
   <td colspan=2 align=center height="40"><font size=5><b><font color="#FFFFFF"><left><a href='#'><font size=1></a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</left>관리자페이지</font></b></font></td>
  
  </tr>
     
  
  <tr bgcolor="#FFFFFF"> 
  <td valign=top width="15%" bgcolor="#F2F2F2"> 
    <TABLE>
    <TR>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
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
  <td valign=top width="85%"><font size=1><b>[ 회원관리 ]<b><BR>
    
<script>
function order(stat,c_stat)
{ 
      location.replace("/admin/order/index.asp?cmd=list&stat="+stat+"&c_stat="+c_stat)
  
}
      
<script>
function del_ok()
{ 
    if (confirm("정말로 탈퇴하시겠습니까?..") ) {
      document.myform2.submit();
    }
}
</script>
<table width="100%" border="0" cellspacing="0" cellpadding="0" align="center">
<form name=form10 method=post action="index.asp">
<input type=hidden name='sr' value='yes'>
<input type=hidden name='cmd' value=''>
  <tr> 
  <td height="30" bgcolor="#FFFFFF" class='css1'><font size=1>전체회원&nbsp;20000명&nbsp;/&nbsp;오늘가입자&nbsp;30명</td>
    <td height="30" bgcolor="#FFFFFF"><div align="right">
        <SELECT name=k>
          <option value="mem_name" >선택</option>
          <option value="mem_name" >이름</option>
          <option value="mem_id" >ID </option>
          <option value="mem_email" >E-mail </option>
        </SELECT>
        <font color="#333333"><font face="돋움" size="1"> 
        <input type="text" name="w" value="" size="15" maxlength="8" style="background-color:FFFFFF; BORDER-BOTTOM: rgb(204,204,204) 1px solid; BORDER-LEFT: rgb(204,204,204) 1px solid; BORDER-RIGHT: rgb(204,204,204) 1px solid; BORDER-TOP: rgb(204,204,204) 1px solid" >
        <input type="image" src="/image/button/search.jpg" align='absmiddle'></font></font> </div></td>
  </tr>
 </form>
  <tr>
    <td colspan=2>
    <TABLE class=shopmode cellSpacing=1 cellPadding=1 width=100% 
            align=center bgColor=#8DB6B6 border=0>
        <FORM name=myform2 method=post action='member_del.asp'>
    <input type='hidden' name='cmd2' value='all'>
          <TR height=30 bgcolor="C7E5E5"> 
            <TD width=20> 
              <DIV align=center> 
                  <INPUT type=checkbox 
                  name=checkboxAll>
                </DIV></TD>
            <TD width=70> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>아이디</B></font></DIV></TD>
              
            <TD width=50> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>이름</B></font></DIV>
            </TD>
              
            <TD width=110> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>전화</B></font></DIV></TD>
              
              <TD width=150> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>주소</B></font></DIV></TD>
            <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>E-mail</B></font></DIV></TD>
        
            <TD width=70> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>구매총액</B></font></DIV>
            </TD>
              
            <TD width=70> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>가입날짜</B></font></DIV>
            </TD>
             <TD width=70> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><B>회원정보</B></font></DIV>
            </TD>
            
            <TR bgColor="#FFFFFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value='jaejin'>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>jaejin</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">최재진</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-7387-1122</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>경기도 의정부시 민락동</a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>jaejin@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>50000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2010/03/30</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>
            
            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value='bsj'>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>bsj</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">방수정</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-2560-1279</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>서울특별시 노원구 </a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>bsj@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>35000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2014/07/03</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>

            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>Ljink</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">이진경</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-5143-7298</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>경기도 남양주시 호평동</a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>Ljink@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>78000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2012/05/16</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>
            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>kimjh</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">김재형</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-2789-9910</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>서울특별시 도곡동</a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>kimjh@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>30000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2018/05/16</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>

            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>kssk</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">김성지</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-6178-9783</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>서울특별시 가산동 </a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>kssk@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>60000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2015/07/16</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>

            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>kEj</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">권은진</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-8456-5248</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>서울특별시 동대문구</a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>kEj@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>57000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2015/01/09</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>

            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>kimjh</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">김재희</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-5648-8562</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>제주특별시 서귀포시 </a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>kimjh@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>63000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2011/08/16</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>

            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>jisu</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">최지수</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-9260-1263</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>서울특별시 중랑구 </a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>jisu@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>100000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2011/05/18</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>

            <TR bgColor="#F0FBFF"> 
              <TD> 
              <DIV align=center> 
        <INPUT type=checkbox name='mem_id' value=''>
              </DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=view&mem_id=test2&page=1&w=&k=&sr='>Leesu</a></font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">이수진</font></DIV></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움">010-7156-9845</font></DIV></TD>
              
              <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>서울특별시 중랑구</a></font></TD>
            <TD> <font color="#333333" size="1" face="돋움">&nbsp;&nbsp;<a href='index.asp?cmd=email&gubun=list&mem_id=test2&page=1&w=&k=&sr='>Leesu@gmail.com</a></font></TD>
              <TD> 
              <DIV align=center><font color="#333333" size="1" face="돋움"><a href='index.asp?cmd=point&gubun_page=list&mem_id=test2&page1=1&w=&k=&sr='>35000</a>원</font></DIV>
            </TD>
        
            <TD align="right"> <font color="#333333" size="1" face="돋움">2017/07/29</font>&nbsp;&nbsp;</TD>
              
          </font></DIV></TD>
              <TD> 
              <div align="center"><font face="돋움"><font size="1"><font color="#333333">
              <a href="index.asp?cmd=modify&mem_id=test2&w=&k=&sr=&page=1">수정</a>/<a href="javascript:del_ok()">삭제
        </a></font></font></font></div></TD>
            </TR>
            
            
        </FORM>
      </TABLE></td>
  </tr>
  
</table>

<table width="90%" border="0" cellspacing="3" cellpadding="0" align="center">
  <tr> 
    <td align="center" height="25"> 
  <!--    
      <font size="2" face="돋움" color="#808080"><img src="/image/board/arro1.gif" border=0></font>&nbsp;
   
      <font size="2" face="돋움" color="#808080"><img src="/image/board/arro01.gif" border=0></font>-->
      <font size="2" face="돋움" color="#808080">&nbsp;back</font>&nbsp;
   
         <font size=3 face=돋움 color=#990000>1</font> 
<
      &nbsp; 
          <font size="2" face="돋움" color="#808080"> &nbsp;next </font>&nbsp;<!--<img src="/image/board/arro02.gif" border=0>-->
           

      &nbsp;<font size="2" face="돋움" color="#808080"><!--<img src="/image/board/arro2.gif" border=0>--></font>

    </td>
  </tr>
</table> 
</td>
</tr>
</table>
  </TD>
</TR>
</TABLE>
</BODY>
</HTML>