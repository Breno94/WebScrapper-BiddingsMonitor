import os, smtplib
import pandas as pd
from scrapper import bidding_df


# Convert all the table's 'Table Content' column to a list for faster computing
content_array = bidding_df['Table Content'].apply(lambda x: x.upper()).tolist()

# Read the search terms excel file
search_words = pd.read_excel('search_words.xlsx')
search_words = search_words.iloc[:,0].apply(lambda x: x.upper()).tolist()

# Search for the predefined terms
biddings = ''
for content in content_array:
    for term in search_words:
        if content.find(term) != -1:
            biddings = biddings + (
                f'Termo Encontrado: "{term}"\n\n'
                f'{bidding_df.loc[content_array.index(content), "Índice"]}\t{bidding_df.loc[content_array.index(content), "UF"]} - {bidding_df.loc[content_array.index(content), "Cidade"]}\n'
                f'{bidding_df.loc[content_array.index(content), "Órgão"]}\n\n'
                f'{bidding_df.loc[content_array.index(content), "Table Content"]}\n'
                f'Link da Página: {bidding_df.loc[content_array.index(content), "Link"]}\n\n'
            )
            break
print(biddings)
# Notification e-mail
# URL to allow Python to access the e-mail account: https://myaccount.google.com/lesssecureapps?pli=1

# address = os.environ.get('USER_EMAIL') # E-mail and password locally saved as environment variables
# password = os.environ.get('USER_PASSWORD')
#
# smtp = smtplib.SMTP('smtp.gmail.com:587')
# smtp.ehlo()
# smtp.starttls()
# smtp.login(address, password)
# subject = 'TESTE'
# body = 'teste'
# msg = f'Subject: {subject}\n\n{body}'
# smtp.sendmail(address, address, msg)
