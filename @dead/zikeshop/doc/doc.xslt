<?xml version="1.0"?>
<xsl:transform version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="doc">
    <html>
      <head>
        <link rel="stylesheet" href="doc.css"/>
      </head>
      <body>
        <h1><xsl:value-of select="title"/></h1>
        <xsl:apply-templates select="sec"/>
        <hr/>
        <i><xsl:value-of select="ver"/></i>
      </body>
    </html>
  </xsl:template>

  <xsl:template match="sec">
    <div class="sec">
    <h2><xsl:value-of select="@title"/></h2>
    <xsl:apply-templates/>
    </div>
  </xsl:template>
    
  <!-- everything else just gets passed through: -->
  <xsl:template match="*|@*">
    <xsl:copy><xsl:apply-templates select="*|@*|text()"/></xsl:copy>
  </xsl:template>

</xsl:transform>
