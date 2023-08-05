import time
import logging
from enum import Enum

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import (NoSuchElementException,
                                        TimeoutException,
                                        ElementClickInterceptedException,
                                        UnexpectedAlertPresentException,
                                        WebDriverException)

from . import exceptions, schemas


class Selector(Enum):
    by_class_name = By.CLASS_NAME
    by_id = By.ID
    by_name = By.NAME
    by_xpath = By.XPATH


docker_remote_options = {
    'command_executor': "http://selenium:4444/wd/hub",
    'desired_capabilities': DesiredCapabilities.FIREFOX
}


class Crawler:
    """
    BASE CRAWLER CLASS
    """
    remote_options = docker_remote_options
    base_options = FirefoxOptions()
    base_options.headless = True

    def __init__(self, url: str, remote: bool = False, debug: bool = False):
        self.url = url
        self.remote = remote
        self.debug = debug
        self.driver = None

    def _init_driver(self) -> None:
        self.driver = self._get_driver()

    def _get_driver(self) -> WebDriver:
        if self.remote:
            return webdriver.Remote(**self.remote_options, options=self.base_options)
        if self.debug:
            self.base_options.headless = False
        return webdriver.Firefox(options=self.base_options)

    def start(self) -> None:
        # инициализируем драйвер явныи образом в момент запуска краулера
        self._init_driver()
        self.driver.get(self.url)

    def wait_element(self, selector: Selector, value: str) -> WebElement:
        # ждем появления и возвращаем элемент по типу селектора и значению
        wait = WebDriverWait(self.driver, 30)
        try:
            return wait.until(EC.visibility_of_element_located((selector.value, value)))
        except TimeoutException:
            raise exceptions.ElementHiddenException

    def element_is_exists(self, selector: Selector, value: str) -> bool:
        try:
            self.driver.find_element(selector.value, value)
        except NoSuchElementException:
            return False
        return True

    def stop(self) -> None:
        self.driver.quit()

    @classmethod
    def wait(cls, seconds: int = 5) -> None:
        time.sleep(seconds)


def attempted_crawling(attempts: int):
    # декоратор увеличения попыток краулинга
    def actual_decorator(func):

        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= attempts:
                logging.warning(f'ATTEMPT# {attempt}')
                try:
                    return func(*args, **kwargs)
                except (NoSuchElementException,
                        TimeoutException,
                        AttributeError,
                        WebDriverException,
                        ElementClickInterceptedException) as e:
                    logging.warning(e)
                    attempt += 1
            raise exceptions.FatalityException()

        return wrapper

    return actual_decorator


def logg_func_execution(func):
    def echo_func(*func_args, **func_kwargs):
        logging.warning(f'{func.__name__}: in process')
        result = func(*func_args, **func_kwargs)
        logging.warning(f'{func.__name__}: done')
        return result

    return echo_func


class AmoPartnerCrawler(Crawler):
    """
    CLASS FOR SCRAPING BILLING DATA FROM AMO PARTNER CABINET
    """

    def __init__(self, email: str, password: str, remote: bool, debug: bool = False):
        self.email = email
        self.password = password
        super().__init__(url='https://www.amocrm.ru/partners/private/shop/bill', remote=remote, debug=debug)

    @logg_func_execution
    def login(self, email: str, password: str) -> None:
        login_form_button = self.wait_element(Selector.by_class_name, 'page_header__auth_button')
        login_form_button.click()
        email_field = self.driver.find_element_by_class_name('form_auth__type_email')
        password_field = self.driver.find_element_by_class_name('form_auth__type_password')
        submit_login_button = self.driver.find_element_by_class_name('form_auth__button_submit')
        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_login_button.click()

    def unlock_screen(self) -> None:
        # избавление от всплывающего окна
        try:
            locker = self.driver.find_element_by_class_name('hb-animateIn')
            self.driver.execute_script("arguments[0].style.visibility='hidden'", locker)
        except NoSuchElementException:
            pass

    @property
    @logg_func_execution
    def billing_is_available(self):
        try:
            self.wait_element(Selector.by_class_name, 'js-months_without_discount')
            return False
        except exceptions.ElementHiddenException:
            return True

    @property
    @logg_func_execution
    def is_tech_account(self):
        self.unlock_screen()
        tariff_select = self.wait_element(Selector.by_class_name, 'extend-tariff-list')
        self.unlock_screen()
        selected_tariff = tariff_select.get_attribute("value")
        self.unlock_screen()
        logging.warning(selected_tariff)
        if int(selected_tariff) == 22000000:
            return True
        return False

    @property
    @logg_func_execution
    def account_id_is_recognized(self):
        try:
            self.unlock_screen()
            self.wait_element(Selector.by_class_name, 'bill_error')
            self.unlock_screen()
            return False
        except exceptions.ElementHiddenException:
            return True

    @logg_func_execution
    def fill_form(self, account_id: int) -> None:
        # заполнение биллинговой формы
        self.unlock_screen()
        account_id_field = self.wait_element(Selector.by_name, 'account_id')
        self.unlock_screen()
        account_id_field.send_keys(account_id)
        self.unlock_screen()
        if self.is_tech_account:
            raise exceptions.TechAccountException()
        self.wait(5)

        if not self.account_id_is_recognized:
            raise exceptions.IDNotFoundException()
        self.unlock_screen()
        currency_select_field = Select(self.wait_element(Selector.by_id, 'currency_id'))
        self.unlock_screen()
        currency_select_field.select_by_value("RUB")
        self.unlock_screen()
        self.wait(10)
        tariff_select_field = self.wait_element(Selector.by_id, 'tariff_id')
        # тариф иногда невозможно выбрать, стоит дефол
        if tariff_select_field.is_enabled():
            tariff_select = Select(tariff_select_field)
            tariff_select.select_by_value('19208542')
        self.unlock_screen()
        count_users_field = self.wait_element(Selector.by_id, 'col_users')
        self.wait(5)
        count_users_field.send_keys(0)
        self.wait()
        period_to_pay_select_field = Select(self.wait_element(Selector.by_id, 'period_id'))
        self.unlock_screen()
        period_to_pay_select_field.select_by_value('12')
        # пользователь мог уже оплатить, пробив билинга недоступен
        if not self.billing_is_available:
            raise exceptions.BillingNotAvailableException()
        self.wait(3)
        self.unlock_screen()
        contract_select_field = Select(self.wait_element(Selector.by_id, 'contract_id'))
        contract_select_field.select_by_value('10952733')

    @logg_func_execution
    def approve_form(self) -> None:
        # подтверждение формы и переход к тоталу по введенным данным
        self.wait()
        try:
            approve_bill_button = self.wait_element(Selector.by_id, 'start_bill')
            approve_bill_button.click()
            self.unlock_screen()
        # игнорируем диалоговое окном
        except UnexpectedAlertPresentException:
            pass

    @logg_func_execution
    def extract_data(self) -> dict:
        self.wait()
        tariff = self.wait_element(Selector.by_xpath, "//div[contains(@class, 'tariff_value')]/input")
        count_users = self.driver.find_element(By.XPATH, "//div[contains(@class, 'col_user')]/div[2]/input")
        pay_period = self.driver.find_element(By.XPATH, "(//div[@class='row_field'])[3]/input")
        price = self.driver.find_element(By.XPATH, "(//div[@class='row_field'])[4]/input")
        return {'price': price.get_attribute('value'),
                'users_count': count_users.get_attribute('value'),
                'tariff': tariff.get_attribute('value'),
                'pay_period': pay_period.get_attribute('value')}

    @attempted_crawling(attempts=3)
    def get_billing_data(self, account_id: int) -> schemas.BillingSchema:
        self.start()
        logging.warning('START')
        self.unlock_screen()
        # если не авторизованы - логинимся
        if not self.element_is_exists(Selector.by_id, 'user-select__header'):
            self.unlock_screen()
            self.login(self.email, self.password)
            self.unlock_screen()
        try:
            self.fill_form(account_id=account_id)
            self.approve_form()
            data = self.extract_data()
            self.stop()
            return schemas.BillingSchema(**data, is_paid=False)
        except exceptions.BillingNotAvailableException:
            self.stop()
            return schemas.BillingSchema(is_paid=True)
        except (exceptions.IDNotFoundException,
                exceptions.FatalityException,
                exceptions.TechAccountException):
            self.stop()
            return schemas.BillingSchema()
