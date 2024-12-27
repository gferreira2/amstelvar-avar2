import os, glob, shutil, json, time
from xml.etree.ElementTree import parse
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont
from defcon import Font
from ufo2ft import compileVariableTTF
import ufoProcessor # upgrade to UFOOperator?
from xTools4.modules.measurements import FontMeasurements, permille
from xTools4.modules.linkPoints2 import readMeasurements


SUBFAMILY = ['Roman', 'Italic'][0]

ASCII  = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'
LATIN1 = ASCII + ' exclamdown cent sterling currency yen brokenbar section dieresis copyright ordfeminine guillemotleft logicalnot registered macron degree plusminus twosuperior threesuperior acute uni00B5 micro paragraph periodcentered cedilla onesuperior ordmasculine guillemotright onequarter onehalf threequarters questiondown Agrave Aacute Acircumflex Atilde Adieresis Aring AE Ccedilla Egrave Eacute Ecircumflex Edieresis Igrave Iacute Icircumflex Idieresis Eth Ntilde Ograve Oacute Ocircumflex Otilde Odieresis multiply Oslash Ugrave Uacute Ucircumflex Udieresis Yacute Thorn germandbls agrave aacute acircumflex atilde adieresis aring ae ccedilla egrave eacute ecircumflex edieresis igrave iacute icircumflex idieresis eth ntilde ograve oacute ocircumflex otilde odieresis divide oslash ugrave uacute ucircumflex udieresis yacute thorn ydieresis idotless Lslash lslash OE oe Scaron scaron Ydieresis Zcaron zcaron florin circumflex caron breve dotaccent ring ogonek tilde hungarumlaut endash emdash quoteleft quoteright quotesinglbase quotedblleft quotedblright quotedblbase dagger daggerdbl bullet ellipsis perthousand guilsinglleft guilsinglright fraction Euro trademark minus fi fl'


class AmstelvarA2DesignSpaceBuilder:
    '''
    Simple parametric designspace for use while designing.

    Specialized designspaces for output are created by subclassing this object.

    - parametric axes

    + builds instances from blends.json file
    + builds variable font

    '''
    familyName      = 'AmstelvarA2'
    subFamilyName   = SUBFAMILY
    defaultName     = 'wght400'
    designspaceName = f'{familyName}-{subFamilyName}.designspace'

    parentAxesBuild  = True
    parentAxesRoman  = 'XOPQ YOPQ XTRA XSHA YSHA XSVA YSVA XVAA YHAA'.split() # YTRA
    parentAxesItalic = 'XOPQ YOPQ XTRA XSHA YSHA XSVA YSVA'.split() # YTRA

    parametricAxesRoman  = 'XOUC XOLC XOFI YOUC YOLC YOFI XTUC XTLC XTFI YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XVAU YHAU XVAL YHAL XVAF YHAF XTTW YTTL YTOS XUCS WDSP XDOT YTEQ'.split()
    parametricAxesItalic = 'XOUC XOLC XOFI YOUC YOLC YOFI XTUC XTLC XTFI YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL           XSVF YSVF XTTW YTTL YTOS XUCS WDSP XDOT'.split()

    def __init__(self):
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Sources', self.subFamilyName)

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    @property
    def varFontsFolder(self):
        return os.path.join(self.baseFolder, 'Fonts')

    @property
    def varFontPath(self):
        return os.path.join(self.varFontsFolder, self.designspaceName.replace('.designspace', '.ttf'))

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, 'measurements.json')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceName)

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        L['GRAD'] = 0
        L['BARS'] = 100
        # L['YTEQ'] = 0
        return L

    @property
    def amstelvarFolder(self):
        # path to a local copy of http://github.com/gferreira/amstelvar
        return os.path.join(os.path.dirname(self.baseFolder), 'amstelvar')

    @property
    def amstelvarBlendsPath(self):
        return os.path.join(self.amstelvarFolder, self.subFamilyName, 'blends.json')

    @property
    def blendsPath(self):
        return os.path.join(self.sourcesFolder, 'blends.json')

    @property
    def blendedAxes(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['axes']

    @property
    def blendedSources(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['sources']

    @property
    def parametricAxes(self):
        if self.subFamilyName == 'Italic':
            return self.parametricAxesItalic
        else:
            return self.parametricAxesRoman

    def buildBlendsFile(self):
        if not os.path.exists(self.amstelvarBlendsPath):
            return

        # import Amstelvar blends
        with open(self.amstelvarBlendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)

        # -------------
        # add XTSP axis
        # -------------

        blendsDict['axes']['XTSP'] = {
            "name"    : "XTSP",
            "default" : 0,
            "min"     : -100,
            "max"     : 100,
        }
        # get min/max values from file names
        values = []
        for ufo in self.parametricSources:
            if 'XUCS' in ufo:
                value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                values.append(value)
        assert len(values)
        values.sort()
        # add XTSP min source
        blendsDict['sources']['XTSP-100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP-100']['XUCS'] = values[0]
        # add XTSP max source
        blendsDict['sources']['XTSP100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP100']['XUCS'] = values[1]

        # -----------------------
        # add blended PARENT axes
        # -----------------------

        if self.parentAxesBuild:
            measurements = readMeasurements(self.measurementsPath)
            fontMeasurements = measurements['font']

            # get children axes
            parentAxes = self.parentAxesRoman if SUBFAMILY == 'Roman' else self.parentAxesItalic
            for parentAxis in parentAxes:
                parentMeasurement = fontMeasurements[parentAxis]

                children = {}
                childNames = [a[0] for a in fontMeasurements.items() if a[1]['parent'] == parentAxis]
                for childName in childNames:
                    # get min/max values from file names
                    values = []
                    for ufo in self.parametricSources:
                        if childName in ufo:
                            value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                            values.append(value)

                    if not len(values) == 2:
                        print(parentAxis, childName, values)
                        continue

                    values.sort()
                    children[childName] = values

                # add parent axis
                parentMin    = min([v[0] for v in children.values()]) # parent min is the lowest  child min  <-- IS THIS CORRECT ??
                parentMax    = max([v[1] for v in children.values()]) # parent max is the highest child max 
                parenDefault = permille(self.measurementsDefault.values[parentAxis], self.unitsPerEm)
                blendsDict['axes'][parentAxis] = {
                    "name"    : parentAxis,
                    "default" : parenDefault,
                    "min"     : parentMin,
                    "max"     : parentMax,
                }

                # add parent min source
                blendsDict['sources'][f'{parentAxis}{parentMin}'] = self.defaultLocation.copy()
                for childAxis in children.keys():
                    blendsDict['sources'][f'{parentAxis}{parentMin}'][childAxis] = children[childAxis][0]

                # add parent max source
                blendsDict['sources'][f'{parentAxis}{parentMax}'] = self.defaultLocation.copy()
                for childAxis in children.keys():
                    blendsDict['sources'][f'{parentAxis}{parentMax}'][childAxis] = children[childAxis][1]

        # -----------------------
        # save AmstelvarA2 blends
        # -----------------------

        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def addParametricAxes(self):

        # add custom parametric axes
        a = AxisDescriptor()
        a.name    = 'GRAD'
        a.tag     = 'GRAD'
        a.minimum = -300
        a.maximum = 500
        a.default = 0
        self.designspace.addAxis(a)

        # add parametric axes
        for name in self.parametricAxes:
            # get default value
            defaultValue = permille(self.measurementsDefault.values[name], self.unitsPerEm)
            # get min/max values from file names
            values = []
            for ufo in self.parametricSources:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            if len(values) == 2:
                values.sort()
                minValue, maxValue = values
            elif len(values) == 1:
                values.append(defaultValue)
                values.sort()
                minValue, maxValue = values
            else:
                print(f'ERROR: {name}: {values}')
                # continue

            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = minValue
            a.maximum = maxValue
            a.default = defaultValue

            self.designspace.addAxis(a)

        # add custom BARS axis
        a = AxisDescriptor()
        a.name    = 'BARS'
        a.tag     = 'BARS'
        a.minimum = 0
        a.maximum = 100
        a.default = 100
        self.designspace.addAxis(a)

        # # custom YTEQ axis
        # if self.subFamilyName == 'Roman':
        #     a = AxisDescriptor()
        #     a.name    = 'YTEQ'
        #     a.tag     = 'YTEQ'
        #     a.minimum = 0
        #     a.maximum = 100
        #     a.default = 0
        #     self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = f'{self.familyName} {self.subFamilyName}'
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation
        self.designspace.addSource(src)

    def addParametricSources(self):

        # add custom parametric sources
        axis = 'GRAD'
        for value in [-300, 500]:
            src = SourceDescriptor()
            src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{axis}{value}.ufo')
            src.familyName = f'{self.familyName} {self.subFamilyName}'
            src.styleName  = f'{axis}{value}'
            L = self.defaultLocation.copy()
            L[axis] = value
            src.location = L
            self.designspace.addSource(src)

        axis  = 'BARS'
        value = 0
        src = SourceDescriptor()
        src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{axis}{value}.ufo')
        src.familyName = f'{self.familyName} {self.subFamilyName}'
        src.styleName  = f'{axis}{value}'
        L = self.defaultLocation.copy()
        L[axis] = value
        src.location = L
        self.designspace.addSource(src)

        # if self.subFamilyName == 'Roman':
        #     axis  = 'YTEQ'
        #     value = 100
        #     src = SourceDescriptor()
        #     src.path       = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{axis}{value}.ufo')
        #     src.familyName = f'{self.familyName} {self.subFamilyName}'
        #     src.styleName  = f'{axis}{value}'
        #     L = self.defaultLocation.copy()
        #     L[axis] = value
        #     src.location = L
        #     self.designspace.addSource(src)

        # add parametric sources
        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = f'{self.familyName} {self.subFamilyName}'
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addInstances(self):
        for styleName in self.blendedSources.keys():
            L = self.defaultLocation.copy()
            for axis, value in self.blendedSources[styleName].items():
                L[axis] = value

            I = InstanceDescriptor()
            I.familyName     = f'{self.familyName} {self.subFamilyName}'
            I.styleName      = styleName.replace('_', ' ')
            I.name           = styleName
            I.designLocation = L
            I.filename       = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')

            self.designspace.addInstance(I)

    def buildInstances(self, clear=True):

        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)

        ufoProcessor.build(self.designspacePath)
        ufos = glob.glob(f'{self.instancesFolder}/*.ufo')

        # copy glyph order from default
        f = OpenFont(self.defaultUFO, showInterface=False)
        glyphOrder = f.glyphOrder
        f.close()

        for ufo in ufos:
            f = OpenFont(ufo, showInterface=False)
            f.glyphOrder = glyphOrder
            f.save()
            f.close()

    def addBlendedAxes(self):
        for tag in self.blendedAxes.keys():
            a = AxisDescriptor()
            a.name    = self.blendedAxes[tag]['name']
            a.tag     = tag
            a.minimum = self.blendedAxes[tag]['min']
            a.maximum = self.blendedAxes[tag]['max']
            a.default = self.blendedAxes[tag]['default']
            self.designspace.addAxis(a)

    def build(self, blends=True, instances=True):
        self.designspace = DesignSpaceDocument()
        if blends:
            self.buildBlendsFile()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        if instances:
            self.addInstances()

    def save(self):
        if not self.designspace:
            return
        print(f'saving {os.path.split(self.designspacePath)[-1]}...')
        self.designspace.write(self.designspacePath)

    def buildVariableFont(self, subset=None, setVersionInfo=True, debug=False):

        print(f'generating variable font for {self.designspaceName}...')

        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        print(f'\tloading sources...')
        for src in D.sources:
            if debug:
                print(f'\t\tloading {src.familyName} {src.styleName}...')
            src.font = Font(src.path)

        print(f'\tcompiling variable font...')
        f = compileVariableTTF(D, featureWriters=[], reverseDirection=False)
        f.save(self.varFontPath)

        assert os.path.exists(self.varFontPath)

        # subset ascii variable font with pyftsubset
        if subset:
            print('\tsubsetting variable font...')
            asciiGlyphs = subset.split()
            font = TTFont(self.varFontPath)
            subsetter = Subsetter()
            subsetter.populate(glyphs=asciiGlyphs)
            subsetter.subset(font)
            font.save(self.varFontPath)

        # set version info in the font's unique name
        if setVersionInfo:
            print('\tsetting version info...')
            # convert ttf to ttx
            ttxPath = self.varFontPath.replace('.ttf', '.ttx')
            tt = TTFont(self.varFontPath)
            tt.verbose = False
            tt.saveXML(ttxPath)
            tt.close()
            # make unique name with timestamp
            timestamp = time.strftime("%Y%m%d%H%M", time.localtime())
            uniqueName = f'{self.familyName} {self.subFamilyName} {timestamp}'
            # add version info to unique name -- nameID 3
            tree = parse(ttxPath)
            root = tree.getroot()
            for child in root.find('name'):
                if child.attrib['nameID'] == '3':
                    child.text = uniqueName
            tree.write(ttxPath)
            # convert ttx back to ttf
            tt = TTFont()
            tt.verbose = False
            tt.importXML(ttxPath)
            tt.save(self.varFontPath)
            tt.close()
            # clear ttx file
            os.remove(ttxPath)

        print('...done.\n')


class AmstelvarA2DesignSpaceBuilder_avar1(AmstelvarA2DesignSpaceBuilder):
    '''
    Designspace for building an avar1 variable font.

    - parametric axes
    - blended axes: opsz wght wdth (XTSP)
    - wght/wdth extrema defined by instances

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar1.designspace')

    def addBlendedSources(self):
        for tag in self.blendedAxes.keys():
            axisName = self.blendedAxes[tag]['name']
            valueMin = self.blendedAxes[tag]['min']
            valueMax = self.blendedAxes[tag]['max']
            for value in [valueMin, valueMax]:
                ufoPath = os.path.join(self.instancesFolder, f'{self.familyName}-{self.subFamilyName}_{tag}{value}.ufo')
                if not os.path.exists(ufoPath):
                    print(f'font {ufoPath} does not exist')
                L = self.defaultLocation.copy()
                L[axisName] = value
                src = SourceDescriptor()
                src.path       = ufoPath
                src.familyName = self.familyName
                src.styleName  = f'{tag}{value}'
                src.location   = L
                self.designspace.addSource(src)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addBlendedSources()


class AmstelvarA2DesignSpaceBuilder_avar2(AmstelvarA2DesignSpaceBuilder):
    '''
    Designspace for building an avar2 variable font.

    - parametric axes
    - XTSP
    - blended axes: wght wdth
    - wght/wdth extrema defined by avar2 <mappings>

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar2.designspace')

    def addMappings(self):

        blendedAxes    = self.blendedAxes
        blendedSources = self.blendedSources

        for styleName in blendedSources.keys():
            m = AxisMappingDescriptor()

            # get input value from style name
            inputLocation = {}
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                axisName  = blendedAxes[tag]['name']
                inputLocation[axisName] = value

            # get output value from blends.json file
            outputLocation = {}
            for axisName in blendedSources[styleName]:
                outputLocation[axisName] = int(blendedSources[styleName][axisName])

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation

            self.designspace.addAxisMapping(m)

        # retract BARS
        # m = AxisMappingDescriptor()
        # m.inputLocation = {
        #     "BARS"   : 100,
        #     "Weight" : 700,
        # }
        # m.outputLocation = {
        #     "BARS" : 0,
        # }
        # self.designspace.addAxisMapping(m)
        # m = AxisMappingDescriptor()
        # m.inputLocation = {
        #     "BARS"   : 100,
        #     "Weight" : 1000,
        # }
        # m.outputLocation = {
        #     "BARS" : 0,
        # }
        # self.designspace.addAxisMapping(m)

    def build(self):
        self.buildBlendsFile()
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings()
        self.addDefaultSource()
        self.addParametricSources()
        self.addInstances()


class AmstelvarA2DesignSpaceBuilder_avar2_fences(AmstelvarA2DesignSpaceBuilder_avar2):
    '''
    Designspace which adds fences to the avar2 variable font.

    same as the avar2 build plus:

    - fences for the default (wght400)
    - fences for blended extrema (wght200 wght800 wdth85 wdth125)
    - limit min/max values for XOPQ YOPQ XTRA XTSP only

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar2_fences.designspace')

    @property
    def fencesPath(self):
        return os.path.join(self.sourcesFolder, 'fences.json')

    @property
    def fences(self):
        with open(self.fencesPath, 'r', encoding='utf-8') as f:
            fences = json.load(f)
        return fences

    def addMappingsFences(self):

        defaultName = 'wght400'

        # add fences for default (monovar)

        blendTag    = defaultName[:4]
        blendValue  = int(defaultName[4:])
        blendName   = self.blendedAxes[blendTag]['name']
        for tag in self.fences[defaultName]:
            # get min/max fence values
            valuesFence = [
                self.fences[defaultName][tag]['min'],
                self.fences[defaultName][tag]['max'],
            ]
            # get min/max parametric axis value from file names
            valuesAxis = []
            for ufo in self.parametricSources:
                if tag in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    valuesAxis.append(value)
            assert len(valuesAxis)
            valuesAxis.sort()
            # create mapping elements
            for i, valueFence in enumerate(valuesFence):
                valueAxis  = valuesAxis[i]
                m = AxisMappingDescriptor()
                m.inputLocation = {
                    blendName : blendValue,
                    tag       : valueAxis,
                }
                m.outputLocation = {
                    blendName : blendValue,
                    tag       : valueFence,
                }
                self.designspace.addAxisMapping(m)

        # add fences for extrema

        # for styleName in self.fences.keys():
        #     if styleName == defaultName:
        #         continue
        #     blendTag    = styleName[:4]
        #     blendValue  = int(styleName[4:])
        #     blendName   = self.blendedAxes[blendTag]['name']
        #     for tag in self.fences[styleName]:
        #         # get min/max fence values
        #         valuesFence = [
        #             self.fences[defaultName][tag]['min'],
        #             self.fences[defaultName][tag]['max'],
        #         ]
        #         # get min/max parametric axis value from file names
        #         valuesAxis = []
        #         for ufo in self.parametricSources:
        #             if tag in ufo:
        #                 value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
        #                 valuesAxis.append(value)
        #         assert len(valuesAxis)
        #         valuesAxis.sort()
        #         # create null mappings
        #         for i, valueFence in enumerate(valuesFence):
        #             valueAxis  = valuesAxis[i]
        #             m = AxisMappingDescriptor()
        #             m.inputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueAxis,
        #             }
        #             m.outputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueFence,
        #             }
        #             self.designspace.addAxisMapping(m)

        #             m = AxisMappingDescriptor()
        #             m.inputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueAxis,
        #             }
        #             m.outputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueAxis,
        #             }
        #             self.designspace.addAxisMapping(m)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings()
        self.addMappingsFences()
        self.addDefaultSource()
        self.addParametricSources()


class AmstelvarA2DesignSpaceInitializer(AmstelvarA2DesignSpaceBuilder):

    # designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_init.designspace')

    @property
    def defaultLocation(self):
        return { name: 0 for name in self.parametricAxes }

    def addParametricAxes(self):
        print('adding parametric axes...')
        for name in self.parametricAxes:
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = -1.0
            a.maximum = 1.0
            a.default = 0
            self.designspace.addAxis(a)

    def addParametricSources(self):
        print('adding parametric sources...')
        for name in self.parametricAxes:
            for value in ['min', 'max']:
                ufoPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{name}{value}.ufo')
                src = SourceDescriptor()
                src.path       = ufoPath
                src.familyName = self.familyName
                L = self.defaultLocation.copy()
                src.styleName  = f'{name}{value}'
                L[name] = -1.0 if value == 'min' else 1.0
                src.location = L
                self.designspace.addSource(src)

    def buildParametricSources(self):
        for name in self.parametricAxes:
            for value in ['min', 'max']:
                ufoPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{name}{value}.ufo')
                if os.path.exists(ufoPath):
                    shutil.rmtree(ufoPath)
                shutil.copytree(self.defaultUFO, ufoPath)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        # self.buildParametricSources()


class AmstelvarA2DesignSpaceBuilder_avar2_v2(AmstelvarA2DesignSpaceBuilder_avar2):
    '''
    Experimental version of avar2 designspace with instances defined by user axes instead of parametric ones.

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar2_v2.designspace')

    def addInstances(self):

        for styleName in self.blendedSources.keys():
            parameters = styleName.split('_')
            L = {}
            for parameter in parameters:
                tag  = parameter[:4]
                value = int(parameter[4:])
                axis = self.blendedAxes[tag]['name']
                L[axis] = value

            I = InstanceDescriptor()
            I.familyName   = self.familyName
            I.styleName    = styleName.replace('_', ' ')
            I.name         = styleName
            I.userLocation = L
            I.filename     = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')

            self.designspace.addInstance(I)


# -----
# build
# -----

if __name__ == '__main__':

    # D0 = AmstelvarA2DesignSpaceInitializer()
    # D0.build()
    # D0.save()

    # D = AmstelvarA2DesignSpaceBuilder()
    # D.build(blends=True, instances=True)
    # D.save()
    # D.buildInstances()

    # D1 = AmstelvarA2DesignSpaceBuilder_avar1()
    # D1.build()
    # D1.save()
    # D1.buildVariableFont()

    D2 = AmstelvarA2DesignSpaceBuilder_avar2()
    D2.build()
    D2.save()
    D2.buildVariableFont(subset=None, setVersionInfo=True, debug=False)

    # D3 = AmstelvarA2DesignSpaceBuilder_avar2_fences()
    # D3.build()
    # D3.save()
    # D3.buildVariableFont()

    # D4 = AmstelvarA2DesignSpaceBuilder_avar2_v2()
    # D4.build()
    # D4.save()
    # D4.buildVariableFont(subset=None, setVersionInfo=True, debug=False)

