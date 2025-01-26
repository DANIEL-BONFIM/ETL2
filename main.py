from ScraperLinkedin.scraper import scrape_linkedin_posts
from ScraperLinkedin.Auth import login
from ScraperLinkedin.utils import load_existing_data, save_data, scroll_down
from selenium.webdriver import Chrome
from selenium import webdriver


def main(user:str, pwd: str) -> None:
    """
    Main script.
    """
    output_file = r'Raw/linkedin_posts.json'
    driver = webdriver.Chrome()
    try:
        # Login into LinkedIn
        login(driver, user, pwd)

        # Load existent data
        existing_data = load_existing_data(output_file)
        existing_ids = {post['post_id'] for post in existing_data}

        # take new posts
        new_posts = scrape_linkedin_posts(driver, max_posts=10)
        unique_new_posts = [post for post in new_posts if post['post_id'] not in existing_ids]

        # add data 
        existing_data.extend(unique_new_posts)

        # Save json
        save_data(output_file, existing_data)
        print(f"Saving process was successful: {output_file}")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main('danielbonfimsts@gmail.com','sch@lke04+05')

