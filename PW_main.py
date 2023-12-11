import requests
import re
import os

# + Взять словарь всех 5 буквенных слов
# Указать исключающие буквы
# Указать присутствующие буквы
# Выдать возможные варианты на каждом этапе 




def update_dict():   
    resp = requests.get ('https://bezbukv.ru/mask/*****?page=1').text
    all_page = re.findall(r'page=\d*', resp)
    last_page = str(all_page[-2]).strip('page=')

    with open ('lib.txt', "w") as lib:
        for page in range(1, int(last_page)+1):

            link = 'https://bezbukv.ru/mask/*****?page=' + str(page) 
            resp = requests.get (link).text

            f = str(re.findall(r'\.\n\t\w{5}', resp))
            x = re.findall(r'\w{6}', f)   

            for word in x:        
                lib.writelines (word.lstrip('t') + '\n')


def search_word(negative_let, positive_let):

    #Словарь для слов в которых есть буквы "positive_let"
    positive_list = []
    #Словарь для слов в которых есть буквы "negative_let"
    negative_list = []

    #Заполняем словари букв
    negative_let_list = set(let for let in negative_let)
    positive_let_list = set(let for let in positive_let)

    
    i = 0

    if os.getcwd().split('\\')[-1] == 'Tinkoff_word_game':
        path = '.\\lib.txt'
    else:
        path = '.\\Tinkoff_word_game\\lib.txt'

    with open (path, "r") as dictt:
        for word in dictt.readlines():
            negative_list.append(word.strip('\n'))

    for word in negative_list:
        i=negative_list.index(word)
        for let in negative_let_list:
            if let in word:
                negative_list.insert(i, '0')
                negative_list.remove(word)
                break
  
    while '0' in negative_list != False:
        negative_list.remove('0')
        

    for word in negative_list:
        for let in positive_let_list:
            if let in word:
                positive_list.append (word)

    positive_list = list(dict.fromkeys(positive_list))

    # Поиск только тех слов, в которых есть все буквы

    dict_res = {}
    check_let = []

    for word in positive_list:
        for let in positive_let_list:
            if let in word:
                check_let.append(let)
        dict_res.update({word: len(check_let)})
        check_let = []

    # Возвращает список слов в которых есть все известные буквы
    final = [key for key,value in dict_res.items() if value == len(positive_let_list)]

    if len(final) > 0:
        return final
    else:
        final = 'не существуют'
        return final


def check_position(maska, word_list):
    mask = [m for m in maska]

    check = []

    for word in word_list:
        for i,symb in enumerate(mask):
            if symb == '*':
                continue
            elif symb == word[i]:
                check.append(word)
            else:
                try:
                    check.remove(word)
                    break
                except ValueError:
                    break
    
    if len(check) > 0:
        print ('Варианты:', set(check))
    else:
        print ('Вариантов нет')

def main_menu():
    print ('Режимы:\n0 - Обновить\n1 - Проверка слов без маски\n2 - Проверка с маской, вида: "*****". На месте * известные буквы\nexit - чтобы выйти')
    flag = True
    while flag:
        user_chooise = input()
        if user_chooise == '0':
            update_dict()
            print ('Обновление словаря закончено. Можно выбрать другой режим')
        elif user_chooise == 'exit':
            flag = False
            break
        elif user_chooise == '1':
            negative_let = input ('Буквы которых нет: ')
            positive_let = input ('Буквы которые есть: ')
            print ('Варианты:', search_word(negative_let, positive_let))
            flag = False
            break
        elif user_chooise == '2':
            negative_let = input ('Буквы которых нет: ')
            positive_let = input ('Буквы которые есть: ')
            final = search_word(negative_let, positive_let)
            mask = input('Ввидите маску: ')
            check_position(mask, final)
            flag = False
            break

if __name__ == "__main__":

    main_menu() 
