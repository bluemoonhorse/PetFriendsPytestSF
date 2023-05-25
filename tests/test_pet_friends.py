from api import PetFriends
import pytest
from settings import valid_email, valid_password, chinese_name, emoji_animal_type, pi_age, payload, payload2
import os

pf = PetFriends()



def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


# TC001
###тест 1 для нового метода простого пета 1 пост
def test_add_new_pet_with_simple_data(name='Простецкий', animal_type='дуб',
                                      age='88'):
    """Проверяем что можно добавить питомца с простыми данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pets_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# TC002
###тест 2 для нового метода обновления пут 2
def test_successful_update_self_pet(name='Пудинг', animal_type='обжора', age='3'):
    """Проверяем что можно обновить питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на обновление
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.put_update_info_about_pet(auth_key, pet_id, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# TC003
def test_get_api_key_for_invalid_user(email="qqqqqqqqqqqqqqqqqq@qqqqqqq.qqq", password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате не содержится слово key
    при неверной почте"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# TC004
def test_get_api_key_for_invalid_password(email=valid_email, password='123123123123123'):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате не содержится слово key
    при неверном пароле"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# TC005
def test_add_new_pet_with_complex_emoji_data(name=chinese_name, animal_type=emoji_animal_type, age=pi_age):
    """Проверяем что нельзя добавить питомца с большими и нестандартными данными
    В идеале эти строки нужно положить в файл. Но ломается open и на отладку уйдет много времени -- у меня, поэтому положил в settings"""

    """    
    f = open('test_add_new_pet_with_chinese_emoji_data.json', encoding='utf-8')
    data = json.load(f)
    name = data["name"]
    animal_type = data["animal_type"]
    age = data["age"] 
    """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pets_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400


# TC006
def test_add_new_pet_with_without_name(name="", animal_type='анонимный тест',
                                       age='123', pet_photo='images/solarcute.png'):
    """Проверяем что нельзя добавить питомца с пустыми данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 400


# TC007
def test_update_nonexistent_pet(name='Непознаваемый', animal_type='Невозможный', age='3'):
    """Проверяем что нельзя обновить несуществующего питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Берём нереальный id питомца и отправляем запрос на обновление
    pet_id = "7658754568753654678678945321235786"
    status, result = pf.put_update_info_about_pet(auth_key, pet_id, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом - должно быть 400 - нельзя
    assert status == 400


# TC008
def test_post_request_with_xss_payload(name=payload, animal_type=payload2,
                                       age=payload):
    """Проверяем что нельзя послать XSS"""
    """пожалуйста подскажите во время проверки, правильно ли я отправляю XSS, потому что он постится, но как строка
    и не совсем понятно, что подходит для XSS через pytest"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_create_pets_simple(auth_key, name, animal_type, age)

    assert status == 400


# TC009
def test_delete_nonexistent_pet(pet_id="literally nonexistent"):
    """Проверяем невозможность удаления несуществующего питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Проверяем что статус ответа равен не 200
    assert status != 200

# TC010
def test_delete_other_pet():
    """Проверяем возможность удаления чужого питомца"""

    # Получаем ключ auth_key и запрашиваем список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, other_pets = pf.get_list_of_pets(auth_key, "")

    # Сохраняем ID, удаляем чужого питомца
    pet_id = other_pets['pets'][0]['id']
    first_compare = pet_id
    #print("\n"+first_compare)
    #print(other_pets['pets'][0]['name'])
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список питомцев
    _, other_pets = pf.get_list_of_pets(auth_key, "")
    second_compare = other_pets['pets'][0]['id']
    #print("\n" + pet_id)
    #print(second_compare)

    # Проверяем что id первых в списке питомцев не изменился
    # assert status != 200
    assert first_compare == second_compare



