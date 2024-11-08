# Steam Sales Scraper

https://docs.google.com/spreadsheets/d/1naXAMnoSGRZFUxAkE42QbOeNpiA7ws51N0A5Kj_1B2Y/edit?usp=sharing

Esse projeto é um **web scraper** que coleta dados de vendas e promoções da plataforma **Steam**. 
Utilizando bibliotecas como **Selenium** e **BeautifulSoup**, o programa extrai informações de jogos e armazena esses dados no **Google BigQuery**, 
além de exportá-los para o **Google Sheets** para fácil visualização e análise.

## Funcionalidades

- **Coleta de dados da Steam**: Extrai informações de jogos em promoção, como nome, preço, desconto, entre outros.
- **Armazenamento no Google BigQuery**: Salva os dados diretamente no BigQuery para facilitar consultas e análises.
- **Exportação para Google Sheets**: Permite a exportação dos dados para uma planilha do Google Sheets, tornando-os acessíveis para visualização e compartilhamento.
- **Automação com API do Google**: Utiliza uma conta de serviço do Google para automatizar o processo de autenticação e acesso aos serviços.

## Requisitos

- **Python** 3.7+
- **Google Cloud** com acesso ao BigQuery e Google Sheets.
- **Bibliotecas Python**: As principais bibliotecas usadas são:
  - selenium
  - beautifulsoup4
  - google-auth
  - google-auth-oauthlib
  - google-auth-httplib2
  - google-api-python-client

## Instalação

Clone este repositório:
git clone https://github.com/pcrs29/steam-sales-scraper.git
cd steam-sales-scraper

Instale as dependências:
pip install -r requirements.txt

Configure as variáveis de ambiente criando um arquivo .env na pasta do projeto com o seguinte conteúdo:
GOOGLE_APPLICATION_CREDENTIALS="credentials.json"
BIGQUERY_PROJECT_ID="direct-analog-420112"
BIGQUERY_TABLE="meu_dataset.minha_tabela"

Uso
Execute o scraper:
python extrator_steamdb.py
O script irá extrair os dados da Steam, armazená-los no BigQuery e exportá-los para o Google Sheets.

Estrutura de Arquivos
extrator_steamdb.py: Script principal do scraper.
.env: Arquivo de variáveis de ambiente com as configurações do projeto (não incluído no repositório por questões de segurança).
credentials.json: Arquivo de credenciais do Google (também ignorado para segurança).
.gitignore: Configurado para ignorar .env, credentials.json e outros arquivos sensíveis.
Contribuição
Contribuições são bem-vindas! Se você deseja melhorar o projeto ou sugerir novas funcionalidades, sinta-se à vontade para abrir um pull request ou issue no GitHub.

Licença
Este projeto está sob a licença MIT. Para mais informações, consulte o arquivo de licença.