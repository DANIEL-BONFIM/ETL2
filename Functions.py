#%%
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import json
from typing import List, Dict, Set, Optional

def scroll_down(driver: Chrome, times: int = 1) -> None:
     """
    EN: Make Scroll Down on the web page.

    Args:
        driver (Chrome): WebDriver Instance.
        times (int): Time for scrolling down.


     """

     for _ in range(times):
        driver.execute_script("window.scrollBy(0, 1000);")
        sleep(2)


def login(driver: Chrome, user: str, pwd: str) -> None:
    
    '''
    Open Bronswer, and put the link and credentials
    '''

    driver.get('https://www.linkedin.com/login')

    # Preencher credenciais
    email = driver.find_element(By.ID, 'username')
    email.send_keys(user)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(pwd)
    password.submit()

def load_existing_data(file_path: str) -> List[Dict[str, str]]:
    """
   Load data into a JSON.

    Args:
        file_path (str): Path of JSON.

    Returns:
        List[Dict[str, str]]: List of Posts .
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_data(file_path: str, data: List[Dict[str, str]]) -> None:
    """
    Save data into a JSON file.

    Args:
        file_path (str): path for JSON file.
        data (List[Dict[str, str]]): Data that need to be save.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def extract_post_data(post) -> Optional[Dict[str, str]]:

      ''' 
   Extract metrics on the page for each post
   
   Args: post - > Beaultiful Soup element
   Returns: Optional[Dict[str, str]] -> Dictionary with data of reactions, commments and shares
   
      '''
      try:

          post_id = post.get('data-id')
          if not post_id:
              return None

          try:
                #Reacations
                social_metrics = post.find('ul', {'class': 'display-flex flex-wrap'})
                reactions = social_metrics.find('span', class_='social-details-social-counts__reactions-count').text.strip()
          except:
                  reactions= '0'
              # Comments
          try:
                comments_li = social_metrics.find('li', class_='social-details-social-counts__comments')
                comments = comments_li.find('button', {'aria-label': True}).text.strip()
          except:
                 comments= '0'
              # Shares
          try:
                shares_li = social_metrics.find('li', class_='social-details-social-counts__item--right-aligned')
                share = shares_li.find_next('button').find_next('button').text.strip()
          except:
                share = '0'

          # Nome do autor do post
          name_actor = post.find('a', class_='update-components-actor__image')
          actor = name_actor.get('aria-label') if name_actor else 'Desconhecido'    

          return {
            'post_id': post_id,
            'actor': actor,
            'reacoes': reactions,
            'comentarios': comments,
            'compartilhamentos': share
            }
      

      except AttributeError as e:
          print(f"Erro ao extrair dados do post: {e}")
          return None
      
def scrape_linkedin_posts(driver: Chrome, max_posts: int) -> List[Dict[str, str]]:
    """
    Taking posts of LinkedIn.

    Args:
        driver (Chrome): WebDriver Instance.
        max_posts (int): Max number of posts took.

    Returns:
        List[Dict[str, str]]: Lists of posts.
    """
    profile_data = []
    post_ids_seen: Set[str] = set()

    while len(profile_data) < max_posts:
        scroll_down(driver, times=1)
        sleep(2)
        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        posts_container = soup.find('div', {'class': 'scaffold-finite-scroll__content'})
        if not posts_container:
            continue

        posts = posts_container.find_all('div', class_='relative')

        for post in posts:
            if len(profile_data) >= max_posts:
                break
            post_data = extract_post_data(post)
            if post_data and post_data['post_id'] not in post_ids_seen:
                # No considering Unknow actors
                if post_data['actor'] == 'Desconhecido':
                    continue

            post_data = extract_post_data(post)
            if post_data and post_data['post_id'] not in post_ids_seen:
                post_ids_seen.add(post_data['post_id'])
                profile_data.append(post_data)

    return profile_data


def main() -> None:
    """
    Main script.
    """
    output_file = 'linkedin_posts.json'
    driver = webdriver.Chrome()
    try:
        # Login into LinkedIn
        login(driver, user='danielbonfimsts@gmail.com', pwd='schalke04+05')

        # Load existent data
        existing_data = load_existing_data(output_file)
        existing_ids = {post['post_id'] for post in existing_data}

        # take new posts
        new_posts = scrape_linkedin_posts(driver, max_posts=100)
        unique_new_posts = [post for post in new_posts if post['post_id'] not in existing_ids]

        # add data 
        existing_data.extend(unique_new_posts)

        # Save json
        save_data(output_file, existing_data)
        print(f"Dados salvos com sucesso em: {output_file}")

    except Exception as e:
        print(f"Erro durante a execução: {e}")
