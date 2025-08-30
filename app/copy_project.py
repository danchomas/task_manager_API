#!/usr/bin/env python3
import os
from pathlib import Path

def collect_project_files(project_root, ignore_patterns):
    """Собирает все файлы проекта, исключая указанные паттерны."""
    project_files = []

    for root, dirs, files in os.walk(project_root):
        # Удаляем игнорируемые директории
        dirs[:] = [d for d in dirs if not should_ignore_dir(d, ignore_patterns)]

        for file in files:
            if not should_ignore_file(file, ignore_patterns):
                file_path = Path(root) / file
                relative_path = file_path.relative_to(project_root)
                project_files.append(relative_path)

    return sorted(project_files)

def should_ignore_dir(dir_name, ignore_patterns):
    """Проверяет, нужно ли игнорировать директорию."""
    ignore_dirs = [
        '__pycache__', '.git', '.idea', '.vscode', 'venv', 'env', '.venv',
        'build', 'dist', '.eggs', '*.egg-info'
    ]
    return dir_name in ignore_dirs

def should_ignore_file(file_name, ignore_patterns):
    """Проверяет, нужно ли игнорировать файл."""
    ignore_files = [
        '*.pyc', '*.pyo', '*.pyd', '.DS_Store', '*.log', '.gitignore',
        '.env', '*.tmp', '*.swp', '*.swo', 'Thumbs.db', '*.so', '*.dll'
    ]

    for pattern in ignore_files:
        if pattern.startswith('*.'):
            if file_name.endswith(pattern[1:]):
                return True
        else:
            if file_name == pattern:
                return True
    return False

def read_file_content(file_path):
    """Читает содержимое файла, если это текстовый файл."""
    try:
        # Пробуем открыть как текстовый файл
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except (UnicodeDecodeError, PermissionError):
        return "[Бинарный файл или файл недоступен для чтения]"

def main():
    # Путь к текущей директории (корень проекта)
    project_root = Path(__file__).parent.resolve()

    # Имя выходного файла
    output_file = project_root / "project_backup.txt"

    print("Собираю список файлов проекта...")

    # Собираем все файлы проекта
    ignore_patterns = []  # Можно расширить при необходимости
    project_files = collect_project_files(project_root, ignore_patterns)

    print(f"Найдено файлов: {len(project_files)}")
    print("Записываю данные в файл...")

    # Записываем всё в текстовый файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== РЕЗЕРВНАЯ КОПИЯ ПРОЕКТА ===\n")
        f.write(f"Путь к проекту: {project_root}\n")
        f.write(f"Дата создания: {os.path.getctime(__file__)}\n")
        f.write(f"Всего файлов: {len(project_files)}\n")
        f.write("=" * 50 + "\n\n")

        for file_path in project_files:
            full_path = project_root / file_path
            f.write(f"\n{'='*20} {file_path} {'='*20}\n")

            # Читаем содержимое файла
            content = read_file_content(full_path)
            f.write(content)
            f.write("\n")

    print(f"Резервная копия создана: {output_file}")

if __name__ == "__main__":
    main()
