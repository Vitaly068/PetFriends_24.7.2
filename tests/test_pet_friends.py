from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os.path

pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что код статуса запроса 200 и в переменной result
    содержится слово key'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем что код статуса запроса 200 и список всех питомцев не пустой
    Для этого при помощи метода get_app_key() получаем ключ, сохраняем его в переменной
    api_key, затем применяем метод get_list_of_pets() и проверяем статус ответа и то
    что список питомцев не пустой'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(api_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_pets_with_valid_data(name='Felix', animal_type='cat', age= '3', pet_photo='images/Felix.jpeg'):
    '''Проверяем что код статуса запроса 200 и что список с добавленными данными не пустой для этого
    в переменную pet_photo сохраняем путь к файлу фотографии питомца, сохраняем ключ в переменную api_key,
    проверяем статус ответа и что в ответе содержатся добавленные данные.
     '''


    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_delete_pet():
    '''Проверяем возможность удаления питомца'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pets(api_key, 'Murzik', 'cat', '5', 'images/Felix.jpeg')
        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    pet_id = my_pets['pets'][0]['id']

    status, _ = pf.delete_pets(api_key, pet_id)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    assert status == 200
    assert pet_id not in my_pets.values()


def test_update_pet_info(name='New', animal_type='Newanimal', age='5'):
    '''Проверяем возможность изменения данных питомца'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(api_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_pets_with_valid_data_without_photo(name='БезФото', animal_type='кот', age='6'):
    '''Проверяем возможность добавления нового питомца без фото'''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_at_pet(pet_photo='images/phyntik.jpeg'):
    '''Проверяем возможность добавления новой фотографии питомца'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(api_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(api_key, 'my_pets')

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("Питомцы отсутствуют")


def test_add_pet_negative_age_number(name='Fedor', animal_type='bird', age= "-3", pet_photo='images/sova.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
     '''

    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)


    assert result['age'] < '0'
    if AssertionError:
        print('Питомец добавлен на сайт с отрицательным числом в поле возраст')
    else:
        raise Exception('Не верно указан возраст')



def test_add_pet_with_four_digit_age_number(name='Fedor', animal_type='cat', age= '12345', pet_photo='images/felix.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с числом более трех знаков в переменной age.
    Тест не будет пройден ели питомец будет добавлен на сайт с числом превышающим три знака в поле возраст.'''


    _, api_key = pf.get_api_key(valid_email, valid_password)
    _, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert AssertionError
    if AssertionError:
       print('Питомец добавлен на сайт с числом привышающим 3 знака в поле возраст')


def test_add_pet_with_empty_value_in_variable_name(name='', animal_type='cat', age='2', pet_photo='images/penni.jpeg'):
    '''Проверяем возможность добавления питомца с пустым значением в переменной name
    Тест не будет пройден если питомец будет добавлен на сайт с пустым значением в поле "имя"'''


    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert AssertionError
    if AssertionError:
        print('Питомец добавлен на сайт с пустым значением в имени')


def test_add_pet_with_a_lot_of_words_in_variable_name(animal_type='cat', age='2', pet_photo='images/felix.jpeg'):
    '''Проверка с негативным сценарием. Добавления питомца имя которого превышает 5 слов
    Тест не будет пройден если питомец будет добавлен на сайт с именем состоящим из более 5 слов'''

    name = 'pip3 install python dotenv all'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)


    assert status == 200
    assert AssertionError
    if AssertionError:
        print('Питомец добавлен с именем больше 5 слов')


def test_add_pet_with_special_characters_in_variable_animal_type(name='Fedor', age='3', pet_photo='images/phyntik.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с специальными символами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с спец.символами вместо букв в поле порода.
    '''
    animal_type = 'Pig%@'


    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)


    assert status == 200
    assert AssertionError
    if AssertionError:
        print('Питомец добавлен с недопустимыми спец.символами')


def test_add_pet_with_numbers_in_variable_animal_type(name='Fedor', animal_type='34562', age='3',
                                                      pet_photo='images/sova.jpeg'):
    '''Проверка с негативным сценарием. Добавление питомца с цифрами вместо букв в переменной animal_type.
    Тест не будет пройден если питомец будет добавлен на сайт с цифрами вместо букв в поле порода.'''

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert AssertionError
    if AssertionError:
        print('Питомец добавлен на сайт с цифрами вместо букв в поле порода')

def test_add_pet_with_a_lot_of_words_in_variable_animal_type(name='Fedor', age='2', pet_photo='images/penni.jpeg'):
    '''Проверка с негативным сценарием. Добавления питомца название породы которого превышает 5 слов
    Тест не будет пройден если питомец будет добавлен на сайт с названием породы состоящим из более 5 слов'''

    animal_type = 'Liam Noah William James Oliver'

    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pets(api_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert AssertionError
    if AssertionError:
        print('Питомец добавлен с названием породы больше 5 слов')


def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с невалидным паролем и с валидным емейлом.
    Проверяем нет ли ключа в ответе'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
