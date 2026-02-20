FROM python:3.14.2-slim

# Настройка окружения: не писать .pyc, не буферизовать логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Объединяем системные зависимости и чистим кэш в одном слое
RUN apt-get update && apt-get install -y --no-install-recommends \
    mc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создаем директории и пользователя (безопасность)
RUN mkdir -p /usr/www/logs && \
    useradd -m -d /usr/www ular && \
    chown -R ular:ular /usr/www

WORKDIR /usr/www/

# Сначала ставим зависимости (используем кэш, пока requirements.txt не изменится)
COPY --chown=ular:ular req.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r req.txt

# Копируем приложение
COPY --chown=ular:ular src ./src

WORKDIR /usr/www/

# Переключаемся на пользователя
USER ular

# Запуск через Daphne
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]