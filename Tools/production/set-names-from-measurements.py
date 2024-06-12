from importlib import reload
import variableValues.measurements
reload(variableValues.measurements)

import os, glob, shutil
from collections import Counter
from variableValues.measurements import FontMeasurements

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

allUFOs = glob.glob(f'{sourcesFolder}/*.ufo')

ignoreTags = ['wght', 'GRAD', 'BARS']

preflight = False

allNames = []
for ufo in sorted(allUFOs):
    tag = os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][:4]

    # set family name
    f = OpenFont(ufo, showInterface=False)
    if f.info.familyName != f'{familyName} {subFamilyName}':
        print(f'family name: {f.info.familyName} --> {familyName}' )
        if not preflight:
            f.info.familyName = f'{familyName} {subFamilyName}'

    if tag in ignoreTags:
        print(f'getting {tag} value from file name: {os.path.split(ufo)[-1]}...')
        newValue = newValue1000 = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])    
        print(f'\t{newValue}')
    else:
        print(f'measuring {tag} in {os.path.split(ufo)[-1]}...')
        m = FontMeasurements()
        m.read(measurementsPath)
        m.measure(f)
        newValue = m.values[tag]
        newValue1000 = round(newValue * 1000 / f.info.unitsPerEm)
        print(f'\tunits  = {newValue}')
        print(f'\tpermil = {newValue1000}')

    # set style name
    newStyleName = f'{tag}{newValue1000}'
    allNames.append(newStyleName)
    if newStyleName != f.info.styleName:
        print(f'style name: {f.info.styleName} --> {newStyleName}' )
        if not preflight:
            f.info.styleName = newStyleName

    # rename UFO file
    newFileName = f'{familyName}-{subFamilyName}_{newStyleName}.ufo'
    newFilePath = os.path.join(sourcesFolder, newFileName)
    if not preflight:
        f.save()
    f.close()

    if ufo != newFilePath:
        print(f'\tfile name: {os.path.split(ufo)[-1]} --> {newFileName}' )
        if not preflight:
            shutil.move(ufo, newFilePath)   

    print()

# find duplicate styles
duplicates = [k for k,v in Counter(allNames).items() if v > 1]
print('duplicate style names:')
print(duplicates)
