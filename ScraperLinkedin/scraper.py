from typing import Dict, Optional, List, Set
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from time import sleep
from ScraperLinkedin.utils import scroll_down


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
          print(f"Erro: {e}")
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