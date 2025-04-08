from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, glob, shutil
from collections import Counter
from xTools4.modules.measurements import FontMeasurements

# --------
# settings
# --------

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

ignoreTags = ['wght', 'GRAD'] # 'BARS', 
preflight  = True

# --------
# do stuff
# --------

allUFOs = glob.glob(f'{sourcesFolder}/*.ufo')

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
        # print(f'getting {tag} value from file name: {os.path.split(ufo)[-1]}...')
        newValue = newValue1000 = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])    
        # print(f'\t{newValue}')
    else:
        # print(f'measuring {tag} in {os.path.split(ufo)[-1]}...')
        m = FontMeasurements()
        m.read(measurementsPath)
        m.measure(f)
        newValue = m.values[tag]
        newValue1000 = round(newValue * 1000 / f.info.unitsPerEm)
        # print(f'\tunits  = {newValue}')
        # print(f'\tpermil = {newValue1000}')

    # set style name
    newStyleName = f'{tag}{newValue1000}'
    allNames.append(newStyleName)
    if newStyleName != f.info.styleName:
        print(f'updating style name:\n\t{f.info.styleName} --> {newStyleName}\n' )
        if not preflight:
            f.info.styleName = newStyleName

    # rename UFO file
    newFileName = f'{familyName}-{subFamilyName}_{newStyleName}.ufo'
    newFilePath = os.path.join(sourcesFolder, newFileName)
    if not preflight:
        f.save()
    f.close()

    if ufo != newFilePath:
        print(f'updating file name:\n\t{os.path.split(ufo)[-1]} --> {newFileName}\n' )
        if not preflight:
            shutil.move(ufo, newFilePath)   

    # print()

# find duplicate styles
duplicates = [k for k, v in Counter(allNames).items() if v > 1]
print('duplicate style names:')
print(duplicates)
