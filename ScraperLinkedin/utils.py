import os
import json
from typing import List, Dict
from selenium.webdriver import Chrome
from time import sleep

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