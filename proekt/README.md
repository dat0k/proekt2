# Scrape Currency Project

## Описание
Этот проект собирает данные о курсах валют с помощью парсинга сайтов с использованием **Python**, **Crawlee** и **Playwright**.  
Проект демонстрирует работу с реальными данными и автоматизацию сбора информации.

## Требования
- Python 3.10+
- Браузеры для Playwright (устанавливаются через `python3 -m playwright install chromium`)

## Установка

1. Клонируем репозиторий:

git clone <URL_репозитория>
cd <название_папки>

2.Устанавливаем зависимости:

python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install -r requirements.txt
python3 -m playwright install chromium

3.Запускаем скрипт:
python3 scrape_currency.py
