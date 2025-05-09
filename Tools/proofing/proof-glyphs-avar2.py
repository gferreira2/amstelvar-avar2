import os, datetime
import drawBot as DB

baseFolder   = os.path.dirname(os.path.dirname(os.getcwd()))
pdfsFolder   = os.path.join(baseFolder, 'Proofs', 'PDF')
fontsFolder  = os.path.join(baseFolder, 'Fonts')
fontRoman    = os.path.join(fontsFolder, 'AmstelvarA2-Roman_avar2.ttf')
fontItalic   = os.path.join(fontsFolder, 'AmstelvarA2-Italic_avar2.ttf')

assert os.path.exists(pdfsFolder)
assert os.path.exists(fontRoman)
assert os.path.exists(fontItalic)

_wdth = [ 50, 100, 150 ]
_wght = [ 100, 400, 1000 ]
_opsz = [ 8, 14, 144 ]

savePDF = True

fs = 56

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

ASCII  = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()
LATIN1 = ASCII + ' exclamdown cent sterling currency yen brokenbar section dieresis copyright ordfeminine guillemotleft logicalnot registered macron degree plusminus twosuperior threesuperior acute uni00B5 micro paragraph periodcentered cedilla onesuperior ordmasculine guillemotright onequarter onehalf threequarters questiondown Agrave Aacute Acircumflex Atilde Adieresis Aring AE Ccedilla Egrave Eacute Ecircumflex Edieresis Igrave Iacute Icircumflex Idieresis Eth Ntilde Ograve Oacute Ocircumflex Otilde Odieresis multiply Oslash Ugrave Uacute Ucircumflex Udieresis Yacute Thorn germandbls agrave aacute acircumflex atilde adieresis aring ae ccedilla egrave eacute ecircumflex edieresis igrave iacute icircumflex idieresis eth ntilde ograve oacute ocircumflex otilde odieresis divide oslash ugrave uacute ucircumflex udieresis yacute thorn ydieresis idotless Lslash lslash OE oe Scaron scaron Ydieresis Zcaron zcaron florin circumflex caron breve dotaccent ring ogonek tilde hungarumlaut endash emdash quoteleft quoteright quotesinglbase quotedblleft quotedblright quotedblbase dagger daggerdbl bullet ellipsis perthousand guilsinglleft guilsinglright fraction Euro trademark minus fi fl'.split()

glyphNames = ASCII # 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde exclamdown cent sterling currency yen brokenbar section dieresis copyright ordfeminine guillemotleft logicalnot registered macron degree plusminus twosuperior threesuperior acute mu paragraph periodcentered cedilla onesuperior ordmasculine guillemotright onequarter onehalf threequarters questiondown Agrave Aacute Acircumflex Atilde Adieresis Aring AE Ccedilla Egrave Eacute Ecircumflex Edieresis Igrave Iacute Icircumflex Idieresis Eth Ntilde Ograve Oacute Ocircumflex Otilde Odieresis multiply Oslash OE Ugrave Uacute Ucircumflex Udieresis Yacute Thorn germandbls agrave aacute acircumflex atilde adieresis aring ae ccedilla egrave eacute ecircumflex edieresis igrave iacute icircumflex idieresis eth ntilde ograve oacute ocircumflex otilde odieresis divide oslash oe ugrave uacute ucircumflex udieresis yacute thorn ydieresis circumflex caron breve dotaccent ring ogonek tilde hungarumlaut quoteleft quoteright minus .null CR nbspace .notdef Germandbls f_f fi fl f_f_i f_f_l Euro franc lira naira peseta won dong rupeeIndian liraTurkish manat ruble kip peso cedi colonsign guarani numero commercialMinusSign florin hryvnia tenge zero.lc one.lc two.lc three.lc four.lc five.lc six.lc seven.lc eight.lc nine.lc zero.tab one.tab two.tab three.tab four.tab five.tab six.tab seven.tab eight.tab nine.tab zero.lf one.lf two.lf three.lf four.lf five.lf six.lf seven.lf eight.lf nine.lf perthousand approxequal notequal lessequal greaterequal bulletoperator ellipsis quotesinglbase quotedblleft quotedblright quotedblbase guilsinglleft guilsinglright hyphentwo endash emdash softhyphen dagger daggerdbl bullet trademark zerosuperior foursuperior fivesuperior sixsuperior sevensuperior eightsuperior ninesuperior fraction divisionslash primemod doubleprimemod apostrophemod horizontalbar minute second leftanglebracket rightanglebracket micro hookabove breveinverted dblgrave horn dotbelow dieresisbelow commaaccent brevebelow macronbelow commaaccentturned firsttonechinese gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcomb dieresiscomb hookabovecomb ringcomb hungarumlautcomb caroncomb breveinvertedcomb dblgravecomb horncomb dotbelowcomb dieresisbelowcomb commaaccentcomb cedillacomb ogonekcomb brevebelowcomb macronbelowcomb commaaccentturnedcomb gravecomb-stack acutecomb-stack circumflexcomb-stack tildecomb-stack macroncomb-stack brevecomb-stack dotaccentcomb-stack dieresiscomb-stack hookabovecomb-stack ringcomb-stack hungarumlautcomb-stack caroncomb-stack breveinvertedcomb-stack dblgravecomb-stack grave-stack acute-stack circumflex-stack tilde-stack macron-stack breve-stack dotaccent-stack dieresis-stack hookabove-stack ring-stack hungarumlaut-stack caron-stack breveinverted-stack dblgrave-stack grave.case acute.case dieresis.case macron.case cedilla.case circumflex.case caron.case breve.case dotaccent.case ring.case ogonek.case tilde.case hungarumlaut.case hookabove.case breveinverted.case dblgrave.case horn.case dotbelow.case dieresisbelow.case commaaccent.case brevebelow.case macronbelow.case gravecomb.case acutecomb.case dieresiscomb.case macroncomb.case cedillacomb.case circumflexcomb.case caroncomb.case brevecomb.case dotaccentcomb.case ringcomb.case ogonekcomb.case tildecomb.case hungarumlautcomb.case hookabovecomb.case breveinvertedcomb.case dblgravecomb.case horncomb.case dotbelowcomb.case dieresisbelowcomb.case commaaccentcomb.case brevebelowcomb.case macronbelowcomb.case gravecomb-stack.case acutecomb-stack.case dieresiscomb-stack.case macroncomb-stack.case circumflexcomb-stack.case caroncomb-stack.case brevecomb-stack.case dotaccentcomb-stack.case ringcomb-stack.case tildecomb-stack.case hungarumlautcomb-stack.case hookabovecomb-stack.case breveinvertedcomb-stack.case dblgravecomb-stack.case Amacron amacron Abreve abreve Aogonek aogonek Cacute cacute Ccircumflex ccircumflex Cdotaccent cdotaccent Ccaron ccaron Dcaron dcaron Dcroat dcroat Emacron emacron Ebreve ebreve Edotaccent edotaccent Eogonek eogonek Ecaron ecaron Gcircumflex gcircumflex Gbreve gbreve Gdotaccent gdotaccent Gcommaaccent gcommaaccent Hcircumflex hcircumflex Hbar hbar Itilde itilde Imacron imacron Ibreve ibreve Iogonek iogonek Idotaccent IJ ij Jcircumflex Kcommaaccent kcommaaccent kgreenlandic Lacute lacute Lcommaaccent lcommaaccent Lcaron lcaron Ldot ldot Lslash lslash Nacute nacute Ncommaaccent ncommaaccent Ncaron ncaron napostrophe Eng eng Omacron omacron Obreve obreve Ohungarumlaut ohungarumlaut Racute racute Rcommaaccent rcommaaccent Rcaron rcaron Sacute sacute Scircumflex scircumflex Scedilla scedilla Scaron scaron Tcedilla tcedilla Tcaron tcaron Tbar tbar Utilde utilde Umacron umacron Ubreve ubreve Uring uring Uhungarumlaut uhungarumlaut Uogonek uogonek Wcircumflex wcircumflex Ycircumflex ycircumflex Ydieresis Zacute zacute Zdotaccent zdotaccent Zcaron zcaron Ohorn ohorn Uhorn uhorn DZcaron Dzcaron dzcaron idotless jdotless IJacute ijacute idotaccent jcircumflex Jacute.loclNLD jacute.loclNLD Iacute_J.loclNLD iacute_j.loclNLD LJ Lj lj NJ Nj nj Gcaron gcaron Oogonek oogonek Aringacute aringacute AEacute aeacute Oslashacute oslashacute Adblgrave adblgrave Ainvertedbreve ainvertedbreve Edblgrave edblgrave Einvertedbreve einvertedbreve Idblgrave idblgrave Iinvertedbreve iinvertedbreve Odblgrave odblgrave Oinvertedbreve oinvertedbreve Rdblgrave rdblgrave Rinvertedbreve rinvertedbreve Udblgrave udblgrave Uinvertedbreve uinvertedbreve Scommaaccent scommaaccent Tcommaaccent tcommaaccent Odieresismacron odieresismacron Otildemacron otildemacron Odotaccentmacron odotaccentmacron Ymacron ymacron Schwa schwa Adotbelow adotbelow Ahookabove ahookabove Acircumflexacute acircumflexacute Acircumflexgrave acircumflexgrave Acircumflexhookabove acircumflexhookabove Acircumflextilde acircumflextilde Acircumflexdotbelow acircumflexdotbelow Abreveacute abreveacute Abrevegrave abrevegrave Abrevehookabove abrevehookabove Abrevetilde abrevetilde Abrevedotbelow abrevedotbelow Edotbelow edotbelow Ehookabove ehookabove Etilde etilde Ecircumflexacute ecircumflexacute Ecircumflexgrave ecircumflexgrave Ecircumflexhookabove ecircumflexhookabove Ecircumflextilde ecircumflextilde Ecircumflexdotbelow ecircumflexdotbelow Ihookabove ihookabove Idotbelow idotbelow Odotbelow odotbelow Ohookabove ohookabove Ocircumflexacute ocircumflexacute Ocircumflexgrave ocircumflexgrave Ocircumflexhookabove ocircumflexhookabove Ocircumflextilde ocircumflextilde Ocircumflexdotbelow ocircumflexdotbelow Ohornacute ohornacute Ohorngrave ohorngrave Ohornhookabove ohornhookabove Ohorntilde ohorntilde Ohorndotbelow ohorndotbelow Udotbelow udotbelow Uhookabove uhookabove Uhornacute uhornacute Uhorngrave uhorngrave Uhornhookabove uhornhookabove Uhorntilde uhorntilde Uhorndotbelow uhorndotbelow Ygrave ygrave Ydotbelow ydotbelow Yhookabove yhookabove Ytilde ytilde Wgrave wgrave Wacute wacute Wdieresis wdieresis caroncomb.alt periodcentered.loclCAT diagonalbarO diagonalbarl diagonalbaro engtail horizontalbarH horizontalbarlc ohm numeralsign lownumeralsign gr:question anoteleia tonos tonos.case dieresistonos tonoscomb tonoscomb.case dieresistonoscomb Dje Ieukran Dze Iukran Yi Je Lje Nje Tshe Dzhe Acyr Abrevecyr Adieresiscyr Be Ve Ghe Gje De Ie Io Iebrevecyr Zhe Zhebrevecyr Zhedieresiscyr Ze Icyr Igravecyr Ishort Ka Kje El Em En Ocyr Odieresiscyr Pe Er Es Te Ucyr Ushort Umacroncyr Udieresiscyr Uhungarumlautcyr Ef Ha Tse Che Sha Shcha Hard Yeru Soft Ecyr Yu Ya Gheup Ghestroke Zhedescender Zedescendercyr Kadescender Kaverticalstrokecyr Kabashkircyr Endescender Esdescendercyr Tedescender-cy Ustraight Ustraightstroke Hadescender Chedescender-cy Cheverticalstroke-cy Shha Palochka Schwacyr Obarcyr Hastroke-cy De.bgr Zhe.bgr Ka.bgr El.bgr acyr abrevecyr adieresiscyr be ve ghe gje de ie io iebrevecyr zhe zhebrevecyr zhedieresiscyr ze icyr ishort igravecyr ka kje el em en ocyr odieresiscyr pe er es te ucyr ushort umacroncyr udieresiscyr uhungarumlautcyr ef ha tse che sha shcha hard yeru soft ecyr yu ya dje ieukran dze iukran yi je lje nje tshe dzhe gheup ghestroke zhedescender zedescendercyr kadescender kaverticalstrokecyr kabashkircyr endescender esdescendercyr tedescender-cy ustraight ustraightstroke hadescender chedescender-cy cheverticalstroke-cy shha palochka schwacyr obarcyr hastroke-cy ve.bgr ghe.bgr de.bgr i.bgr igrave.bgr zhe.bgr ze.bgr ka.bgr el.bgr en.bgr pe.bgr te.bgr tse.bgr che.bgr sha.bgr shcha.bgr hard.bgr soft.bgr yu.bgr ishort.bgr be.locl ghe.locl de.locl pe.locl te.locl Amacroncyr amacroncyr Iemacroncyr iemacroncyr Omacroncyr omacroncyr Obrevecyr obrevecyr Emacroncyr emacroncyr Ebrevecyr ebrevecyr Yamacron yamacron Yumacron yumacron breve.cyr.case breve.cyr yi-dieresis breve.cyrcomb.case breve.cyrcomb Yi-dieresiscomb.case yi-dieresiscomb increment Yu-dash.case idot engn ha-stroke hornU hornu ustraight-stroke yu.bgr-stroke Alpha Alphatonos Beta Gamma Delta Epsilon Epsilontonos Zeta Eta Etatonos Theta Iota Iotatonos Iotadieresis Kappa Lambda Mu Nu Xi Omicron Omicrontonos Pi Rho Sigma Tau Upsilon Upsilontonos Upsilondieresis Phi Chi Psi Omega Omegatonos Kaisymbol alpha alphatonos beta gamma delta epsilon epsilontonos zeta eta etatonos theta iota iotadieresistonos iotatonos iotadieresis kappa lambda nu xi omicron omicrontonos pi rho finalsigma sigma tau upsilon upsilondieresistonos upsilondieresis upsilontonos phi chi psi omega omegatonos kaisymbol Obarcyr-stroke U-stroke Ha-stroke obarcyr-stroke Cy-descendercomb.case cy-descendercomb yu-i Engtail diagonalbarL caroncomb-alt.case periodcentered-loclCAT.case'.split()
ignoreGlyphs = 'space nbspace CR .notdef .null gravecomb acutecomb circumflexcomb tildecomb macroncomb brevecomb dotaccentcomb dieresiscomb hookabovecomb ringcomb hungarumlautcomb caroncomb breveinvertedcomb dblgravecomb horncomb dotbelowcomb dieresisbelowcomb commaaccentcomb cedillacomb ogonekcomb brevebelowcomb macronbelowcomb commaaccentturnedcomb gravecomb-stack acutecomb-stack circumflexcomb-stack tildecomb-stack macroncomb-stack brevecomb-stack dotaccentcomb-stack dieresiscomb-stack hookabovecomb-stack ringcomb-stack hungarumlautcomb-stack caroncomb-stack breveinvertedcomb-stack dblgravecomb-stack gravecomb-stack.case acutecomb-stack.case dieresiscomb-stack.case macroncomb-stack.case circumflexcomb-stack.case caroncomb-stack.case brevecomb-stack.case dotaccentcomb-stack.case ringcomb-stack.case tildecomb-stack.case hungarumlautcomb-stack.case hookabovecomb-stack.case breveinvertedcomb-stack.case dblgravecomb-stack.case caroncomb.alt tonoscomb dieresistonoscomb breve.cyrcomb yi-dieresiscomb'.split()

DB.newDrawing()

for glyphName in glyphNames:
    if glyphName in ignoreGlyphs:
        continue

    DB.newPage('A4Landscape')

    with DB.savedState():
        mx, my = 13, 12
        yTop = DB.height()-my
        DB.fontSize(7)
        DB.fill(1, 0, 0)
        DB.text('AmstelvarA2', (mx, yTop), align='left')
        DB.text(glyphName, (DB.width()/2, yTop), align='center')
        DB.text(now, (DB.width()-mx, yTop), align='right')
    #     rotate(90)
    #     W = height()/3
    #     for pt in [8, 14, 144]:
    #         text(f'{pt}', (W/2, -10), align='center')
    #         translate(W, 0)

    w  = DB.width()  / (len(_wght))
    h  = DB.height() / (len(_opsz))

    ww = w / len(_wdth)
    hh = h / 2

    for i, wght in enumerate(_wght):
        for j, opsz in enumerate(_opsz):
            for ii, wdth in enumerate(_wdth):
                for jj, fontStyle in enumerate([fontItalic, fontRoman]):
                    x = i * w + ii * ww + ww * 0.5
                    y = j * h + jj * hh + hh * 0.3
                    T = DB.FormattedString()
                    T.fontSize(fs)
                    T.font(fontStyle)
                    variations = {
                        'opsz' : opsz,
                        'wght' : wght,
                        'wdth' : wdth,
                    }
                    T.fontVariations(**variations)
                    T.appendGlyph(glyphName)
                    DB.text(T, (x, y), align='center')
                    with DB.savedState():
                        DB.fill(1, 0, 0)
                        txt = f'{"Roman" if jj else "Italic"}\n{opsz} {wght} {wdth}'
                        DB.fontSize(7)
                        DB.text(txt, (x, y-10), align='center')

# save PDF
if savePDF:
    pdfPath = os.path.join(pdfsFolder, 'glyphs-Roman-Italic.pdf')
    DB.saveImage(pdfPath)
