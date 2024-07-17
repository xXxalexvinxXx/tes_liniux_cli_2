from utils import checkout

folder_in = "/home/user/tst"  # Папка с файлами для архивации
folder_out = "/home/user/out"  # Папка для сохранения архива
folder_ext = "/home/user/folder1"  # Папка для распаковки файлов
broken_archive = "corrupted.7z"  # Имя поврежденного архива

def test_step1_negative():
    # Негативный тест для распаковки поврежденного архива
    assert not checkout(f"cd {folder_out}; 7z e {broken_archive} -o{folder_ext} -y", "Everything is Ok"), "test_step1_negative FAIL"

def test_step2_negative():
    # Негативный тест для проверки поврежденного архива
    assert not checkout(f"cd {folder_out}; 7z t {broken_archive}", "Everything is Ok"), "test_step2_negative FAIL"

if __name__ == "__main__":
    import pytest
    pytest.main(["-v", __file__])
