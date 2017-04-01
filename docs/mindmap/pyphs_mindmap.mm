<map version="1.0.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node COLOR="#000000" CREATED="1466855962846" ID="ID_1464725744" MODIFIED="1484390830049">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      PyPHS
    </p>
  </body>
</html></richcontent>
<font NAME="SansSerif" SIZE="20"/>
<hook NAME="accessories/plugins/AutomaticLayout.properties"/>
<node COLOR="#0033ff" CREATED="1466856210051" FOLDED="true" ID="ID_735457813" MODIFIED="1484390830033" POSITION="left">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Dictionary
    </p>
  </body>
</html></richcontent>
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1466857124781" ID="ID_821381173" MODIFIED="1466857129784" TEXT="Templates">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466857021131" FOLDED="true" ID="ID_1446913182" MODIFIED="1484390830032" TEXT="Electronics">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1466947168052" ID="ID_971733298" MODIFIED="1466947185544" TEXT="Storages">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1466947186619" ID="ID_1444552983" MODIFIED="1466947190686" TEXT="Dissipatives">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1466947191803" FOLDED="true" ID="ID_788087628" MODIFIED="1484390830030" TEXT="Sources">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466947198428" ID="ID_43841557" MODIFIED="1466947203758" TEXT="Current"/>
<node COLOR="#111111" CREATED="1466947205323" ID="ID_660938725" MODIFIED="1466947214373" TEXT="Voltage"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1466857042809" ID="ID_871745206" MODIFIED="1466857045619" TEXT="Mechanics">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466857047208" ID="ID_1184726687" MODIFIED="1466857054563" TEXT="Mechanics_dual">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466857055808" ID="ID_1481832599" MODIFIED="1466857062937" TEXT="Magnetics">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466857093798" ID="ID_1893190961" MODIFIED="1466857097993" TEXT="Thermics">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466857100765" ID="ID_1167099710" MODIFIED="1466857111273" TEXT="Fractionnal dynamics">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466857113934" ID="ID_1231491469" MODIFIED="1466857119208" TEXT="Connectors">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
</node>
<node COLOR="#0033ff" CREATED="1466856081000" FOLDED="true" ID="ID_140321449" MODIFIED="1484390830034" POSITION="left">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Code generation
    </p>
  </body>
</html></richcontent>
<edge STYLE="sharp_bezier" WIDTH="8"/>
<linktarget COLOR="#b0b0b0" DESTINATION="ID_140321449" ENDARROW="Default" ENDINCLINATION="475;327;" ID="Arrow_ID_1322840204" SOURCE="ID_1218991380" STARTARROW="None" STARTINCLINATION="432;141;"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1466946450713" ID="ID_958036996" MODIFIED="1484390644524">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <ul>
      <li>
        Return simulation process (.cpp) with header (.h).
      </li>
      <li>
        Targets are MAIN and JUCE<br />

        <ul>
          <li>
            MAIN: Generates an additional file (main.cpp) for autonomous simulations with files I/O and interface in python PyPHS object.<br />
          </li>
          <li>
            JUCE: Generates an additional juce_blocks.txt which contains pieces of code to be included in&#160;JUCE template.<br />
          </li>
        </ul>
      </li>
    </ul>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
</node>
<node COLOR="#0033ff" CREATED="1466856089047" FOLDED="true" ID="ID_1833086240" MODIFIED="1484390830035" POSITION="left">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Latex Generation
    </p>
  </body>
</html></richcontent>
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1466946757573" ID="ID_1644193911" MODIFIED="1484390639268">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <ul>
      <li>
        <p>
          Autonomous (.tex) file ready to be compiled
        </p>
      </li>
      <li>
        <p>
          Options are SYS and SIMU
        </p>
        <ul>
          <li>
            <p>
              SYS: Return the symbolic description of the PHS structure with table for parameters replacement.
            </p>
          </li>
          <li>
            <p>
              SIMU: Return a simulation report with plots of power balance and solver convergence.
            </p>
          </li>
        </ul>
      </li>
    </ul>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
</node>
<node COLOR="#0033ff" CREATED="1484390453622" HGAP="25" ID="ID_1380303090" MODIFIED="1484390724795" POSITION="right" TEXT="PSNetlist" VSHIFT="7">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<arrowlink DESTINATION="ID_1297912671" ENDARROW="Default" ENDINCLINATION="29;0;" ID="Arrow_ID_1544717088" STARTARROW="None" STARTINCLINATION="29;0;"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
<node COLOR="#0033ff" CREATED="1484390459398" ID="ID_1297912671" MODIFIED="1484390732818" POSITION="right" TEXT="PHSGraph">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<arrowlink DESTINATION="ID_880672666" ENDARROW="Default" ENDINCLINATION="31;0;" ID="Arrow_ID_1458677216" STARTARROW="None" STARTINCLINATION="31;0;"/>
<linktarget COLOR="#b0b0b0" DESTINATION="ID_1297912671" ENDARROW="Default" ENDINCLINATION="29;0;" ID="Arrow_ID_1544717088" SOURCE="ID_1380303090" STARTARROW="None" STARTINCLINATION="29;0;"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
<node COLOR="#0033ff" CREATED="1484389882864" FOLDED="true" ID="ID_880672666" MODIFIED="1484390830044" POSITION="right" TEXT="PHSCore">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<arrowlink DESTINATION="ID_1651866000" ENDARROW="Default" ENDINCLINATION="117;0;" ID="Arrow_ID_1727530620" STARTARROW="None" STARTINCLINATION="117;0;"/>
<linktarget COLOR="#b0b0b0" DESTINATION="ID_880672666" ENDARROW="Default" ENDINCLINATION="31;0;" ID="Arrow_ID_1458677216" SOURCE="ID_1297912671" STARTARROW="None" STARTINCLINATION="31;0;"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1484390034100" FOLDED="true" ID="ID_1864034196" MODIFIED="1484390830041" TEXT="Attributes">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1466856071432" FOLDED="true" ID="ID_444329499" MODIFIED="1484390830038">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Symbols
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466856322327" FOLDED="true" ID="ID_525866196" MODIFIED="1484390830035" TEXT="x">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856342775" ID="ID_737594003" MODIFIED="1466856434242">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Symbols for the state. Ordering matters for<br />linear/nonlinear or separate/nonseparate splits
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#111111" CREATED="1466856327615" FOLDED="true" ID="ID_724119492" MODIFIED="1484390830036" TEXT="w">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856446139" ID="ID_1347324595" MODIFIED="1466856478486">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Symbols for the dissipative variables.<br />Ordering matters for linear/nonlinear<br />or separate/nonseparate splits
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#111111" CREATED="1466856331079" FOLDED="true" ID="ID_1965392407" MODIFIED="1484390830036" TEXT="u">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856870905" ID="ID_1619590734" MODIFIED="1466856886411" TEXT="Symbols for system inputs"/>
</node>
<node COLOR="#111111" CREATED="1466856334982" FOLDED="true" ID="ID_1227053089" MODIFIED="1484390830037" TEXT="y">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856892575" ID="ID_1777091156" MODIFIED="1466856895758" TEXT="Symbols for system outputs"/>
</node>
<node COLOR="#111111" CREATED="1466856336927" FOLDED="true" ID="ID_1729665936" MODIFIED="1484390830037" TEXT="p">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856897175" ID="ID_326317336" MODIFIED="1466856941975">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Symbols for time varying<br />parameters (controls)
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#111111" CREATED="1466856338759" FOLDED="true" ID="ID_1221504513" MODIFIED="1484390830037" TEXT="subs">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856945253" ID="ID_592888840" MODIFIED="1478257968326">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Dicitonary with constant parameters<br />symbols as keys and these constant parameters<br />values as values
    </p>
  </body>
</html></richcontent>
</node>
</node>
</node>
<node COLOR="#990000" CREATED="1466856110342" FOLDED="true" ID="ID_1778905818" MODIFIED="1484390830040">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Expressions
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466856651620" FOLDED="true" ID="ID_1544817430" MODIFIED="1484390830039" TEXT="H">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856679669" ID="ID_373442031" MODIFIED="1466856711838">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Hamiltonian of the systems<br />with symbols in x, p and subs
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#111111" CREATED="1466856659356" FOLDED="true" ID="ID_1655189887" MODIFIED="1484390830039" TEXT="z">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856715988" ID="ID_282564549" MODIFIED="1466856811136" TEXT="Dissipative functions with symbols&#xa;in w, x, p and subs, such that &#xa;z(0)=0 and z(w).w&gt;0 is the &#xa;dissipated power"/>
</node>
<node COLOR="#111111" CREATED="1466856663572" FOLDED="true" ID="ID_1068909209" MODIFIED="1484390830040" TEXT="y">
<font NAME="SansSerif" SIZE="12"/>
<node COLOR="#111111" CREATED="1466856817447" ID="ID_1835449718" MODIFIED="1466856861657">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Output function (observation) with<br />symbols in x, w, u, p and subs
    </p>
  </body>
</html></richcontent>
</node>
</node>
</node>
</node>
<node COLOR="#00b439" CREATED="1484390039868" ID="ID_1155657722" MODIFIED="1484390042110" TEXT="Methods">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1466856187339" FOLDED="true" ID="ID_317080439" MODIFIED="1484390830043">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Structure
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1466856585592" FOLDED="true" ID="ID_248201900" MODIFIED="1484390830041" TEXT="J">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466856637613" ID="ID_53278513" MODIFIED="1466947328442">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <ul>
      <li>
        Conservative interconnection
      </li>
      <li>
        J = (M-M^T)/2
      </li>
    </ul>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#990000" CREATED="1466856612958" FOLDED="true" ID="ID_723307920" MODIFIED="1484390830042" TEXT="R">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466856637613" ID="ID_389516432" MODIFIED="1466947284796">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <ul>
      <li>
        Resistive interconnection
      </li>
      <li>
        R = -(M+M^T)/2
      </li>
    </ul>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#990000" CREATED="1466947227531" FOLDED="true" ID="ID_1624417548" MODIFIED="1484390830042" TEXT="M">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466947366376" ID="ID_269038058" MODIFIED="1466947395298">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <ul>
      <li>
        <p>
          Complete interconnection&#160;
        </p>
      </li>
      <li>
        <p>
          M = J - R
        </p>
      </li>
    </ul>
  </body>
</html></richcontent>
</node>
</node>
<node COLOR="#990000" CREATED="1466856592646" FOLDED="true" ID="ID_911931001" MODIFIED="1484390830042" TEXT="Blocks">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466856599398" ID="ID_99442255" MODIFIED="1466856612549" TEXT="Pointers to parts of J or R"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1484390478269" FOLDED="true" ID="ID_1651866000" MODIFIED="1484390830047" POSITION="right" TEXT="PHSNumericalMethod">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<arrowlink DESTINATION="ID_1218991380" ENDARROW="Default" ENDINCLINATION="39;0;" ID="Arrow_ID_1539656201" STARTARROW="None" STARTINCLINATION="39;0;"/>
<linktarget COLOR="#b0b0b0" DESTINATION="ID_1651866000" ENDARROW="Default" ENDINCLINATION="117;0;" ID="Arrow_ID_1727530620" SOURCE="ID_880672666" STARTARROW="None" STARTINCLINATION="117;0;"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1466857387409" FOLDED="true" ID="ID_228084994" MODIFIED="1484390830046" TEXT="Numerical Schemes">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1466856152997" FOLDED="true" ID="ID_1956358438" MODIFIED="1484390830045">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      FIrst order methods
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466857402514" ID="ID_438342199" MODIFIED="1466857518643" TEXT="Explicit Euler">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1466857414073" ID="ID_1165134541" MODIFIED="1466857518643" TEXT="Implicit Euler">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1466857440376" ID="ID_1154819353" MODIFIED="1466857518645" TEXT="Discrete gradient">
<font NAME="SansSerif" SIZE="12"/>
</node>
</node>
<node COLOR="#990000" CREATED="1466856152997" FOLDED="true" ID="ID_1544711492" MODIFIED="1484390830045">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Second order methods
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466857419361" ID="ID_403755582" MODIFIED="1466857518644" TEXT="Trapezoidal rule">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1466857426872" ID="ID_1315528850" MODIFIED="1466857518645" TEXT="Midpoint rule">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1466857440376" ID="ID_1099151295" MODIFIED="1466857518645" TEXT="Discrete gradient">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1466857642321" ID="ID_1641182942" MODIFIED="1484390308964" TEXT="Runge-Kutta"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1466856163820" FOLDED="true" ID="ID_1020538140" MODIFIED="1484390830046">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Solvers for implicit relations
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1466857392186" ID="ID_841264879" MODIFIED="1484390517029" TEXT="Newton-Raphson">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1466857666919" ID="ID_1494287825" MODIFIED="1484390517030" TEXT="K-method">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1466857673518" ID="ID_715173949" MODIFIED="1484390517030" TEXT="Switching Storage">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1484390467741" ID="ID_1218991380" MODIFIED="1484390801609" POSITION="right" TEXT="PHSNumericalCore">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<arrowlink DESTINATION="ID_1116059127" ENDARROW="Default" ENDINCLINATION="45;0;" ID="Arrow_ID_1186811621" STARTARROW="None" STARTINCLINATION="45;0;"/>
<arrowlink DESTINATION="ID_140321449" ENDARROW="Default" ENDINCLINATION="475;327;" ID="Arrow_ID_1322840204" STARTARROW="None" STARTINCLINATION="432;141;"/>
<linktarget COLOR="#b0b0b0" DESTINATION="ID_1218991380" ENDARROW="Default" ENDINCLINATION="39;0;" ID="Arrow_ID_1539656201" SOURCE="ID_1651866000" STARTARROW="None" STARTINCLINATION="39;0;"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
<node COLOR="#0033ff" CREATED="1484390488509" FOLDED="true" HGAP="21" ID="ID_1116059127" MODIFIED="1484390830049" POSITION="right" TEXT="PHSSimulation" VSHIFT="-5">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<linktarget COLOR="#b0b0b0" DESTINATION="ID_1116059127" ENDARROW="Default" ENDINCLINATION="45;0;" ID="Arrow_ID_1186811621" SOURCE="ID_1218991380" STARTARROW="None" STARTINCLINATION="45;0;"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1466856116174" FOLDED="true" ID="ID_1467468861" MODIFIED="1484390830049">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Data
    </p>
  </body>
</html></richcontent>
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1466946288584" FOLDED="true" ID="ID_808523780" MODIFIED="1484390830047" TEXT="Storage">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466946349452" ID="ID_222863502" MODIFIED="1466946352000" TEXT="x"/>
<node COLOR="#111111" CREATED="1466946352386" ID="ID_662484213" MODIFIED="1466946353811" TEXT="dx"/>
<node COLOR="#111111" CREATED="1466946357178" ID="ID_1173768066" MODIFIED="1466946359593" TEXT="dxH"/>
<node COLOR="#111111" CREATED="1466946362274" ID="ID_1732867281" MODIFIED="1466946365639" TEXT="x0"/>
</node>
<node COLOR="#990000" CREATED="1466946310027" FOLDED="true" ID="ID_1041214395" MODIFIED="1484390830048" TEXT="Dissipative">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466946373243" ID="ID_1522562311" MODIFIED="1466946374678" TEXT="w"/>
<node COLOR="#111111" CREATED="1466946375137" ID="ID_542108248" MODIFIED="1466946377189" TEXT="z"/>
</node>
<node COLOR="#990000" CREATED="1466946300671" FOLDED="true" ID="ID_1422028716" MODIFIED="1484390830048" TEXT="Source">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1466946382690" ID="ID_1217188625" MODIFIED="1466946385026" TEXT="u"/>
<node COLOR="#111111" CREATED="1466946385754" ID="ID_264548995" MODIFIED="1466946386831" TEXT="y"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1466856063017" ID="ID_1066991633" MODIFIED="1466856316548" POSITION="left">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Graph Analysis
    </p>
  </body>
</html></richcontent>
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
<node COLOR="#0033ff" CREATED="1466856504297" ID="ID_1934658202" MODIFIED="1466947118286" POSITION="left">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      <strike><font color="#0033ff">Flatness Analysis</font></strike>
    </p>
  </body>
</html></richcontent>
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
</node>
</map>
