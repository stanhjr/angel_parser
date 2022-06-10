from selenium.common.exceptions import InvalidSessionIdException, TimeoutException
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from fake_useragent import UserAgent
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from tools import parse_one_page

user_agent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--enable-javascript")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.maximize_window()
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
wait = WebDriverWait(driver, 10)
driver.get("https://angel.co/jobs")
actions = ActionChains(driver)

if __name__ == '__main__':
    try:
        time.sleep(20)
        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,
                                                   "#main > header > nav > div > a.mr-4.rounded.border.py-\[9\.6px\].px-4.font-arbeit.text-new-black.hover\:text-new-blue"))).click()

        wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#user_email")))
        input_email = driver.find_element(By.CSS_SELECTOR, "#user_email")
        input_password = driver.find_element(By.CSS_SELECTOR, "#user_password")
        time.sleep(1)
        input_email.send_keys("stanislav.o@cybearsoft.com")
        input_password.send_keys("Power5Power6Power7")
        time.sleep(1)
        wait.until(ec.presence_of_element_located(
            (By.CSS_SELECTOR, "#new_user > div.s-vgTop1_5.login-actions > input"))).click()
        time.sleep(15)
        old_title_for_page = []
        scroll = 0
        now = time.time()
        for i in range(10):
            print("old_title_for_page")
            print(len(old_title_for_page))
            old_title_list, scroll = parse_one_page(driver=driver,
                                                    wait=wait,
                                                    actions=actions,
                                                    old_title_for_page=old_title_for_page, scroll=scroll)

            old_title_for_page += old_title_list
            driver.execute_script(f"Y = window.pageYOffset; window.scrollTo(0, Y + 700)")
            time.sleep(4)
        print('Time over', time.time() - now)

    except TimeoutException:
        ...
    finally:
        driver.quit()
