#!/bin/bash

# 🐸 Автоматический деплой Python-ботов с Docker + Compose
# Запускать на чистом сервере после клонирования репозитория

set -e  # Остановить выполнение при ошибке

echo "✅ Начинаем развёртывание ботов..."

# 1. Обновляем систему
echo "🔧 Обновляем систему..."
sudo apt update && sudo apt upgrade -y

# 2. Устанавливаем Docker и Docker Compose v2
echo "📥 Устанавливаем Docker и Docker Compose..."

if ! command -v docker &> /dev/null; then
    echo "🐳 Устанавливаем Docker..."
    sudo apt install -y ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo "🐳 Docker уже установлен"
fi

# Проверка Docker Compose v2
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose не найден. Убедитесь, что установлена версия >= 2.0."
    exit 1
fi

# 3. Добавляем пользователя в группу docker
if ! groups | grep -q '\bdocker\b'; then
    echo "👥 Добавляем пользователя $USER в группу docker..."
    sudo usermod -aG docker "$USER"
    echo "⚠️  Для применения изменений требуется новая сессия."
    echo "💡 Вы можете выполнить: 'newgrp docker' и перезапустить скрипт,"
    echo "   или перезайти в систему. Сейчас продолжим через sudo при необходимости."
fi

# 4. Переходим в корень проекта

# 5. Проверяем наличие docker-compose.yml
COMPOSE_FILE="docker-compose.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Не найден файл конфигурации: $COMPOSE_FILE"
    echo "Проверьте, что вы находитесь в корне проекта:"
    pwd
    ls -la
    exit 1
fi

echo "📦 Используем файл конфигурации: $COMPOSE_FILE"

# 6. Создаём .env, если нет
ENV_FILE="./.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  Файл $ENV_FILE не найден. Создаём шаблон..."
    cat > "$ENV_FILE" <<EOF
# 🐸 Пример переменных окружения
BOT_TOKEN=your_token_here
# Добавьте другие параметры по необходимости
EOF
    echo "✅ Шаблон создан. Отредактируйте $ENV_FILE и вставьте реальные токены!"
fi

# 7. Собираем и запускаем контейнеры
echo "🚀 Собираем и запускаем ботов через Docker Compose..."
if groups | grep -q '\bdocker\b'; then
    docker compose -f "$COMPOSE_FILE" up -d --build
else
    echo "🔁 Запуск через sudo (пока не обновлена сессия)..."
    sudo docker compose -f "$COMPOSE_FILE" up -d --build
fi

# 8. Проверяем статус
echo "📊 Статус контейнеров:"
if groups | grep -q '\bdocker\b'; then
    docker compose -f "$COMPOSE_FILE" ps
else
    sudo docker compose -f "$COMPOSE_FILE" ps
fi

echo "✅ Развёртывание завершено! Боты работают в фоне."
echo "💡 Команды для управления:"
echo "   docker compose logs -f bot1    — смотреть логи bot1"
echo "   docker compose restart bot2    — перезапустить bot2"
echo "   docker compose down            — остановить ВСЁ"
