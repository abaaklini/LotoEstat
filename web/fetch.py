#! /usr/bin/python
# -*- coding: iso-8859-15 -*-
"""Copyright (C) 2011 Alexandre Baaklini, abaaklini@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

"""
"""
import StringIO
import zipfile
import urllib2
import cookielib
import filecmp
import time
import shutil
import logging
import logging.handlers

def update_db (game='quina'):
    if game == 'quina':
        url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_quina.zip'
        filedb = 'D_QUINA.HTM'
    elif game == 'sena':
        url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_mgsasc.zip'
        filedb = 'd_megasc.htm'
    elif game == 'facil':
        url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip' 
        filedb = 'D_LOTFAC.HTM'
    else:
        logger.error('Game %(game)s does not exist' % {'game':game})

    logger.info('Iniciando atualização do arquivo %(arq)s' % {'arq': filedb})

    #Tratamento para cookies fornecidos pelo site
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    
    #Download propiamente dito
    try:
        raw_file = opener.open(url)
    except urllib2.URLError, err:
        logger.error('%(err)s' % {'err':err})
        return
    
    #Conteúdo do arquivo zipado, atribuido a uma variável
    file_temp = raw_file.read()
    
    #TypeError: file() argument 1 must be encoded string without NULL bytes, not str
    file_stream = StringIO.StringIO(file_temp)
    
    #Objeto zipfile criado
    zip_file = zipfile.ZipFile(file_stream,'r')
    
    #Obtendo a lista de arquivos dentro do zipfile
    list_of_files_inside_zip_file = zip_file.namelist()
    
    
    if filedb in list_of_files_inside_zip_file:
        #Arquivo sendo extraido para um path determinado
        path_to_extracted_file = zip_file.extract(filedb, path='.')
        if not filecmp.cmp(filedb, '/home/alexandre/python/lotto/web/data/' + filedb):
            logger.info('Arquivo %(arq)s sendo atualizado' % {'arq': filedb}) 
            shutil.copyfile('/home/alexandre/Dropbox/Project/python/exemplo/lotto/web/' + filedb,
                    '/home/alexandre/Dropbox/Project/python/exemplo/lotto/web/data/' + filedb)
        else:
            logger.info('Nada a ser feito para %(filedb)s' % {'filedb':filedb})
    else:
        logger.warning('Arquivo %(filedb)s não encontrado' % {'filedb':filedb})

LOGFILENAME = 'fetch.log'
logging.basicConfig(filename= LOGFILENAME, format='%(levelname)s: %(asctime)s %(message)s')
logger = logging.getLogger('FetchLog')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(
                      LOGFILENAME, maxBytes=1000000, backupCount=5)

logger.addHandler(handler)

while True:
    update_db('quina')
    update_db('sena')
    update_db('facil')
    time.sleep(86400)
