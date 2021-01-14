# biddings_monitor

Breno Ingwersen Santos

*Python Version 3.0+*


This is a web scraper designed with requests and beautifulsoup libraries to gather information about the daily Brazil's biddings. Unfortunately, due to the nature of a scraper project, the code needs to be constantly updated to track any changes to the web page's source code in order to fully function and retrieve all the data in an organized way.

* scrapper.py - Scrapes all the pages listing all the biddings' information, treating it and putting it into a pandas DataFrame object
* notify.py - Compares the information retrieved by the scrapper.py file to a single row excel containing specific keywords of interest and sends a notification (*not fully implemented*) with the bidding's information through e-mail if a correspondence was found.

Last project update: 2020-08-10.

Esse projeto consiste em um web scraper em Python que realiza a raspagem de dados sobre as licitações publicadas diariamente através do site compras.gov.br. No entanto, devido à natureza de projetos de web scrapping, o código necessita de constante atualização para que esse possa acompanhar quaisquer mudanças no código fonte da página e, deste modo, recuperar todos os dados de modo organizado.

* scrapper.py - Raspa as páginas, trata, lista todas as informações das licitações publicadas e as armazena em um objeto DataFrame de pandas.
* notify.py - Realiza a leitura de um excel contendo palavras-chave e compara com as informações das licitações. Caso haja algum hit, ele envia um e-mail para o usuário (*não totalmente implementado*) contendo as informações da licitação encontrada.

Última atualização do projeto: 2020-08-10.
