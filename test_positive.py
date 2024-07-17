import os
import subprocess
from utils import checkout

current_dir = os.path.dirname(os.path.abspath(__file__))  # Текущая директория скрипта
folder_in = "/home/user/tst"  # Папка с файлами для архивации
folder_out = "/home/user/out"  # Папка для сохранения архива
folder_ext = "/home/user/folder1"  # Папка для распаковки файлов
path_to_file = "/home/user/out/arx2.7z"  # Полный путь к файлу архива
file_to_delete = "test1"  # Файл для удаления из архива
file_to_add = "test2"  # Файл для добавления в архив

def test_step1():   # Тест 1 - создание архива и проверка его существования
    assert checkout(f"cd {folder_in}; 7z a {path_to_file}", "Everything is Ok"), "test1 FAIL"
    assert os.path.exists(path_to_file), "Файл архива не был создан"

def test_step2(): # Тест 2 - распаковка архива и проверка существования распакованных файлов
    assert checkout(f"cd {folder_out}; 7z e {path_to_file} -o{folder_ext} -y", "Everything is Ok"), "test2 FAIL"
    extracted_files = os.listdir(folder_ext)
    assert len(extracted_files) > 0, "Файлы не были распакованы"

def test_step3():   # Тест 3 - проверка архива
    assert checkout(f"cd {folder_out}; 7z t {path_to_file}", "Everything is Ok"), "test3 FAIL"

def test_step4():   # Тест 4 - удаление файла из архива и проверка выполнения команды
    assert checkout(f"cd {folder_out}; 7z d {path_to_file} {file_to_delete}", "Everything is Ok"), "test4 FAIL"

def test_step5():   # Тест 5 - обновление архива и проверка выполнения команды
    assert checkout(f"cd {folder_in}; 7z u {path_to_file} {file_to_add}", "Everything is Ok"), "test5 FAIL"

def test_step6():   # Тест 6 - вывод списка файлов в архиве
    assert checkout(f"cd {folder_out}; 7z l {path_to_file}", "Name"), "test6 FAIL"

def test_step7():   # Тест 7 - распаковка с сохранением путей
    assert checkout(f"cd {folder_out}; 7z x {path_to_file} -o{folder_ext} -y", "Everything is Ok"), "test7 FAIL"
    extracted_files = os.listdir(folder_ext)
    assert len(extracted_files) > 0, "Файлы не были распакованы"

def test_step8():   # Тест 8 - сравнение CRC32 файлов в архиве с использованием Perl-скрипта и 7z
    perl_script_path = os.path.join(current_dir, "calc_crc32_files.pl")

    # Вызов Perl-скрипта для расчета CRC32 для файлов в архиве
    result = subprocess.run(["perl", perl_script_path, path_to_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    assert result.returncode == 0, f"Ошибка выполнения скрипта Perl: {result.stderr}"
    perl_crc32_lines = result.stdout.strip().splitlines()

    # Вызов 7z для получения CRC32 файлов в архиве
    result = subprocess.run(f"cd {folder_out}; 7z l {path_to_file}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    assert result.returncode == 0, "Ошибка при выполнении команды 7z для списка файлов"
    lines = result.stdout.splitlines()
    crc32_lines = [line for line in lines if line.startswith("CRC32")]
    assert len(crc32_lines) == len(perl_crc32_lines), "Количество CRC32 в Perl и 7z не совпадает"

    # Сравнение CRC32, вычисленных 7z и pers
    for perl_crc32, line in zip(perl_crc32_lines, crc32_lines):
        calculated_crc32_7z = line.split()[-1]
        assert perl_crc32 == calculated_crc32_7z, f"Хеши не совпадают: Perl({perl_crc32}) != 7z({calculated_crc32_7z})"

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", __file__])
