#%%
import json
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

# Loop até coletar 3 posts
while len(profile_data) < 3:
    # Rolagem para carregar novos posts
    scroll_down(driver, times=1)
    sleep(2)  # Espera para carregamento
    page = driver.page_source  # Atualiza o código-fonte após rolagem
    soup = BeautifulSoup(page, 'lxml')
    
    # Encontrar posts
    posts_container = soup.find('div', {'class': 'scaffold-finite-scroll__content'})
    if not posts_container:
        continue
    
    posts = posts_container.find_all('div', class_='relative')
    
    for post in posts:
        post_id = post.get('data-id')
        if not post_id or post_id in post_ids_seen:
            continue  # Pula posts já processados
        
        post_ids_seen.add(post_id)
        
        try:
            # Reações
            try:
              social_metrics = post.find('ul', {'class': 'display-flex flex-wrap'})
              reactions = social_metrics.find('span', class_='social-details-social-counts__reactions-count').text.strip()
            except:
               reactions = '0'
            # Comentários
            try:
              comments_li = social_metrics.find('li', class_='social-details-social-counts__comments')
              comments = comments_li.find('button', {'aria-label': True}).text.strip()
            except:
               comments =  '0'
            # Compartilhamentos (tratamento de exceções caso não exista)
            try:
                shares_li = social_metrics.find('li', class_='social-details-social-counts__item--right-aligned')
                share = shares_li.find_next('button').find_next('button').text.strip()
            except:
                share = '0'
            
            # Nome do autor do post
            name_actor = post.find('a', class_='update-components-actor__image')
            actor = name_actor.get('aria-label') if name_actor else 'Desconhecido'

            profile_data.append({
                'actor': actor,
                'reacoes': reactions,
                'comentarios': comments,
                'compartilhamentos': share
            })
             
             # Para assim que coletar 3 posts
            if len(profile_data) >= 3:
                break
        
        except AttributeError as e:
            continue
        
with open('dados_posts.json', 'r', encoding='utf-8') as json_file:
    dados_existentes = json.load(json_file)

dados_existentes.extend(profile_data)

with open('dados_posts.json', 'w', encoding='utf-8') as json_file:
    json.dump(dados_existentes, json_file, ensure_ascii=False, indent=4)