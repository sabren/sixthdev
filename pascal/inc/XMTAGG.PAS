{ TheDraw Pascal Screen Image }
const
  XMTAG_WIDTH=80;
  XMTAG_DEPTH=4;
  XMTAG_LENGTH=640;
  XMTAG : array [1..640] of Char = (
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,' ' ,#13 ,'�' ,#5  ,'G' ,#12 ,'�' ,#13 ,'U' ,#12 ,
    '�' ,#14 ,'R' ,#12 ,'�' ,#13 ,'U' ,#12 ,'�' ,#5  ,' ' ,#13 ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,' ' ,#5  ,' ' ,#5  ,'�' ,#5  ,
    '�' ,#5  ,'D' ,#7  ,'�' ,#13 ,'O' ,#15 ,'�' ,#13 ,'S' ,#7  ,'�' ,#5  ,
    '�' ,#5  ,' ' ,#5  ,' ' ,#5  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,'�' ,#4  ,
    '�' ,#4  ,'�' ,#4  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,
    '�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  ,'�' ,#8  );
