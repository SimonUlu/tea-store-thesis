## one specific services gets penetrated -> in this example f.e. it is the place order

from locust import HttpUser, task, between
import random
from bs4 import BeautifulSoup

class TeaStoreUser(HttpUser):
    wait_time = between(1, 10)
    host = "http://10.1.1.1:8080/tools.descartes.teastore.webui"
    product_id = 1 
    category_id = 1  
    user_postfix = 1
    browse_category_counter = 0 ## variable to simulate system errors

    def on_start(self):
        self.user_postfix = random.randint(1, 90)

    @task(3)
    def login(self):
        self.client.post("/loginAction", {"username": f"user{self.user_postfix}", "password": "password"})

    @task(2)
    def browse_category(self):
        self.browse_category_counter += 1  
        if self.browse_category_counter % 4 == 0:  
            response = self.client.get("/non-existing-page")
            print(f"Simulierter Fehler bei Aufruf {self.browse_category_counter}: Status Code {response.status_code}")
        else:
            self.client.get(f"/category?page=1&category={self.category_id}")

    @task(1)
    def view_product(self):
        self.client.get(f"/product?id={self.product_id}")

    @task(1)
    def add_to_cart(self):
        self.client.post("/cartAction", {"addToCart": "", "productid": self.product_id})

    @task(8)
    def place_order(self):
        self.client.post("/cartAction", {
            "firstname": "User",
            "lastname": "User",
            "address1": "Road",
            "address2": "City",
            "cardtype": "volvo",
            "cardnumber": "314159265359",
            "expirydate": "12/2050",
            "confirm": "Confirm"
        })

    @task(2)
    def get_random_category_id(self):
        response = self.client.get("/categories") 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        category_links = soup.find_all('a', href=True)
        category_ids = [link['href'] for link in category_links if 'category?id=' in link['href']]
        
        if category_ids:
            random_category_link = random.choice(category_ids)
            
            category_id = random_category_link.split('=')[1]
            return category_id
        
        return 1

    @task(3)
    def get_random_product_id(self):
        response = self.client.get("/category?page=1&category=1")  
        soup = BeautifulSoup(response.text, 'html.parser')
        product_links = soup.find_all('a', href=True)
        product_ids = [link['href'] for link in product_links if 'product?id=' in link['href']]
        if product_ids:
            random_product_link = random.choice(product_ids)
            product_id = random_product_link.split('=')[1]
            return product_id
        return 1  # base case

    @task(1)
    def logout(self):
        self.client.post("/loginAction", {"logout": ""})