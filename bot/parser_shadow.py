import csv
import time

from environs import Env
from selenium_stealth import stealth
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from loguru import logger

env = Env()
env.read_env()


def lets_pars_shadow():

    ua = UserAgent(browsers=['chrome'])
    user_a = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    # user_a_h = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/96.0.4664.110 Safari/537.36'

    # s = Service(executable_path="../home/footbal_bot/chromedriver/chromedriver")
    s = Service(executable_path='C:\\Users\\Пользователь\\PycharmProjects\\football_bot\\chromedriver\\chromedriver.exe')
    options_chrome = webdriver.ChromeOptions()
    # options_chrome.add_argument(f"user-agent={ua.random}")
    options_chrome.add_argument(f"user-agent={user_a}")
    options_chrome.add_argument("--disable-blink-features=AutomationControlled")
    options_chrome.add_argument('--headless')
    options_chrome.add_experimental_option('excludeSwitches', ['enable-automation'])
    options_chrome.add_experimental_option('useAutomationExtension', False)
    options_chrome.add_argument("--window-size=1920,1080")
    options_chrome.add_argument("--no-sandbox")
    options_chrome.add_argument('--blink-settings=imagesEnabled=false')     # это строка отклучает прогрузку медиа на сранице

    login: str = env('LOGIN')
    password: str = env('PASSWORD')

    with webdriver.Chrome(options=options_chrome, service=s) as browser:
        
        # скрываем следы использования бота в браузере
        stealth(browser,
                languages=["en-US", "en", "ru"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        # Убрать элементы, которые показывают, что работает автоматический скрипт
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
          '''
        })
        
        # скрываем отслеживание со стороны веб-сайта
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                    get: function() { return {"0":{"0":{}},"1":{"0":{}},"2":{"0":{},"1":{}}}; }
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ["en-US", "en", "ru"]
            });
            Object.defineProperty(navigator, 'mimeTypes', {
                get: function() { return {"0":{},"1":{},"2":{},"3":{}}; }
            });

            window.screenY=23;
            window.screenTop=23;
            window.outerWidth=1337;
            window.outerHeight=825;
            window.chrome =
            {
              app: {
                isInstalled: false,
              },
              webstore: {
                onInstallStageChanged: {},
                onDownloadProgress: {},
              },
              runtime: {
                PlatformOs: {
                  MAC: 'mac',
                  WIN: 'win',
                  ANDROID: 'android',
                  CROS: 'cros',
                  LINUX: 'linux',
                  OPENBSD: 'openbsd',
                },
                PlatformArch: {
                  ARM: 'arm',
                  X86_32: 'x86-32',
                  X86_64: 'x86-64',
                },
                PlatformNaclArch: {
                  ARM: 'arm',
                  X86_32: 'x86-32',
                  X86_64: 'x86-64',
                },
                RequestUpdateCheckStatus: {
                  THROTTLED: 'throttled',
                  NO_UPDATE: 'no_update',
                  UPDATE_AVAILABLE: 'update_available',
                },
                OnInstalledReason: {
                  INSTALL: 'install',
                  UPDATE: 'update',
                  CHROME_UPDATE: 'chrome_update',
                  SHARED_MODULE_UPDATE: 'shared_module_update',
                },
                OnRestartRequiredReason: {
                  APP_UPDATE: 'app_update',
                  OS_UPDATE: 'os_update',
                  PERIODIC: 'periodic',
                },
              },
            };
            window.navigator.chrome =
            {
              app: {
                isInstalled: false,
              },
              webstore: {
                onInstallStageChanged: {},
                onDownloadProgress: {},
              },
              runtime: {
                PlatformOs: {
                  MAC: 'mac',
                  WIN: 'win',
                  ANDROID: 'android',
                  CROS: 'cros',
                  LINUX: 'linux',
                  OPENBSD: 'openbsd',
                },
                PlatformArch: {
                  ARM: 'arm',
                  X86_32: 'x86-32',
                  X86_64: 'x86-64',
                },
                PlatformNaclArch: {
                  ARM: 'arm',
                  X86_32: 'x86-32',
                  X86_64: 'x86-64',
                },
                RequestUpdateCheckStatus: {
                  THROTTLED: 'throttled',
                  NO_UPDATE: 'no_update',
                  UPDATE_AVAILABLE: 'update_available',
                },
                OnInstalledReason: {
                  INSTALL: 'install',
                  UPDATE: 'update',
                  CHROME_UPDATE: 'chrome_update',
                  SHARED_MODULE_UPDATE: 'shared_module_update',
                },
                OnRestartRequiredReason: {
                  APP_UPDATE: 'app_update',
                  OS_UPDATE: 'os_update',
                  PERIODIC: 'periodic',
                },
              },
            };
            ['height', 'width'].forEach(property => {
                const imageDescriptor = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, property);

                // redefine the property with a patched descriptor
                Object.defineProperty(HTMLImageElement.prototype, property, {
                    ...imageDescriptor,
                    get: function() {
                        // return an arbitrary non-zero dimension if the image failed to load
                    if (this.complete && this.naturalHeight == 0) {
                        return 20;
                    }
                        return imageDescriptor.get.apply(this);
                    },
                });
            });

            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Open Source Technology Center';
                }
                if (parameter === 37446) {
                    return 'Mesa DRI Intel(R) Ivybridge Mobile ';
                }

                return getParameter(parameter);
            };

            const elementDescriptor = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'offsetHeight');

            Object.defineProperty(HTMLDivElement.prototype, 'offsetHeight', {
                ...elementDescriptor,
                get: function() {
                    if (this.id === 'modernizr') {
                    return 1;
                    }
                    return elementDescriptor.get.apply(this);
                },
            });
            '''
        })
        
        url: str = env('URL_SR')
        
        logger.debug('заходим на страницу СР')
        browser.get(url)
        time.sleep(10)

        # Находим кнопку логина с помощью аккаунта СР и нажимаем на неё
        # print('Находим кнопку логина с помощью аккаунта СР и нажимаем на неё')
        logger.debug('Находим кнопку логина с помощью аккаунта СР и нажимаем на неё')
        browser.find_element(By.XPATH, "//button[text()='Login with your Sorare account']").click()
        time.sleep(5)

        # Ждём прогрузки страницы и нажимаем принять куки
        # print('Ждём прогрузки страницы')
        logger.debug('Ждём прогрузки страницы')
        time.sleep(5)

        # Получить iframe, содержащий поля ввода логина и пароля
        # print('Получить iframe, содержащий поля ввода логина и пароля')
        logger.debug('Получить iframe, содержащий поля ввода логина и пароля')
        iframe = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#wallet")))

        # Переключить контекст на iframe
        # print('Переключить контекст на iframe')
        logger.debug('Переключить контекст на iframe')
        browser.switch_to.frame(iframe)
        time.sleep(10)

        # Найти элементы поля ввода логина и пароля и ввести соответствующие значения
        # print('Вводим email')
        logger.debug('Вводим email')
        email_field = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "Email")))
        email_field.send_keys(login)
        time.sleep(1)
        # print('Вводим пароль')
        logger.debug('Вводим пароль')
        password_field = WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "Password")))
        password_field.send_keys(password)
        time.sleep(1)

        # Найти элемент кнопки входа и нажать на нее
        # print('Нажимаем на кнопку войти')
        logger.debug('Нажимаем на кнопку войти')
        signin_button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Sign in']")))
        signin_button.click()

        # Ждём прогрузки страницы
        # print('Ждём прогрузки страницы')
        logger.debug('Ждём прогрузки страницы')
        time.sleep(10)

        # ждем, пока не появится кнопка "разрешить"
        # print('ждем, пока не появится кнопка "разрешить"')
        logger.debug('ждем, пока не появится кнопка "разрешить"')
        allow_button = WebDriverWait(browser, 60).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Разрешить"]')))

        # нажимаем на кнопку "разрешить"
        logger.debug('нажимаем на кнопку "разрешить"')
        allow_button.click()

        time.sleep(5)

        # print('заходим на страницу с фильтрами')
        logger.debug('заходим на страницу с фильтрами')
        
        # url_f: str = env('URL_SR_F')
        #
        # browser.get(url_f)
        #
        # time.sleep(10)
        #
        # # print('Нажимаем на вкладку Players')
        # logger.debug('Нажимаем на вкладку Players')
        # browser.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div[2]/div[2]/div').click()
        # time.sleep(5)
        #
        # # print('Нажимаем на кнопку Gk')
        # logger.debug('Нажимаем на кнопку Gk')
        # # нужно прокрутить до этого элемента, чтобы он стал виден
        # gk = browser.find_element(By.XPATH, "//p[text()='Gk']")
        # browser.execute_script("arguments[0].click();", gk)
        # time.sleep(5)
        #
        # # print('Нажимаем на кнопку For')
        # logger.debug('Нажимаем на кнопку For')
        # # нужно прокрутить до этого элемента, чтобы он стал виден
        # forw = browser.find_element(By.XPATH, "//p[text()='For']")
        # browser.execute_script("arguments[0].click();", forw)
        # time.sleep(5)
        #
        # # прокручиваем страницу ниже, к кнопке Filter
        # logger.debug('прокручиваем страницу ниже, к кнопке Filter')
        # browser.find_element(By.XPATH, "//button[contains(text(),'Filter')]").send_keys(Keys.DOWN)
        #
        # time.sleep(5)
        #
        # # print('Выбираем Injured')
        # logger.debug('Выбираем Injured')
        # # Находим элемент
        # element_injured = browser.find_element(By.CSS_SELECTOR, 'input.select-search__input[placeholder="Filter by availability status"]')
        #
        # time.sleep(5)
        #
        # element_injured.click()
        # time.sleep(5)
        # element_injured.send_keys(Keys.DOWN)
        # element_injured.send_keys(Keys.DOWN)
        # element_injured.send_keys(Keys.DOWN)
        # element_injured.send_keys(Keys.RETURN)
        #
        # time.sleep(5)
        #
        # # print('Нажимаем на кнопку Filter')
        # logger.debug('Нажимаем на кнопку Filter')
        # element_filter = browser.find_element(By.XPATH, "//button[contains(text(),'Filter')]")
        # browser.execute_script("arguments[0].click();", element_filter)

        # ниже кода для фильтра на странице рейтинга

        # print('заходим на страницу с фильтрами')
        url_r: str = env('URL_SR_R')

        browser.get(url_r)

        time.sleep(10)

        # print('Нажимаем на кнопку Gk')
        logger.debug('Нажимаем на кнопку Gk')
        gk = browser.find_element(By.XPATH, "//p[text()='Gk']")
        browser.execute_script("arguments[0].click();", gk)
        time.sleep(3)

        # print('Нажимаем на кнопку Filter')
        logger.debug('Нажимаем на кнопку Filter')
        element_filter = browser.find_element(By.XPATH, "//button[contains(text(),'Filter')]")
        browser.execute_script("arguments[0].click();", element_filter)

        time.sleep(3)

        # ждем, пока загрузится нужный элемент
        wait = WebDriverWait(browser, 30)
        players = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/player/"]')))

        # запоминаем начальное количество игроков
        prev_num_players = len(players)

        # прокручиваем страницу до тех пор, пока количество игроков не перестанет меняться
        # print('запускаем цикл прокрутки страницы до самого низа')
        logger.debug('запускаем цикл прокрутки страницы до самого низа')
        while True:
            time.sleep(5)
            # прокручиваем страницу до самого низа
            # print('прокручиваем')
            logger.debug('прокручиваем')
            browser.execute_script("arguments[0].scrollIntoView();", players[-1])
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            browser.execute_script("window.scrollBy(0, 500)")
            
            # ждем, пока не загрузятся новые игроки
            time.sleep(7)
            # wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*")))
            browser.execute_script("window.scrollBy(0, 500)")
            time.sleep(3)

            # получаем новый список игроков
            players = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/player/"]')

            # # если количество игроков на странице не изменилось, выходим из цикла
            # if len(players) == prev_num_players:
            #     break
            
            # если количество игроков на странице не изменилось, выходим из цикла
            # if len(players) == prev_num_players and len(players) > 75:
            if len(players) == prev_num_players and len(players) > 50:
                break

            # обновляем количество игроков
            prev_num_players = len(players)

        # print('Прокручиваем страницу до самого низа')
        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(5)

        # print('находим все элементы a с атрибутом href, который начинается на "/player/"')
        logger.debug('находим все элементы a с атрибутом href, который начинается на "/player/"')
        # находим все элементы a с атрибутом href, который начинается на "/player/" и выводим их текст
        links = browser.find_elements(By.CSS_SELECTOR, 'a[href^="/player/"]')

        names = []
        player_links = []

        # print('заполняем списки с именами и ссылками')
        logger.debug('заполняем списки с именами и ссылками')
        for link in links:
            # name = link.text
            name = link.find_element(By.CLASS_NAME, 'font-semibold').text
            player_link = link.get_attribute('href')
            names.append(name)
            player_links.append(player_link)

        # print('записываем данные в файл, если списки не пустые')
        logger.debug('записываем данные в файл, если списки не пустые')
        if names:
            with open('files/res.csv', 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                for n, p_l in zip(names, player_links):
                    writer.writerow([n, p_l])
        else:
            # print('списки с именами пустые')
            logger.debug('списки с именами пустые')

        time.sleep(3)


if __name__ == '__main__':
    lets_pars_shadow()

