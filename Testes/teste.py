#%%
import os 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def scroll_down(driver, times=1):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, 1000);")
        sleep(2)

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login')

# Preencher credenciais
email = driver.find_element(By.ID, 'username')
email.send_keys('danielbonfimsts@gmail.com')
password = driver.find_element(By.ID, 'password')
password.send_keys('schalke04+05')
password.submit()

profile_data = []
post_ids_seen = set()
#%%

# Rolagem para carregar novos posts
page = driver.page_source  # Atualiza o código-fonte após rolagem
soup = BeautifulSoup(page, 'lxml')
    
   
social_metrics = soup.find('ul', {'class': 'display-flex flex-wrap'})
reactions = social_metrics.find('span', class_='social-details-social-counts__reactions-count').text.strip()

# Comentários
comments_li = social_metrics.find('li', class_='social-details-social-counts__comments')
comments = comments_li.find('button', {'aria-label': True}).text.strip()

shares_li = social_metrics.find('li', class_='social-details-social-counts__item--right-aligned')
share = shares_li.find_next('button').find_next('button').text.strip()

print(share)
#%%            
# Nome do autor do post
name_actor = post.find('a', class_='update-components-actor__image')
actor = name_actor.get('aria-label') if name_actor else 'Desconhecido'

profile_data.append({
    'actor': actor,
    'reacoes': reactions,
    'comentarios': comments,
    'compartilhamentos': share
})

# %%
