import requests
from bs4 import BeautifulSoup
from datetime import date
import math
import pandas as pd
import numpy as np

initial_date = date.today().strftime("%d/%m/%Y") # Today's date

def get_page(main_date, page):
    main_link = 'http://www.comprasnet.gov.br/consultalicitacoes/ConsLicitacao_Relacao.asp?'
    initial_date = f'dt_publ_ini={main_date}' # date format: dd/mm/yyyy
    final_date = f'dt_publ_fim={main_date}' # date format: dd/mm/yyyy
    page = f'numpag={page}'
    return main_link + 'numprp=&' \
         f'{initial_date}' \
         '&' \
         f'{final_date}' \
         '&chkModalidade=1,2,3,20,5,99&chk_concor=31,32,41,42&chk_pregao=1,2,3,4&chk_rdc=1,2,3,4&optTpPesqMat=M&optTpPesqServ=S&chkTodos=-1&chk_concorTodos=-1&chk_pregaoTodos=-1&txtlstUf=&txtlstMunicipio=&txtlstUasg=&txtlstGrpMaterial=&txtlstClasMaterial=&txtlstMaterial=&txtlstGrpServico=&txtlstServico=&txtObjeto=&' \
         f'{page}'

# This is the initial part to get the total page number
full_url = get_page(initial_date, 1)
source = requests.get(full_url, timeout=30, verify=False)
soup = BeautifulSoup(source.text, 'lxml')
page_count = math.ceil(int(soup.find('center').text.split('de ')[1].split(')')[0])/10) # There are 10 biddings per page

content = {
    'Índice': [],
    'Cidade': [],
    'UF': [],
    'Órgão': [],
    'Table Content': [],
    'Link': []
}

for page in range(1, page_count + 1):
    full_url = get_page(initial_date, page=page)
    source = requests.get(full_url, timeout=30, verify=False)
    # print(source.status_code) # Status == 200 the server was contacted correctly

    # Get all page html text
    soup = BeautifulSoup(source.text, 'lxml')

    td = soup.find_all('table', class_='td')
    for td in td:

        # Table header
        content['Índice'].append(td.td.text.split()[0]) # Extracting the index value
        content['Cidade'].append(' '.join(td.td.text.split()[1:-1]).split('-')[0]) # Extracting the city and treating the string
        content['UF'].append(td.td.text.split()[-1]) # Extracting the uf

        # Page link
        content['Link'].append(full_url)

        # Table content (Divided in two parts: First is comprised of all the buyer's information and the Second is comprised of the bidding information)
        table = td.find('tr', class_='tex3')

        # Buyer information (First part of the table)
        # ÓRGÃO SUPERIOR
        # Órgão/Entidade Vinculada
        # Unidade Gestadora Responsável (The bidding's main institution's name also the owner of the UASG)
        # Código UASG (Unidades de Administração de Serviços Gerais)

        # Remove undesired tags from the content
        buyer = str(table.td.b).replace('<b>', '?').replace('</b>', '?').replace('<br>', '?').replace('<br/>', '?')
        # Remove any undesired linebreaks or tabs and split the content into an array and remove empty elements
        buyer = buyer.replace('\t','').replace('\n','').split('?')
        buyer = list(filter(None, buyer)) # Removing empty elements
        content['Órgão'].append('\n'.join(buyer)) # Formating the same way the text is displayed on the webpage

        # Bidding information (Second part of the table)
        sec_part = ''
        for sibling in table.td.b.next_siblings:
            if sibling.name == 'b' and sibling.next_sibling.name != None:
                sec_part = sec_part + sibling.string + '\n'
            if sibling.name == 'b' and sibling.next_sibling.name == None:
                text = f'{sibling.string} {sibling.next_sibling.string}'
                sec_part = sec_part + text.replace(u'\xa0', u'') + '\n'
        content['Table Content'].append(sec_part)

bidding_df = pd.DataFrame(data=content)

