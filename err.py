person = {
    'salary': 1000,
    'name': 'Oleg',
}

# print(person.get('name')) => value, если ключ есть
# => None, если его нет

person_name = person.get('name')
if person_name:
    print(person_name)
else:
    print('error')

# try:
#     print(person['nam'])
# except KeyError:
#     print('try again')
# except AnotherError1:
#     pass
# except AnotherError2:
#     pass
# # except:
# #     pass
    
# ...

# def foo():
#     try:
#         print(person['nam'])
#     except KeyError:
#         print('try again')
        
# foo()


# class CustomError(Exception):
#     pass

# class CustomError2(Exception):
#     pass


# def foo():
#     # print(person['nam'])
#     try:
#         print(person['nam']) # летит красный
#     except CustomError: # ловит только зеленые
#         print('try again')
#     except CustomError2: # ловит только синие
#         print('try again 2')
#     # try:
#     #     print(person['nam'])
#     # except KeyError: #! Вратарь, который никогда не пропускает красные мячи
#     #     print('try again')

# def foo2():
#     try:
#         foo()
#     except CustomError3:
#         pass

# try:
#     foo2()
# except KeyError:
#     print('ERROR')
    
#! Программа аварийно завершает свою работу (с ненулевым кодом), 
#! если ни один обработчик любых уровней не поймал исключение
