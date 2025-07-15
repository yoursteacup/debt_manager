FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директории для базы данных
RUN mkdir -p /app/data

# Запуск бота
CMD ["python", "bot.py"]