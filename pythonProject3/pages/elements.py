import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored

class PageElements(object):
    _locator = ('', '')
    _web_driver = None
    _page = None
    _timeout = 10
    _wait_after_click = False

    def __init__(self, timeout=10, wait_after_click=False, **kwargs):
        self._timeout = timeout
        self._wait_after_click = wait_after_click

        for attr in kwargs:
            self._locator = (str(attr).replace('_', ' '), str(kwargs.get(attr)))

    def find(self, timeout=10):

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_element_located(self._locator)
            )
        except:
            print(colored('Элемент не найден на странице', 'red'))

        return element

    def wait_to_be_clickable(self, timeout=10, check_visibility=True):

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.element_to_be_clickable(self._locator)
            )
        except:
            print(colored('На выбранный элемент нельзя кликнуть', 'red'))

        if check_visibility:
            self.wait_until_not_visible()

        return element

    def is_clickable(self):

        element = self.wait_to_be_clickable(timeout=0.1)
        return element is not None

    def is_presented(self):

        element = self.find(timeout=0.1)
        return element is not None

    def is_visible(self):

        element = self.find(timeout=0.1)

        if element:
            return element.is_displayed()

        return False

    def wait_until_not_visible(self, timeout=10):

        element = None

        try:
            element = WebDriverWait(self._web_driver, timeout).until(
                EC.visibility_of_element_located(self._locator)
            )
        except:
            print(colored('Элемент отсутствует', 'red'))

        if element:
            js = ('return (!(arguments[0].offsetParent === null) && '
                  '!(window.getComputedStyle(arguments[0]) === "none") &&'
                  'arguments[0].offsetWidth > 0 && arguments[0].offsetHeight > 0'
                  ');')
            visibility = self._web_driver.execute_script(js, element)
            iteration = 0

            while not visibility and iteration < 10:
                time.sleep(0.5)

                iteration += 1

                visibility = self._web_driver.execute_script(js, element)
                print('Element {0} visibility: {1}'.format(self._locator, visibility))

        return element

    def send_keys(self, keys, wait=2):

        keys = keys.replace('\n', '\ue007')

        element = self.find()

        if element:
            element.click()
            element.clear()
            element.send_keys(keys)
            time.sleep(wait)
        else:
            msg = 'Элемент с локатором {0} не найден'
            raise AttributeError(msg.format(self._locator))

    def get_text(self):

        element = self.find()
        text = ''

        try:
            text = str(element.text)
        except Exception as e:
            print('Ошибка: {0}'.format(e))

        return text

    def get_attribute(self, attr_name):

        element = self.find()

        if element:
            return element.get_attribute(attr_name)

    def _set_value(self, web_driver, value, clear=True):
        element = self.find()

        if clear:
            element.clear()

        element.send_keys(value)

    def click(self, hold_seconds=0, x_offset=1, y_offset=1):

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).click(on_element=element).perform()
        else:
            msg = 'Элемент с локатором {0} не найден'
            raise AttributeError(msg.format(self._locator))

        if self._wait_after_click:
            self._page.wait_page_loaded()

    def right_mouse_click(self, x_offset=0, y_offset=0, hold_seconds=0):

        element = self.wait_to_be_clickable()

        if element:
            action = ActionChains(self._web_driver)
            action.move_to_element_with_offset(element, x_offset, y_offset). \
                pause(hold_seconds).context_click(on_element=element).perform()
        else:
            msg = 'Элемент с локатором {0} не найден'
            raise AttributeError(msg.format(self._locator))

    def highlight_and_make_screenshot(self, file_name='element.png'):

        element = self.find()

        self._web_driver.execute_script("arguments[0].scrollIntoView();", element)


        self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        self._web_driver.save_screenshot(file_name)

    def scroll_to_element(self):

        element = self.find()

        try:
            element.send_keys(Keys.DOWN)
        except Exception as e:
            pass

    def delete(self):

        element = self.find()

        self._web_driver.execute_script("arguments[0].remove();", element)


class ManyWebElements(PageElements):

    def __getitem__(self, item):

        elements = self.find()
        return elements[item]

    def find(self, timeout=10):

        elements = []

        try:
            elements = WebDriverWait(self._web_driver, timeout).until(
                EC.presence_of_all_elements_located(self._locator)
            )
        except:
            print(colored('Элементы не найдены на странице', 'red'))

        return elements

    def _set_value(self, web_driver, value):
        raise NotImplemented('Данное дейтсвие нельзя совершить с выбранными элементами')

    def click(self, hold_seconds=0, x_offset=0, y_offset=0):
        raise NotImplemented('Данное действие нельзя совершить с выбранными элементами')

    def count(self):

        elements = self.find()
        return len(elements)

    def get_text(self):

        elements = self.find()
        result = []

        for element in elements:
            text = ''

            try:
                text = str(element.text)
            except Exception as e:
                print('Ошибка: {0}'.format(e))

            result.append(text)

        return result

    def get_attribute(self, attr_name):

        results = []
        elements = self.find()

        for element in elements:
            results.append(element.get_attribute(attr_name))

        return results

    def highlight_and_make_screenshot(self, file_name='element.png'):

        elements = self.find()

        for element in elements:
            self._web_driver.execute_script("arguments[0].scrollIntoView();", element)

            self._web_driver.execute_script("arguments[0].style.border='3px solid red'", element)

        self._web_driver.save_screenshot(file_name)