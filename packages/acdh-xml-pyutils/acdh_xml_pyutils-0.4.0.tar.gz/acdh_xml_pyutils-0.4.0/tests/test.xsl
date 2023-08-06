<xsl:stylesheet xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema"  version="1.0">
    <xsl:output omit-xml-declaration="yes"/>
    <xsl:template match="@*|node()">
        <hansi>
            <xsl:copy>
                <xsl:apply-templates select="@*|node()"/>
            </xsl:copy>
        </hansi>
    </xsl:template>
</xsl:stylesheet>