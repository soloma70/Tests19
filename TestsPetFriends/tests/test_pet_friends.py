from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# Блок тестов на получение api ключа

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Позитивный тест получения API ключа для зарегистрированного пользователя. Проверяем, что
    запрос возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_negativ_get_api_key_for_non_password_user(email=valid_email, password=''):
    """Негативный тест получения API ключа для пользователя, у которого не введен пароль. Проверяем,
    что запрос возвращает код ошибки 403, означающий что комбинацию логина и пароля неверна, а так же
    нет слова key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_negativ_get_api_key_for_non_email_user(email='', password=valid_password):
    """Негативный тест получения API ключа для пользователя, у которого не введен email. Проверяем,
    что запрос возвращает код ошибки 403, означающий что комбинацию логина и пароля неверна, а так же
    нет слова key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_negativ_get_api_key_for_non_valid_user(email='Gbgdgn@gsgl.com', password='Dv%f;dGew435'):
    """Негативный тест получения API ключа для незарегистрированного пользователя. Проверяем, что запрос
    возвращает код ошибки 403, означающий что комбинацию логина и пароля неверна, а так же нет слова key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# Блок тестов на проверку списка питомцев

def test_get_all_pets_with_valid_key(filter=''):
    """Позитивный тест получения не пустого списка питомцев по фильтру 'Все питомцы'. Сначала получаем API ключ.
    После поверяем, что запрос возвращает статус 200 и список питомцев не пустой (фильтр 'Все питомцы')"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Позитивный тест получения не пустого списка питомцев по фильтру 'Мои питомцы'. Сначала получаем API ключ.
    После поверяем, что запрос возвращает статус 200 и список питомцев не пустой (фильтр 'Мои питомцы')"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_negativ_get_all_pets_with_non_valid_key(filter=''):
    """Негативный тест получения списка питомцев по фильтру 'Все питомцы' при невалидном API ключе.
    После поверяем, что запрос возвращает статус 403 и в тексте ответа есть слово Forbidden"""
    auth_key = {'key': 'ksa344ldld'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
    assert 'Forbidden' in result


# Блок тестов на проверку добавления питомцев

def test_add_new_pet_with_valid_data(name='Матюся', animal_type='британец', age='9', pet_photo='images/cat11.jpg'):
    """Позитивный тест добавления нового питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_negativ_add_new_pet_with_non_valid_key(name='Матюся', animal_type='британец', age='9', pet_photo='images/cat11.jpg'):
    """Негативный тест добавления нового питомца с некорректным ключом"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Добавляем некорректный ключ api и сохраняем в переменую auth_key
    auth_key = {'key': 'ksa344ldld'}
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert 'Forbidden' in result

def test_negativ_add_new_pet_with_non_valid_data(name='', animal_type='', age='', pet_photo='images/cat11.jpg'):
    """Негативный тест добавления нового питомца с пустыми данными и фото"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == ''

def test_add_new_pet_with_valid_data_no_foto(name='Матюся', animal_type='британец', age='9'):
    """Позитивный тест добавления нового питомца с корректными данными без фото"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_add_new_pet_no_photo(auth_key, name, animal_type, age)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_foto_pet_with_valid_data(pet_photo='images/cat11.jpg'):
    """Позитивный тест добавления нового питомца с корректными данными"""
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, 'Матюся', 'Британец', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берём id первого питомца из списка и отправляем запрос на добавление фото
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.post_add_photo_pet(auth_key, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['id'] == pet_id



# Блок тестов на проверку удаления питомцев

def test_successful_delete_self_pet():
    """Позитивный тест успешного удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Матюся", "Британец", "9", "images/cat11.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_negative_delete_pet_non_correct_key():
    """Негативный тест удаления питомца с некорректным ключом"""
    # Вначале получаем рабочий ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet(auth_key, "Матюся", "Британец", "9", "images/cat11.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    # Берем некорректный ключ auth_key1 и делаем запрос на удаление
    auth_key_false = {'key': 'ksa344ldld'}
    status, result = pf.delete_pet(auth_key_false, pet_id)
    # Проверяем что статус ответа равен 403 и в результате есть Forbidden
    assert status == 403
    assert 'Forbidden' in result

def test_negative_delete_pet_non_correct_id():
    """Негативный тест удаления питомца с некорректным ID"""
    # Получаем рабочий ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Берём некорректный id
    pet_id = ''
    status, result = pf.delete_pet(auth_key, pet_id)
    # Проверяем что статус ответа равен 404 и в результате есть Not Found
    assert status == 404
    assert 'Not Found' in result

# Блок тестов на проверку обновления данных питомцев

def test_successful_update_self_pet_info(name='Матюсище', animal_type='двортерьер', age=6):
    """Позитивный тест успешного обновления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        # добавляем нового питомца и опять запрашиваем список своих питомцев
        pf.post_add_new_pet(auth_key, "Матюся", "Британец", "9", "images/cat11.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, result = pf.put_update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name

def test_negativ_update_pet_info_non_correct_key(name='Матюсище', animal_type='двортерьер', age=6):
    """Негативный тест обновления информации о питомце с некорректным ключом"""
    # Получаем корректный ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст с некорректным ключом
    auth_key_false = {'key': 'ksa344ldld'}
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet_info(auth_key_false, my_pets['pets'][0]['id'], name, animal_type, age)
    else:
        # добавляем нового питомца и опять запрашиваем список своих питомцев
        pf.post_add_new_pet(auth_key, "Матюся", "Британец", "9", "images/cat11.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        # Пробуем обновить имя, тип и возраст с некорректным ключом
        status, result = pf.put_update_pet_info(auth_key_false, my_pets['pets'][0]['id'], name, animal_type, age)
    # Проверяем что статус ответа = 403 и в результате есть Forbidden
    assert status == 403
    assert 'Forbidden' in result

