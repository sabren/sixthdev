<?xml version="1.0"?>
<!-- default rantelope template -->
<xsl:stylesheet version="1.0"
   xmlns:rss="http://backend.userland.com/rss2"
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
   <xsl:template match="rss:channel">
     <html>
       <head>
         <title><xsl:value-of select="rss:title"/></title>
       </head>
       <body>
         <h1><xsl:value-of select="rss:title"/></h1>
         <p><i><xsl:value-of select="rss:description"/></i></p>
         <xsl:for-each select="rss:item">
            <div class="post">
              <h2><xsl:value-of select="rss:title"/></h2>
              <xsl:value-of select="rss:description"/>
            </div>
         </xsl:for-each>
       </body>
     </html>
   </xsl:template>
</xsl:stylesheet>
