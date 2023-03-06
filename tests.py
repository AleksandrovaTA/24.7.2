from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_add_new_pet_without_photo_with_valid_data(name='Дин', animal_type='зебра', age='5'):
    """Проверка возможности добавления питомца без фото с корректными данными"""

    # Запрос API-ключа
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)

    # Добавление нового питомца
    status, result = ptFnd.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_photo_and_empty_data(name='', animal_type='', age='', pet_photo='images/zebra.jpg'):
    """Проверка невозможности добавления питомца с фото и незаполненными данными (БАГ! Так не должно быть!)"""

    # Запрос API-ключа
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)

    # Получение полного пути изображения питомца и его сохранение в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавление нового питомца
    status, result = ptFnd.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_without_photo_and_with_empty_data(name='', animal_type='', age=''):
    """Проверка невозможности добавления питомца без фото и с незаполненными данными """

    # Запрос API-ключа
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)

    # Добавление нового питомца
    status, result = ptFnd.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_set_photo_pet(pet_photo='images/zebra.jpg'):
    """Проверка возможности добавления фото к информации о 'своем питомце'"""

    # Запрос API-ключа и списка 'своих питомцев'
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)
    _, my_pets = ptFnd.get_list_of_pets(auth_key, 'my_pets')

    # Если список 'своих питомцев' не пустой, происходит добавление фото
    if len(my_pets['pets']) > 0:
        status, result = ptFnd.set_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Сопоставление полученных данных с ожидаемым результатом
        assert status == 200
        assert result['pet_photo']
    else:
        # Если список 'своих питомцев' пустой, всплывает исключение с текстом об отсутствии 'своих питомцев'
        raise Exception('There is no my pets')


def test_get_api_key_with_empty_user_data(email=empty_email, password=empty_password):
    """Проверка того, что запрос API-ключа c пустыми значениями логина и пароля пользователя возвращает статус '403'
    и что результат не содержит слово 'key'"""

    # Отправка запроса и сохранение полученного ответа с кодом статуса в 'status', а текста ответа - в 'result'
    status, result = ptFnd.get_api_key(email, password)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 403
    assert 'key' not in result


def test_get_api_key_with_empty_user_password(email=valid_email, password=empty_password):
    """Проверка того, что запрос API-ключа c валидным значением логина и пустым значением пароля пользователя
    возвращает статус '403' и что результат не содержит слово 'key'"""

    # Отправка запроса и сохранение полученного ответа с кодом статуса в 'status', а текста ответа - в 'result'
    status, result = ptFnd.get_api_key(email, password)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_empty_key(filter=''):
    """Проверка того, что запрос списка всех питомцев c пустым значением API-ключа возвращает статус '403'"""

    # Запрос полного списка питомцев
    status, result = ptFnd.get_list_of_pets(empty_auth_key, filter)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 403


def test_get_all_pets_with_incorrect_key(filter=''):
    """Проверка того, что запрос списка всех питомцев c некорректным значением API-ключа возвращает статус '403'"""

    # Запрос полного списка питомцев с некорректным ключом
    status, result = ptFnd.get_list_of_pets(incorrect_auth_key, filter)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 403


def test_add_new_pet_with_incorrect_age(name='Дон', animal_type='Зебра',
                                        age='-2', pet_photo='images/zebra.jpg'):
    """Проверка невозможности добавления питомца с отрицательным возрастом """

    # Запрос API-ключа
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)

    # Получение полного пути изображения питомца и его сохранение в переменную 'pet_photo'
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавление нового питомца
    status, result = ptFnd.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 200
    assert result['age'] == age


def test_delete_not_own_pet():
    """Проверка невозможности удаления 'не своего питомца' """

    # Запрос API-ключа и списка всех питомцев
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)
    _, all_pets = ptFnd.get_list_of_pets(auth_key, '')

    # Если список не пустой, происходит отправка запроса на удаление первого питомца
    if len(all_pets['pets']) > 0:
        pet_id = all_pets['pets'][0]['id']
        status = ptFnd.delete_pet(auth_key, pet_id)

        # Сопоставление полученных данных с ожидаемым результатом
        assert status == 200
        assert pet_id not in all_pets.values()
    else:
        # Если список питомцев пустой, всплывает исключение с текстом об отсутствии питомцев
        raise Exception('There is no pets')


def test_update_not_own_pet_info(name='Сэм', animal_type='енот', age='7'):
    """Проверка невозможности обновления информации о 'не своем питомце' """

    # Запрос API-ключа и списка всех питомцев
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)
    _, all_pets = ptFnd.get_list_of_pets(auth_key, '')

    # Если список не пустой, происходит обновление имени, типа и возраста питомца
    if len(all_pets['pets']) > 0:
        status, result = ptFnd.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)

        # Сопоставление полученных данных с ожидаемым результатом
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, всплывает исключение с текстом об отсутствии питомцев
        raise Exception('There is no pets')


def test_set_photo_not_own_pet(pet_photo='images/deer.jpg'):
    """Проверка возможности добавления фото к информации о 'не своем питомце'"""

    # Запрос API-ключа и списка всех питомцев
    _, auth_key = ptFnd.get_api_key(valid_email, valid_password)
    _, all_pets = ptFnd.get_list_of_pets(auth_key, '')

    # Если список не пустой, происходит добавление фото
    if len(all_pets['pets']) > 0:
        pet_id = all_pets['pets'][0]['id']
        status, result = ptFnd.set_photo_pet(auth_key, pet_id, pet_photo)

        # Сопоставление полученных данных с ожидаемым результатом
        assert status == 500
    else:
        # Если список питомцев пустой, всплывает исключение с текстом об отсутствии питомцев
        raise Exception('There is no pets')
        
