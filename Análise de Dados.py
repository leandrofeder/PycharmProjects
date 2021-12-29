import pandas as pd
#pip install pandas (no terminal)
import win32com.client as win32
#pip install pywin32 (no terminal)

# IMPORTAR BASE DE DADOS:
tabela_vendas = pd.read_excel('Vendas.xlsx') # Importar e ler o arquivo Excel
#pip install openpyxl (no terminal)

# VISUALIZAR A BASE DE DADOS:
pd.set_option('display.max_columns', None) # Mostrar todas as colunas
print(tabela_vendas)

# FATURAMENTO POR LOJA:
#tabela_vendas[['ID Loja', 'Valor Final']] ----- Filtrando duas colunas, não mostrando as demais
#tabela_vendas.groupby('ID Loja').sum() ----- Agrupar as lojas de mesmo nome e somar as outras colunas
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)
print('-' * 50)

# QUANTIDADE DE PRODUTOS VENDIDOS POR LOJA:
produtosvendidos = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(produtosvendidos)
print('-' * 50)

# TICKET MÉDIO = FATURAMENTO / PRODUTOS VENDIDOS:
ticketmedio = (faturamento['Valor Final'] / produtosvendidos['Quantidade']).to_frame() #to_frame() transformar em tabela
ticketmedio = ticketmedio.rename(columns={0: 'Ticket Médio'})
print(ticketmedio)

# ENVIAR E-MAIL COM RELATÓRIO:
outlook = win32.Dispatch('outlook.application') #Conectar Python com o Outlook do Computador
mail = outlook.CreateItem(0) #Criando um e-mail
mail.To ='leandrofeder@outlook.com' #Para quem
mail.Subject = 'Relatório de Vendas por loja' #Assunto do e-mail
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade vendida:</p>
{produtosvendidos.to_html()}

<p>Ticket Médio dos produto em cada loja:</p>
{ticketmedio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Leandro Feder.</p>
''' #Corpo do e-mail

mail.Send()

print('E-mail Enviado.')
