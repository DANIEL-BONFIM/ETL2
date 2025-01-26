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
            # Extrair métricas
            social_metrics = post.find('ul', {'class': 'display-flex flex-wrap'})
            
            # Reações
            reactions = social_metrics.find(
                'span', class_='social-details-social-counts__reactions-count'
            ).text.strip()
            
            # Comentários
            comments_btn = social_metrics.find(
                'button', {'aria-label': lambda x: x and 'comentários' in x.lower()}
            )
            comments = comments_btn.text.strip() if comments_btn else '0'
            
            # Compartilhamentos
            shares_btn = social_metrics.find(
                'button', {'aria-label': lambda x: x and 'compartilhamentos' in x.lower()}
            )
            shares = shares_btn.text.strip() if shares_btn else '0'
            
            # Autor do post
            actor_link = post.find('a', class_='update-components-actor__image')
            actor = actor_link.get('aria-label', 'Desconhecido') if actor_link else 'Desconhecido'
            
            profile_data.append({
                'actor': actor,
                'reacoes': reactions,
                'comentarios': comments,
                'compartilhamentos': shares
            })
            
            # Para assim que coletar 3 posts
            if len(profile_data) >= 3:
                break
        
        except AttributeError as e:
            continue

# Fechar o navegador e exibir resultados
driver.quit()
print(profile_data[:3])  # Garante apenas os 3 primeiros