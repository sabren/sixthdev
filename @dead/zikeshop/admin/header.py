# just a header

import weblib, zikeshop
weblib.auth.check()
zikeshop.siteID = weblib.auth.user.siteID

print '''\
<html>
<head>
<title>Zikeshop</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<style type="text/css">
<!--
h1 {
  font-family: Impact;
  font-size: 24pt; font-weight: normal;
  padding-bottom: 2px
  }
-->
</style>
</head>
<body bgcolor="#666666">
<table width="600" border="0" align="center" cellspacing="0" cellpadding="2">
  <tr bgcolor="#000000"> 
    <td colspan="4"> <font color="#FFFFFF" face="Impact" size="6">&nbsp;Zike<font color="#00FF66">$</font>hop</font><font color="#FFFFFF"> 
      </font></td>
    <td valign="top" colspan="4" align="right">
      <font size="3" face="arial black" color="#33CCFF">^</font>
      <font size="3" face="arial black">
      <font color="#000000">--</font>
      <font color="#00FF00"><a style="color:#00ff00" href="newsale.py">$</a></font>
      <font color="#000000">--</font>
      <font color="#FFCC00">?</font> 
      <font color="#000000">--</font>
      <a style="color:red" href="index.py?auth_logout_flag=1">X</a>
      <font color="#000000">--</font>
      </font></td>
  </tr>
  <tr bgcolor="#00FF00"> 
    <td width="568" colspan="8"><font
       face="Verdana, Arial, Helvetica, sans-serif" size="2">
       <a href="l_category.py">categories</a> |
       <a href="l_product.py">products</a> |
       <a href="sales.py">sales</a> |
       <a href="l_location.py">inventory</a> |
       affiliates |
       reports |
       <a href="templates.py">options</a> |
       zike |</font></td>
  </tr>
  <tr bgcolor="#FFFFFF"> 
    <td colspan="8"> 

'''
