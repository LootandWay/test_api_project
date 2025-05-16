# Импортировать стороннюю библиотеку для создания HTTP-запросов.
import requests

# Импортировать модуль тестов из Python.
import unittest
import json
import os


# Объявить класс для тестов.
class Test_Example(unittest.TestCase):
    # Инициализация и открытие файла
    def setUp(self) -> None:
        # Файл с фактами котов
        self.file_path = os.path.join(os.path.dirname(__file__),'response_1747137860506.json')
        with open(self.file_path,'r',encoding='utf-8') as f:
            self.data = json.load(f)   
        # Файл с описанием котов        
        self.file_path2 = os.path.join(os.path.dirname(__file__),'response_1747149822775.json')
        with open(self.file_path2,'r',encoding='utf-8') as f2:
            self.breeds = json.load(f2)
        # Ссылка на гугл    
        self.url = "https://google.com"
        # Ссылка на кэтфакты
        self.urlcat = "https://catfact.ninja/fact"
        # Ссылка на магазин питомцев
        self.urlpet = "https://petstore.swagger.io/v2/store/order"

    # Объявить метод для теста HTTP-запроса.
    def test_send_request_http200(self) -> None:
        # Объявить URL.
        # Создать GET-запрос на google.com.
        output = requests.get(self.url)
        # Проверить статус кода от GET-запроса на google.com.
        self.assertEqual(output.status_code, 200)

    # Объявить метод для теста JSON-ответа из случайного API.
    def test_read_json_cat_api_rnd_facts(self) -> None:
        # Создать GET-запрос на URL.
        output = requests.get(self.urlcat)
        # Проверить статус кода от GET-запроса на URL.
        self.assertEqual(output.status_code, 200)
        # Прочитать и проверить JSON-ответ от запроса.
        output_json = output.json()
        expected_keys = ["fact", "length"]
        actual_keys = output_json.keys()
        self.assertCountEqual(expected_keys, actual_keys)
    
    # Тест значения длинны , что значение не явлается пустым.
    def test_read_json_api_response_body(self) -> None:
        openurl = requests.get(self.urlcat)
        self.assertEqual(openurl.status_code, 200)
        response_json = openurl.json()
        print('\nРандомный факт -',response_json["fact"])
        self.assertNotEqual(response_json["length"], None)
    
    # Тест на совпадение длинны строки 6
    def test_length_from_file_5pos(self):
        fact_position = self.data["data"][5]
        expected_fact= "Cats make about 100 different sounds. Dogs make only about 10."
        expected_length = 62
        actual_length = self.data["data"][5].get('length')
        actual_fact= self.data["data"][5].get('fact')
        self.assertEqual(actual_length,expected_length)
        self.assertEqual(expected_fact,actual_fact)
        print('\nАктуальный факт 6 строки-',actual_fact, '\nАктуальная длинна 6 строки-',actual_length)
    
    # Тест 11 строки из файла пород, что поведение не внесено
    def test_breeds_file_pattern_none(self) -> None:
        actual_pattern = self.breeds["data"][11].get('pattern')
        self.assertEqual(actual_pattern,"")

    # Тест структуры запроса с фактами котов
    def test_structure_file_cat_facts(self) -> None:
        response = requests.get(self.urlcat)
        self.assertEqual(response.status_code,200)
        json_data = response.json()
        self.assertIn("fact",json_data)
        self.assertIn("length",json_data)
        self.assertIsInstance(json_data['fact'],str)
        self.assertIsInstance(json_data['length'],int)

    # Протестировать заказ на питомца 
    def test_add_order_in_store(self) -> None:
        data = {
            "id": 5,
            "petId": 2323,
            "quantity": 3434,
            "shipDate": "2999-06-14T13:42:40.471Z",
            "status": "placed",
            "complete": "true"
        }
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(self.urlpet, json=data, headers=headers)
        self.assertEqual(response.status_code, 200)
        data= response.json()
        self.assertEqual(data['status'],'placed')
        self.assertEqual(data['complete'],True)
        return (data['id'])


    # Протестировать добавление нового питомца в магазин
    def test_add_new_pet_in_store(self) -> None:
        url= "https://petstore.swagger.io/v2/pet"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"}
        data = {
            "id": 213213,
            "category": {
                "id": 2,
                "name": "Bobik"
            },
            "name": "BobikStyle",
            "photoUrls": ['string'],
            "tags":[
                {
                    "id": 2,
                    "name": "Polet"
                }
            ],
            "status": "available"
        } 
        response=requests.post(url, json=data,headers=headers)
        self.assertEqual(response.status_code,200)
        data=response.json()
        expected_status = ["available", "pending", "sold"]
        self.assertIn(expected_status[0],data['status'])

    # Протестирвать обновление текущего питомца
    def test_update_the_pet(self) -> None:
        url = "https://petstore.swagger.io/v2/pet"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"}
        data = {
            "id":1,
            "category": {
                "id": 0,
                "name": "string"
            },
            "name": "doggie",
            "photoUrls": ['string'],
            "tags":[
                {
                    "id": 2,
                    "name": "string"
                }
            ],
            "status": "available"
        }
        
        response=requests.put(url, headers=headers, json=data)
        self.assertEqual(response.status_code,200)
        data=response.json()
        print(data)


    # Протестировать удаление питомца 
    def test_delete_the_pet(self) -> None:
        url = 'https://petstore.swagger.io/v2/pet/1'
        headers = {"accept": "application/json"}
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code,200)
    
    # Получить и протестировать данные о магазине
    def test_invenrory(self) -> None:
        url = 'https://petstore.swagger.io/v2/store/inventory'
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code,200)
        data= response.json()
        print("\n Интвентарь магазина", data)
        for key,value in data.items():
            with self.subTest(key=key):
                self.assertTrue(isinstance(value,int),f"Значение для ключа:'{key}' не является числом: '{value}'")
                self.assertNotEqual(key.strip(),"",f"Пустой ключ:{key}")

    # Удаление заказа по айди
    def test_delete_order(self) ->None:
        id = self.test_add_order_in_store()
        url_del='https://petstore.swagger.io/v2/store/order/'+str(id)
        headers_del = {"accept": "application/json"}
        print("\n Айди ордера заказа:",self.test_add_order_in_store())
        response_del = requests.delete(url_del)
        self.assertEqual(response_del.status_code, 200)

    # Тест создания пользователя
    def test_create_new_user(self) -> None:
        url= 'https://petstore.swagger.io/v2/user'
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"}
        data = {"id": 3,
                "username": "BobMain",
                "firstName": "Petr",
                "lastName": "Petrov",
                "email": "dotaass@mail.ru",
                "password": "zxc111",
                "phone": "string",
                "userStatus": 0 
            }
        response = requests.post(url,headers=headers,json=data)
        self.assertEqual(response.status_code,200)
        data = response.json()
        print('\nОтвет на создание пользователя',data)


# Инициализировать условный оператор для точечного запуска тестов.
if __name__ == "__main__":
    unittest.main()
