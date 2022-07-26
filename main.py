from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException


class InstagramBot():

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    #---метод для закрытия браузера
    def close_driver(self):

        self.driver.close()
        self.driver.quit()

    #---метод логина
    def login(self):

        driver = self.driver
        driver.get('https://www.instagram.com')
        time.sleep(random.randrange(4, 5))

        username_input = driver.find_element(by=By.NAME, value='username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(4)

        password_input = driver.find_element(by=By.NAME, value='password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

#---ФУНКЦИЯ СТАВИТ ЛАЙКИ ПО HASHTAG
    def like_photo_by_hashtag(self, hashtag):

        driver = self.driver
        driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):  # указываем количество скролов.!!!! либо убираем.
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = driver.find_elements(by=By.TAG_NAME, value='a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                driver.get(url)
                time.sleep(3)
                like_button = driver.find_element(by=By.XPATH,
                                                  value='/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(50, 70)) # Количество действий (подписок, отписок и пр.) не более 30 в час. Не более 720 в день. для аккаунтов старше 6 мес - 60/час.
            except Exception as ex:
                print(ex)
                self.close_driver()

#---Функция проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        driver = self.driver
        try:
            driver.find_element(by=By.XPATH, value=url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist


#---Функция ставит лайк на пост по прямой ссылке
    def put_exactly_like(self, userpost):

        driver = self.driver
        driver.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_driver()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/button').click()
            time.sleep(2)
            print(f"Лайк на пост: {userpost} поставлен!")
        self.close_driver()

#---ФУНКЦИЯ СОБИРАЕТ ССЫЛКИ НА ВСЕ ПОСТЫ ПОЛЬЗОВАТЕЛЯ
    def get_all_posts_urls(self, userpage):
        driver = self.driver
        driver.get(userpage)
        time.sleep(4)

        #---условие для проверки, если поста не существует, или ссылка не верна
        wrong_userpage = "/html/body/div[1]/section/main/div/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Пользователя не существует, проверьте URL")
            self.close_driver()
        else:
            print("Пользователь найден, ставим лайки!")
            time.sleep(2)

            #---Инстаграм при первой загрузке отдает 24 поста. Следующие подгружаются по 12 штук за скрол. Количество постов отображаются на странице аккаунта.
            #---Делим количество постов на 12 чтобы узнать необходимое количество скролов (прокруток).
            post_count = int(driver.find_element(by=By.XPATH,
                                                 value='/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[1]/div/span').text)
            loops_count = int(post_count / 12)
            print(loops_count)

            #---собираем все ссылки
            post_urls = []
            for i in range(0, loops_count):
                hrefs = driver.find_elements(by=By.TAG_NAME, value='a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                #---проходим по ссылкам и добавляем в наш список.
                for href in hrefs:
                    post_urls.append(href)

                #---код для скрола.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(4, 5))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            print(len(post_urls))
            for i in post_urls:
                print(i)

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in post_urls:
                    file.write(post_url + "\n")

            set_post_urls = set(post_urls)                   #---трансформирует список во множество (контейнер в котором собираются только уникальные, неупорядочные элементы).
            set_post_urls = list(set_post_urls)              #---трансформируем уникальные ссылки снова в список для удобной работы.

            with open(f'{file_name}_set.txt', 'a') as file:  #---Сохраняем неповторяющийся список в новый файл. (будет с пометкой set)
                for post_url in set_post_urls:
                    file.write(post_url + '\n')

        self.close_driver()

#---ФУНКЦИЯ СТАВИТ ЛАЙКИ НА ВСЕ ПОСТЫ УКАЗАННОГО АККАУНТА
    def put_many_likes(self, userpage):

        driver = self.driver
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        driver.get(userpage)
        time.sleep(4)

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list: #---[0:6] - количество постов для лайков. можно убрать и будет лайкать все.
                try:
                    driver.get(post_url)
                    time.sleep(2)

                    like_button = driver.find_element(by=By.XPATH, value='/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                    time.sleep(random.randrange(80, 100))
                    time.sleep(2)
                    print(f"Лайк на пост: {post_url} успешно поставлен!")

                except Exception as ex:
                    print(ex)
                    self.close_driver()

        self.close_driver()

my_bot = InstagramBot(username, password)
my_bot.login()
# my_bot.like_photo_by_hashtag("животные")                   #---ФУНКЦИЯ СТАВИТ ЛАЙКИ ПО HASHTAG
# my_bot.put_exactly_like("https://www.instagram.com/")      #---Функция ставит лайк на пост по прямой ссылке
# my_bot.get_all_posts_urls("https://www.instagram.com/")    #---ФУНКЦИЯ СОБИРАЕТ ВСЕ ССЫЛКИ НА ПОСТЫ И СОХРАНЯЕТ ИХ В ФАЙЛ
# my_bot.put_many_likes("https://www.instagram.com/")        #---ФУНКЦИЯ СТАВИТ ЛАЙКИ НА ВСЕ ПОСТЫ УКАЗАННОГО АККАУНТА




