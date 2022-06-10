import time

from selenium.common import WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By



def format_text(text:str) -> str:
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    return text


def parse_employee(driver, wait, actions):
    wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "#main > div.styles_component__VRc0I.styles_white__Nexe6 > div > div > div > div > div > div > div.styles_component__u4jsl > nav")))
    driver.execute_script('document.getElementsByClassName("styles_label___hqwO flex flex-row items-center")[1].click()')
    wait.until(ec.presence_of_element_located((By.CLASS_NAME, "styles_component__1kpJF")))
    founder_block = driver.find_element(By.CLASS_NAME, "styles_component__1kpJF")
    employee_list = []
    if founder_block:
        peoples = founder_block.find_elements(By.TAG_NAME, "h4")
        people_list = list(set([people.text for people in peoples]))
        for people in peoples:
            name = ''
            job_title = ''
            people_list.append(people.text)
            parent_elem = people.find_element_by_xpath('..')
            title = parent_elem.find_element(By.TAG_NAME, "span")
            name = people.text
            if title:
                job_title = format_text(title.text)
            employee_list.append({"name": name, "job_title": job_title})
    location_list = []
    location_block = driver.find_element(By.CSS_SELECTOR, "#main > div.styles_component__VRc0I.styles_white__Nexe6 > div > div > div > div > aside > div > div.styles_component__Wb41n.styles_component__qhaPy.styles_about__6dvji > dl > dt:nth-child(4) > ul")
    if location_block:
        locations = location_block.find_elements(By.TAG_NAME, "li")
        for loc in locations:
            location_list.append(loc.text)
    return employee_list, location_list


def parse_one_page(driver, wait, actions, old_title_for_page: list, scroll):
    old_list = frozenset(old_title_for_page)

    wait.until(ec.presence_of_element_located((By.CLASS_NAME, "styles_name__zvQcy")))
    all_title_for_page = driver.find_elements(By.CLASS_NAME, "styles_name__zvQcy")
    all_title_for_page = [item for item in all_title_for_page if item not in old_list]
    for title in all_title_for_page:
        try:
            actions.move_to_element(title).perform()
            driver.execute_script(f"Y = window.pageYOffset; window.scrollTo(0, Y + 200)")
            time.sleep(2)
            # if title.text and not data_api.check_company(title.text):
            #     print('continue')
            #     continue
            title.click()

            wait.until(ec.presence_of_element_located((By.CLASS_NAME, "styles_component__g_WAp")))

            flex_metadata = driver.find_element(By.CLASS_NAME, "styles_component__g_WAp")
            elements = flex_metadata.find_elements(By.TAG_NAME, "a")
            company_name = title.text
            company_links = []
            for el in elements:
                company_links.append(el.get_attribute("href"))

            description_elem = driver.find_element(By.CSS_SELECTOR, "div[class^='styles_description']")
            description = ''
            if description_elem:
                description = description_elem.text

            wait.until(ec.presence_of_element_located((By.CLASS_NAME, "styles_text__mcPtI")))
            wait.until(ec.presence_of_element_located((By.CLASS_NAME, "styles_footer__pNh_Y")))
            time.sleep(1)

            driver.execute_script('document.getElementsByClassName("styles_text__mcPtI")[0].click()')

            time.sleep(1)
            driver.execute_script(
                'footer = document.getElementsByClassName("styles_footer__pNh_Y")[0]; footer.getElementsByTagName("button")[0].click()')
            driver.switch_to.window(driver.window_handles[1])
            employee_list, location_list = parse_employee(driver=driver, wait=wait, actions=actions)

            print(company_name)
            print(company_links)
            print(description)
            print(employee_list)
            print(location_list)

            time.sleep(1)
            driver.close()

            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

            scroll += 400
        except WebDriverException:
            continue

    return all_title_for_page, scroll
