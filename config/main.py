import tarfile
import os
import json
import datetime
import random
import keyboard

USERNAME = "Danil"
NAME_COMP = "Asus"
PATH = "D:\\DAN\\proga\\config\\root.tar"

temp_path = "D:\\DAN\\proga\\config\\temp.tar" # путь для создания временного архива без удаленного файла
current_path = "root/"
    
def path(par_path):
    if par_path[:5] == "root/":
        return par_path if par_path[-1] == '/' or '.' in par_path.split('/')[-1] else par_path + '/' #Вовзращаем со слэшом в конце или без слэша, если в конце файл (его определем при наличии расширения, то есть должна быть точка)
    elif par_path[:2] == "..":
        if len(par_path) > 3: # Помимо двух точек учитывается слэш
            if par_path[2] == '/':
                if current_path != "root/": #Проверка чтобы не выходить из корневой папки
                    parent_dir = "/".join(current_path.rstrip('/').split('/')[:-1]) + '/' #Берем путь родительской директории
                    return parent_dir + par_path[3:] if par_path[-1] == '/' or '.' in par_path.split('/')[-1] else parent_dir + par_path[3:] + '/' #Присоединяем путь родительской директории и параметр 
                # и возвращаем со слэшом в конце
                else:
                    return "Вы в корневой папке"
            else:
                return "Неправильно введен путь"
        else:
            if current_path != "root/": #Проверка чтобы не выходить из корневой папки
                #Если параметр равен ".." или "../"
                return "/".join(current_path.rstrip('/').split('/')[:-1]) + '/' 
                #Применяем rstrip чтобы удалить конечный слэш и после разбиения в конце не было пустого символа 
            else:
                return "Вы в корневой папке"
    elif par_path[0] == '.':
        if len(par_path) > 2: #Помимо точки еще учитывается слэш
            if par_path[1] == '/':
                return current_path + par_path[2:] if par_path[-1] == '/' or '.' in par_path.split('/')[-1] else current_path + par_path[2:] + '/' #Возвращаем со слэшом в конце
            else:
                return "Неправильно введен путь"
        else:
            #Если параметр равен "." или "./"
            return current_path
    elif par_path[0] == '~':
        if len(par_path) > 2: #Помимо тильды еще учитывается слэш
            if par_path[1] == '/':
                return "root/" + par_path[2:] if par_path[-1] == '/' or '.' in par_path.split('/')[-1] else "root/" + par_path[2:] + '/' #Возвращаем со слэшом в конце
            else:
                return "Неправильно введен путь"
        else:
            #Если параметр равен "." или "~/"
            return "root/"
    else:
        return current_path + par_path if par_path[-1] == '/' or '.' in par_path.split('/')[-1] else current_path + par_path + '/'
    
    
def ls(flag=0, in_path='.'):
    cur_path = path(in_path)
    if cur_path != "Неправильно введен путь" and cur_path != "Вы в корневой папке":
        try:
            result = ""
            with tarfile.open(PATH, 'r') as tar:
                isDir = False
                for file in tar.getmembers():
                    if file.name.startswith(cur_path):
                        isDir = True
                        cur_file = file.name[len(cur_path):]
                        if '/' not in cur_file:
                            if flag == 1:
                                file_metadata = file_mode_users()
                                file_name_update = file.name + ('/' if file.isdir() and file.name[-1] != '/' else '') # Если директория, то со слэшом, если файл, то без
                                mode_own = mode(file_metadata[file_name_update]["permission"][0])
                                mode_group = mode(file_metadata[file_name_update]["permission"][1])
                                mode_other = mode(file_metadata[file_name_update]["permission"][2])
                                result += ("d" if file.isdir() else '-') + mode_own + mode_group + mode_other + " " + file_metadata[file_name_update]["owner"] + " " + file_metadata[file_name_update]["group"] + " " + cur_file + "\n"
                            else:
                                result += f"{cur_file}/\n" if file.isdir() else f"{cur_file}\n"
                if not isDir:
                    return "Нету такой директории"
            return result.strip()
        except FileNotFoundError:
            return "По указанному пути ничего нету"
    else:
        return "Неправильно введен путь" if cur_path == "Неправильно введен путь" else "Вы в корневой папке" 

def cd(in_path='root/'):
    global current_path
    cd_path = path(in_path)
    if cd_path != "Неправильно введен путь" and cd_path != "Вы в корневой папке":
        try:
            with tarfile.open(PATH, 'r') as tar:
                Flag = False
                for file in tar.getmembers():
                    if file.name.startswith(cd_path):
                        Flag = True
                if not Flag:
                    return "Нету такой директории"
                else:
                    current_path = cd_path
                    return f"Перешли в директорию {current_path}"
        except FileNotFoundError:
            return "По указанному пути ничего нету"
    return "Неправильно введен путь" if cd_path == "Неправильно введен путь" else "Вы в корневой папке" 

def pwd():
    return current_path

def rm(path_for_rm):
    rm_file = path(path_for_rm)
    
    file_exists = False
    is_directory = False
    
    if rm_file != "Неправильно введен путь" and rm_file != "Вы в корневой папке" and  rm_file != "root/":
        try:
            with tarfile.open(PATH, 'r') as source_tar:
                for member in source_tar.getmembers():
                    if member.name == rm_file:
                        file_exists = True
                        is_directory = member.isdir()
                        break

            if not file_exists:
                return f"Файл {rm_file} не существует"
            if is_directory:
                return f"{rm_file} является директорией, используйте другой метод для удаления директорий"
        
            with tarfile.open(PATH, 'r') as source_tar:
                with tarfile.open(temp_path, 'w') as temp:
                    for member in source_tar.getmembers():
                        if member.name != rm_file:
                            temp.addfile(member, source_tar.extractfile(member)) 
            os.remove(PATH)
            os.rename(temp_path, PATH)
            return f"Файл {rm_file} удален"
        except FileNotFoundError:
            return "Файл не найден"
    else:
        if rm_file == "Неправильно введен путь":
            return "Неправильно введен путь"
        elif rm_file == "root/":
            return "Не удаляйте корневую папку"
        else:
            return "Вы в корневой папке"
    
def chmod(par_mode, par_path_file):
    if len(par_mode) != 3:
        return "Неправильный формат прав доступа"
    
    file_metadata = file_mode_users()
    path_file = path(par_path_file)
    if path_file in file_metadata:
        file_metadata[path_file]["permission"] = par_mode
        with open('mode.json', 'w') as file_dict:
            json.dump(file_metadata, file_dict)
        return f"Права доступа к {path_file} изменены на {par_mode}"
    return "Неправильный путь"

def file_mode_users():
    with open('mode.json', 'r') as cur_file:
        return json.load(cur_file)

def mode(par_digit):
    mode_dict = {
        '0': '-', '1': '--x', '2': '-w-', '3': '-wx',
        '4': 'r--', '5': 'r-x', '6': 'rw-', '7': 'rwx'
    }
    return mode_dict[par_digit]

def app(command):
    parts_command = command.split()
    if parts_command[0] == "ls":
        if len(parts_command) > 1:
            if parts_command[1] == "-l":
                if len(parts_command) > 2:
                    # Перебираем несколько путей
                    results = []
                    for path_arg in parts_command[2:]:
                        results.append(ls(1, path_arg))
                    return "\n......\n".join(results)
                else:
                    return ls(1)
            else:
                # Перебираем несколько путей
                results = []
                for path_arg in parts_command[1:]:
                    results.append(ls(0, path_arg))
                return "\n.....\n".join(results)
        else:
            return ls()
    elif parts_command[0] == "cd":
        return cd(parts_command[1]) if len(parts_command) == 2 else cd()
    elif parts_command[0] == "pwd":
        return pwd()
    elif parts_command[0] == "rm":
        return rm(parts_command[1]) if len(parts_command) > 1 else "Не указан путь для удаления"
    elif parts_command[0] == "chmod":
        return chmod(parts_command[1], parts_command[2]) if len(parts_command) == 3 else "Неправильная команда chmod"
    else:
        return "Команда не найдена"

def start_script():
    with open("start_script.txt", 'r') as script:
        for command in script.readlines():
            command = command.strip()
            if command:
                result = app(command)
                print(result)
        
def main_loop():
    start_script()
    while True:
        command = input(USERNAME + "@" + NAME_COMP + ":" + current_path + "$ ")
        command = command.strip()
        if command == "exit":
            exit()
        elif command == "":
            continue
        result = app(command)
        print(result)
        
if __name__ == "__main__":
    '''with tarfile.open(PATH, 'r') as tar: # Создадим файл, где будут храниться сведения о доступах к файлам и директориям
        file_metadata = {}
        for file in tar.getmembers():
            owner = random.choice(["Kolya", "Vasya", "Petya", "users2"])
            group = random.choice(["users", "admins"])
            file_metadata[file.name + ('/' if file.isdir() and file.name[-1] != '/' else '')] = {
                "owner": owner,
                "group": group,
                "permission": "666"
            }
        with open('mode.json', 'w') as file:
            json.dump(file_metadata, file)'''
    keyboard.block_key('ctrl')
    main_loop()
    
