{ TheDraw Pascal Screen Image }
const
  ALFSCR_WIDTH=80;
  ALFSCR_DEPTH=25;
  ALFSCR_LENGTH=4000;
  ALFSCR : array [1..4000] of Char = (
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,
    '�' ,#14 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,'�' ,#12 ,'�' ,#76 ,'�' ,#76 ,'�' ,#78 ,'�' ,#78 ,
    '�' ,#78 ,'�' ,#76 ,'�' ,#76 ,'�' ,#78 ,'�' ,#78 ,'�' ,#76 ,'�' ,#76 ,
    '�' ,#76 ,'�' ,#76 ,'�' ,#76 ,'�' ,#76 ,'�' ,#76 ,'�' ,#76 ,'�' ,#76 ,
    '�' ,#12 ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    '�' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#14 ,
    '�' ,#14 ,'�' ,#1  ,'�' ,#25 ,'�' ,#25 ,'�' ,#25 ,'�' ,#1  ,' ' ,#1  ,
    '�' ,#25 ,'�' ,#25 ,'�' ,#14 ,' ' ,#9  ,'�' ,#1  ,'�' ,#25 ,'�' ,#25 ,
    '�' ,#25 ,'�' ,#1  ,' ' ,#9  ,'�' ,#25 ,'�' ,#25 ,' ' ,#76 ,'�' ,#25 ,
    '�' ,#78 ,'�' ,#30 ,'�' ,#25 ,'�' ,#25 ,'�' ,#25 ,'�' ,#65 ,' ' ,#76 ,
    '�' ,#78 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,' ' ,#9  ,' ' ,#9  ,
    '�' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    '�' ,#14 ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,'�' ,#9  ,'�' ,#9  ,'�' ,#9  ,
    ' ' ,#9  ,'�' ,#9  ,' ' ,#9  ,'�' ,#9  ,'�' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    '�' ,#9  ,'�' ,#9  ,'�' ,#9  ,' ' ,#9  ,'�' ,#9  ,' ' ,#9  ,'�' ,#9  ,
    '�' ,#9  ,' ' ,#76 ,'�' ,#9  ,'�' ,#78 ,'�' ,#9  ,'�' ,#9  ,'�' ,#9  ,
    ' ' ,#76 ,'�' ,#9  ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    '�' ,#12 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,
    '�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#9  ,'�' ,#9  ,'�' ,#9  ,'�' ,#9  ,'�' ,#9  ,' ' ,#9  ,'�' ,#9  ,
    '�' ,#9  ,'�' ,#9  ,' ' ,#9  ,'�' ,#9  ,'�' ,#9  ,'�' ,#9  ,'�' ,#9  ,
    '�' ,#9  ,' ' ,#9  ,'�' ,#9  ,'�' ,#9  ,'�' ,#73 ,'�' ,#9  ,' ' ,#76 ,
    '�' ,#9  ,'�' ,#9  ,'�' ,#9  ,'�' ,#73 ,'�' ,#9  ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,
    ' ' ,#9  ,' ' ,#11 ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,
    '�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,'�' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#1  ,'�' ,#1  ,'�' ,#1  ,' ' ,#1  ,
    '�' ,#1  ,' ' ,#9  ,'�' ,#1  ,'�' ,#30 ,'�' ,#1  ,' ' ,#1  ,'�' ,#1  ,
    '�' ,#1  ,'�' ,#1  ,' ' ,#1  ,' ' ,#9  ,' ' ,#9  ,'�' ,#1  ,'�' ,#28 ,
    ' ' ,#76 ,'�' ,#65 ,' ' ,#76 ,'�' ,#65 ,'�' ,#65 ,'�' ,#65 ,' ' ,#76 ,
    '�' ,#65 ,' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,
    '�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#14 ,
    '�' ,#14 ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,
    '�' ,#11 ,'�' ,#11 ,'�' ,#12 ,' ' ,#76 ,' ' ,#76 ,' ' ,#77 ,' ' ,#77 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,' ' ,#9  ,' ' ,#14 ,'�' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,'�' ,#14 ,' ' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,'�' ,#14 ,' ' ,#14 ,'�' ,#14 ,' ' ,#14 ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#14 ,' ' ,#10 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#14 ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,
    ' ' ,#9  ,' ' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,'�' ,#12 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    '�' ,#12 ,' ' ,#2  ,'�' ,#10 ,' ' ,#10 ,' ' ,#10 ,'�' ,#10 ,' ' ,#10 ,
    '�' ,#10 ,' ' ,#10 ,'�' ,#10 ,' ' ,#10 ,'�' ,#10 ,'�' ,#10 ,'�' ,#10 ,
    ' ' ,#10 ,' ' ,#10 ,'�' ,#10 ,' ' ,#10 ,' ' ,#10 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,
    ' ' ,#11 ,'�' ,#12 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,' ' ,#9  ,' ' ,#2  ,'�' ,#2  ,'�' ,#2  ,
    ' ' ,#2  ,'�' ,#2  ,' ' ,#2  ,'�' ,#2  ,'�' ,#2  ,'�' ,#2  ,' ' ,#2  ,
    '�' ,#2  ,' ' ,#2  ,'�' ,#2  ,' ' ,#2  ,' ' ,#2  ,'�' ,#2  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#12 ,
    ' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#12 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,' ' ,#9  ,'�' ,#11 ,
    '�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#13 ,
    '�' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#13 ,' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#12 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,'�' ,#11 ,'�' ,#11 ,'�' ,#11 ,
    '�' ,#11 ,'�' ,#11 ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,
    '�' ,#14 ,'�' ,#14 ,' ' ,#9  ,' ' ,#9  ,'�' ,#12 ,' ' ,#76 ,' ' ,#76 ,
    ' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,' ' ,#76 ,'�' ,#12 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    '�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,'�' ,#14 ,'�' ,#14 ,'�' ,#14 ,' ' ,#9  ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,'�' ,#12 ,
    '�' ,#12 ,'�' ,#12 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,'�' ,#11 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#9  ,' ' ,#12 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#14 ,' ' ,#9  ,' ' ,#12 ,' ' ,#12 ,
    ' ' ,#12 ,' ' ,#14 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,'t' ,#7  ,'h' ,#7  ,'e' ,#7  ,' ' ,#7  ,
    'a' ,#7  ,'r' ,#7  ,'c' ,#7  ,'u' ,#7  ,'s' ,#7  ,' ' ,#7  ,'m' ,#7  ,
    'i' ,#7  ,'n' ,#7  ,'d' ,#7  ,'g' ,#7  ,'y' ,#7  ,'m' ,#7  ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,' ' ,#11 ,
    ' ' ,#11 ,' ' ,#7  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,'(' ,#7  ,'c' ,#7  ,')' ,#7  ,'1' ,#7  ,'9' ,#7  ,'9' ,#7  ,
    '6' ,#7  ,' ' ,#7  ,'s' ,#7  ,'t' ,#7  ,'e' ,#7  ,'r' ,#7  ,'l' ,#7  ,
    'i' ,#7  ,'n' ,#7  ,'g' ,#7  ,' ' ,#7  ,'s' ,#7  ,'i' ,#7  ,'l' ,#7  ,
    'v' ,#7  ,'e' ,#7  ,'r' ,#7  ,'w' ,#7  ,'a' ,#7  ,'r' ,#7  ,'e' ,#7  ,
    '.' ,#7  ,' ' ,#7  ,'a' ,#7  ,'l' ,#7  ,'l' ,#7  ,' ' ,#7  ,'r' ,#7  ,
    'i' ,#7  ,'g' ,#7  ,'h' ,#7  ,'t' ,#7  ,'s' ,#7  ,' ' ,#7  ,'r' ,#7  ,
    'e' ,#7  ,'s' ,#7  ,'e' ,#7  ,'r' ,#7  ,'v' ,#7  ,'e' ,#7  ,'d' ,#7  ,
    '.' ,#7  ,' ' ,#13 ,' ' ,#13 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,' ' ,#14 ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,'[' ,#1  ,'[' ,#9  ,' ' ,#7  ,' ' ,#7  ,'P' ,#15 ,' ' ,#7  ,
    'R' ,#15 ,' ' ,#15 ,'e' ,#11 ,' ' ,#15 ,'S' ,#15 ,' ' ,#15 ,'S' ,#15 ,
    ' ' ,#15 ,' ' ,#15 ,' ' ,#15 ,'a' ,#11 ,' ' ,#15 ,'N' ,#15 ,' ' ,#15 ,
    'y' ,#11 ,' ' ,#15 ,' ' ,#15 ,' ' ,#15 ,'K' ,#15 ,' ' ,#15 ,'e' ,#11 ,
    ' ' ,#7  ,'Y' ,#15 ,' ' ,#7  ,']' ,#9  ,']' ,#1  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#14 ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,
    ' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#9  ,' ' ,#12 ,' ' ,#12 ,' ' ,#12 ,
    ' ' ,#12 ,' ' ,#12 ,' ' ,#12 ,' ' ,#12 ,' ' ,#12 ,' ' ,#12 ,' ' ,#12 ,
    ' ' ,#12 ,' ' ,#14 ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#13 ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,
    ' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,' ' ,#7  ,
    ' ' ,#7  ,' ' ,#7  ,' ' ,#13 ,' ' ,#13 ,' ' ,#13 ,'.' ,#7  ,'.' ,#7  ,
    '.' ,#7  ,' ' ,#13 ,'[' ,#1  ,'[' ,#9  ,'S' ,#15 ,'a' ,#11 ,'B' ,#15 ,
    'R' ,#15 ,'e' ,#11 ,'N' ,#15 ,']' ,#9  ,']' ,#1  );
