import time
import datetime

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


def lets_pars_trans(name: str = None):

    ua = UserAgent(browsers=['chrome'])
    user_a = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'

    s = Service(executable_path='../home/footbal_bot/chromedriver/chromedriver')
    # s = Service(executable_path='C:\\Users\\Пользователь\\PycharmProjects\\football_bot\\chromedriver\\chromedriver.exe')
    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument(f"user-agent={ua.random}")
    options_chrome.add_argument("--disable-blink-features=AutomationControlled")
    options_chrome.add_argument('--headless')
    options_chrome.add_experimental_option('excludeSwitches', ['enable-automation'])
    options_chrome.add_experimental_option('useAutomationExtension', False)
    options_chrome.add_argument("--window-size=1920,1080")
    options_chrome.add_argument("--no-sandbox")
    options_chrome.add_argument('--blink-settings=imagesEnabled=false')     # это строка отклучает прогрузку медиа на сранице

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
        
        url: str = env('URL_TR')
        
        logger.debug('заходим на страницу ТМ')
        browser.get(url)
        # time.sleep(3)
        wait = WebDriverWait(browser, 60)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*")))

        # находим все фреймы на странице
        logger.debug('находим все фреймы на странице')
        frames = browser.find_elements(By.TAG_NAME, "iframe")
        # проходимся по фреймам, чтобы найти нужный и принятием куки и нажать "ПРИНЯТЬ ВСЕ"
        logger.debug('проходимся по фреймам')
        for frame in frames:
            if "sp_message_iframe" in frame.get_attribute("id"):
                # найден нужный фрейм
                logger.debug('найден нужный фрейм')
                # # переключаемся на фрейм
                browser.switch_to.frame(frame)

                # находим кнопку "ПРИНИМАТЬ ВСЕ" и нажимаем на неё
                logger.debug('находим кнопку "ПРИНИМАТЬ ВСЕ" и нажимаем на неё')
                button = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.sp_choice_type_11")))
                button.click()

        time.sleep(3)

        # name = 'Andreas Jungdal'
        name = 'Alexander Schlager'
        # вводим имя игрока в поле поиска
        # print('вводим имя игрока в поле поиска')
        # print(name)
        logger.debug('вводим имя игрока в поле поиска')
        logger.debug(name)
        search_input = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="schnellsuche"]/input[1]')))
        search_input.send_keys(name)
        # нажимаем Enter для поиска
        # print('нажимаем Enter для поиска')
        logger.debug('нажимаем Enter для поиска')
        search_input.send_keys(Keys.RETURN)

        time.sleep(3)

        # print('Проверяем наличие iframe с принятием политики конфеденциальности')
        logger.debug('Проверяем наличие iframe с принятием политики конфеденциальности')
        # находим все фреймы на странице
        frames = browser.find_elements(By.TAG_NAME, "iframe")
        # проходимся по фреймам, чтобы найти нужный и принятием куки и нажать "ПРИНЯТЬ ВСЕ"
        if frames:
            # print('на странице есть iframe')
            logger.debug('на странице есть iframe')
            for frame in frames:
                if "sp_message_iframe" in frame.get_attribute("id"):
                    # найден нужный фрейм, выполните здесь свой код
                    # print('iframe наиден, нажимаем на кнопку Принять всё')
                    logger.debug('iframe наиден, нажимаем на кнопку Принять всё')
                    # # переключаемся на фрейм
                    browser.switch_to.frame(frame)

                    # находим кнопку "ПРИНИМАТЬ ВСЕ" и нажимаем на неё
                    button = WebDriverWait(browser, 30).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button.sp_choice_type_11")))
                    browser.execute_script("arguments[0].click();", button)
                    # button.click()

        time.sleep(2)

        # периодически в цикле возникает ошибка stale element reference: element is not attached to the page document
        # пробуем обновить страницу, чтобы избежать этой ошибки
        browser.refresh()

        time.sleep(2)
        
        # если есть результаты поиска, то находим все строчки с результатом
        logger.debug('если есть результаты поиска, то находим все строчки с результатом')
        try:
            elements = WebDriverWait(browser, 40).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".odd, .even")))
        except Exception as e:
            logger.debug('результатов поиска нет')
            return False

        # print(name)
        # print(len(elements))
        logger.debug(name)
        logger.debug(len(elements))

        # print('находим нужное амплуа')
        logger.debug('находим нужное амплуа')
        need_amplua = False
        for element in elements:
            amplua = element.find_element(By.CLASS_NAME, 'zentriert')
            if amplua.text in ('В', 'ЛВ', 'ПВ', 'ОН', 'ЦН', 'Нападающий', 'АП'):
                # time.sleep(3)
                # print(element.text)
                logger.debug(element.text)
                # element.find_element(By.CLASS_NAME, 'hauptlink').click()
                link = element.find_element(By.CLASS_NAME, 'hauptlink')
                # print('Нужное амплуа найдено, нажимаем на ссылку на игрока')
                logger.debug('Нужное амплуа найдено, нажимаем на ссылку на игрока')
                link.find_element(By.TAG_NAME, 'a').click()
                # print('нажали на ссылку')
                need_amplua = True
                # print('Прерываем цикл')
                logger.debug('Прерываем цикл')
                break
        
        # print('check need_amplua')
        if not need_amplua:
            return False


        # time.sleep(1)
        # print('ждем прогрузки всей страницы')
        logger.debug('ждем прогрузки всей страницы')
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*")))
        
        # получаем страницу, чтобы при необходимости проверить, что она показывает
        page = browser.execute_script("return document.documentElement.outerHTML;")

        # создаем имя файла на основе текущей даты и времени
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"../bot/pages/{current_time}_{name}.html"
        # filename = f"pages\\{current_time}_{name}.html"

        # записываем страницу в файл
        logger.debug('записываем страницу в файл')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(page)

        # логируем сообщение в консоль
        logger.info(f'Страница сохранена в файл: {current_time}_{name}.html')
        
        # находим на странице элемент "Данные игрока", если этот элемент прогружен, значит вместе с ним должен быть прогружен элемент с травмой, если травма есть
        # print('ждем прогрузки элемента "Даные игрока"')
        logger.debug('ждем прогрузки элемента "Даные игрока"')
        wait.until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(), "Данные игрока")]')))
        
        # проверяем наличие поля с травмами на странице игрока
        element_exists = len(browser.find_elements(By.CSS_SELECTOR, ".verletzungsbox")) > 0
        # print('проверяем есть ли поле с травмой на странице')
        logger.debug('проверяем есть ли поле с травмой на странице')
        if element_exists:
            # print('Травма есть')
            logger.debug('Травма есть')
            res = True
        else:
            # print('Травмы нет')
            logger.debug('Травмы нет')
            res = False

        return res


if __name__ == '__main__':
    lets_pars_trans()
