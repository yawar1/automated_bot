from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

class SCRIPT:

    def __init__(self):
        self.bot = webdriver.Chrome('./driver') #path to driver
        self.bot.set_window_size(1800, 1000)
        self.bot.set_window_position(100,40)

    def implement(self, file_name):
        """
        gets product url and product sizes from file_name.
        """

        with open(file_name, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]

        for line in lines:
            words = line.split(',')
            url = words[0]
            sizes = words[1:]
            sizes = [size.strip(' []') for size in sizes]
            self.to_cart(url, sizes) #calling to_cart function
        

    def to_cart(self, url, sizes):
        """
        Adds product to cart with specific sizes if sizes are available, and gets other information.
        """
        self.bot.get(url)

        title = self.bot.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/h1/span')
        title = str(title.text).split()
        sku = title[-1]

        try:
            price = self.bot.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div/div/span')
        except NoSuchElementException:
            price = self.bot.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[4]/div/div/div[3]/div[2]/span')
        price = price.text

        size_options = self.bot.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[3]/div[2]')
        sizes_available = size_options.find_elements(By.TAG_NAME, 'div')
        not_sizes_available = size_options.find_elements(By.CLASS_NAME, 'so')

        sizes_available = [size for size in sizes_available if size not in not_sizes_available]

        added_sizes = []
        for sz in sizes_available:
            if sz.text in sizes:
                sz.click()
                time.sleep(5)
                try:
                    cart_button = self.bot.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[5]/button')
                    cart_button.click()
                except NoSuchElementException:
                    print('size not available')
                else:
                    added_sizes.append(int(sz.text))
                time.sleep(5)

        if added_sizes:
            self.mark_ordered(url, added_sizes, sku, price) #calling mark_ordered funtion

    def mark_ordered(self, url, added_sizes, sku, price):
        """
        Marks product as ordered which gets added to cart with available sizes and stores other required data to the output file.
        """

        line = f'{url}, {added_sizes} , ordered, {sku}, {price}\n'
        with open('output.csv', 'a') as f:
            f.write(line)
        return True


if __name__ == '__main__':
    app = SCRIPT()

    app.implement('input.csv')

    app.bot.quit()
