from pandas_gbq import to_gbq
from google.oauth2 import service_account
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import logging
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Autenticação BigQuery
credencial = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
    scopes=["https://www.googleapis.com/auth/bigquery"]
)

# Iniciar WebDriver com Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
games = []

try:
    # Acessar o site SteamDB
    driver.get("https://steamdb.info/sales/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "DataTables_Table_0")))

    # Função para rolar a página até o final
    def scroll_down_page(speed=10):
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

    # Função para extrair dados da página
    def extract_data_from_page(soup):
        table = soup.find(id="DataTables_Table_0")
        rows = table.find_all("tr", class_="app")
        for row in rows:
            data_cells = row.find_all("td")
            game_data = {
                "Nome": data_cells[2].find("a").text.strip(),
                "Desconto": data_cells[3].text.strip(),
                "Preço": data_cells[4].text.strip(),
                "Avaliação": data_cells[5].text.strip(),
                "Lançamento": data_cells[6].text.strip(),
                "Termina": data_cells[7].text.strip(),
                "Começou": data_cells[8].text.strip()
            }
            logging.info(game_data)
            games.append(game_data)

    # Extração dos dados
    while True:
        scroll_down_page()  # Rolar a página até o final
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        extract_data_from_page(soup)

        # Verificar se há uma próxima página
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'button.dt-paging-button.next')
            if next_button.get_attribute('aria-disabled') == 'true':
                break
            next_button.click()
            WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
        except Exception as e:
            logging.error(f"Erro ao navegar: {e}")
            break
finally:
    driver.quit()

# Criação de DataFrame com os dados extraídos
df = pd.DataFrame(games)

# Envio para o BigQuery
try:
    to_gbq(df, destination_table=os.getenv('BIGQUERY_TABLE'),
           project_id=os.getenv('BIGQUERY_PROJECT_ID'),
           if_exists='replace', credentials=credencial)
    logging.info("Dados carregados com sucesso no BigQuery")
except Exception as e:
    logging.error(f"Erro ao carregar dados no BigQuery: {e}")
