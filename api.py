import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """API-библиотека к веб-приложению 'Pet Friends'"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        """Магическая функция '__init__' присваивает всем экземплярам класса 'PetFriends' базовый URL"""

def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Функция добавляет информацию о новом питомце без фото и возвращает информацию в формате JSON"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Функция добавляет фото питомца к информации о существующем питомце и возвращает информацию в формате JSON"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result
