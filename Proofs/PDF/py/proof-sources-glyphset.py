from importlib import reload
import xTools4.modules.glyphSetProofer
reload(xTools4.modules.glyphSetProofer)

import os, glob, time
from xTools4.modules.glyphSetProofer import GlyphSetProofer

familyName      = 'AmstelvarA2'
subFamily       = ['Roman', 'Italic'][1]
proofsFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
pdfsFolder      = os.path.join(proofsFolder, 'PDF')
baseFolder      = os.path.dirname(proofsFolder)
sourcesFolder   = os.path.join(baseFolder, 'Sources', subFamily)
defaultFontPath = os.path.join(sourcesFolder, f'{familyName}-{subFamily}_wght400.ufo')
sourcePaths     = sorted(glob.glob(f'{sourcesFolder}/*.ufo'))
sourcePaths.remove(defaultFontPath)

start = time.time()

P = GlyphSetProofer(f'{familyName} {subFamily}', defaultFontPath, sourcePaths)
P.build(savePDF=True, folder=pdfsFolder)

end = time.time()

print(f'total build time: {end - start:.2f} seconds\n')
