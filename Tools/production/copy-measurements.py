import os, json
from xTools4.modules.measurements import readMeasurements


baseFolder          = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder       = os.path.join(baseFolder, 'Sources')
measurementsPathSrc = os.path.join(sourcesFolder, 'Roman',  'measurements.json')
# measurementsPathDst = os.path.join(sourcesFolder, 'Italic', 'measurements.json') 
amstelvarFolder     = os.path.join(os.path.dirname(baseFolder), 'amstelvar')
measurementsPathDst = os.path.join(amstelvarFolder, 'Roman',  'measurements.json')
measurementsSrc     = readMeasurements(measurementsPathSrc)
measurementsDst     = readMeasurements(measurementsPathDst)

measurementNames    = 'XVAA YHAA XVAU YHAU XVAL YHAL'.split()
glyphNames          = ['AE'] # CurrentFont().selectedGlyphNames

print('source:\n\t', measurementsPathSrc, os.path.exists(measurementsPathSrc))
print('target:\n\t', measurementsPathDst, os.path.exists(measurementsPathDst))
print()

copyFontMeasurements  = True
copyGlyphMeasurements = False

# copy font-level measurements
if copyFontMeasurements:
    print('copying font-level measurements...')
    for measurementName in measurementNames:
        print(f'\tcopying {measurementName}...')
        measurementsDst['font'][measurementName] = measurementsSrc['font'][measurementName] 
    print()

# copy glyph-level measurements
if copyGlyphMeasurements:
    print('copying glyph-level measurements...')
    for glyphName in glyphNames:
        print(f'\tcopying {glyphName}...')
        if glyphName not in measurementsSrc['glyphs']:
            continue
        measurementsDst['glyphs'][glyphName] = measurementsSrc['glyphs'][glyphName] 
    print()

# save dest measurements file
if copyFontMeasurements or copyGlyphMeasurements:
    print('\tsaving measurements...')
    with open(measurementsPathDst, 'w', encoding='utf-8') as f:
        json.dump(measurementsDst, f, indent=2)
    print('...done.')
