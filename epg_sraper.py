# Importing libraries
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def distribution_epg():
    check = 1
    while check == 1:
        # Link
        url = 'https://store.epicgames.com/ru/'

        # Path to ChromeDriver
        # chrome_driver_path = "chromedriver_win32\\chromedriver.exe"

        # # Creating an instance of the ChromeDriver service
        # service = Service(
        #     executable_path=chrome_driver_path
        # )
        # # Creating a ChromeDriver instance
        driver = webdriver.Chrome()
        try:
            # Request for a link
            driver.get(url=url)

            # Looking for a div with games
            games = driver.find_elements(By.CLASS_NAME, value="css-1myhtyb")

            for game in games:
                # Getting HTML code
                game = game.get_attribute('innerHTML')
                soup = BeautifulSoup(game, 'lxml')

                # Getting Names
                n = []
                i = []
                names = soup.find_all(class_="css-1h2ruwl")
                for name in names:
                    name = name.text
                    n.append(name)

                    # Getting src
                    img = soup.find('img', alt=name)
                    src = img.get('data-image')
                    i.append(src)

                # Getting status
                s = []
                json_data = []
                st_classes = ['css-11xvn05', 'css-gyjcm9']
                statuses = soup.find_all(class_=st_classes)
                for status in statuses:
                    status = status.text
                    # Cyrillic to Latin translation
                    if status == 'Сейчас бесплатно':
                        status = 'Now for free'
                    else:
                        status = 'Coming soon'
                    s.append(status)

                # Creating dictionaries
                for r in range(len(n)):
                    result = {
                        'NAME': n[r],
                        'SRC': i[r],
                        'STATUS': s[r]
                    }

                    # Integrity check
                    if result is None:
                        continue
                    else:
                        json_data.append(result)
                        check = check - 1
                return json_data

        except Exception as ex:
            print(ex)

        # Closing a ChromeDriver instance
        finally:
            driver.close()
            driver.quit()


if __name__ == "__main__":
    distribution_epg()
