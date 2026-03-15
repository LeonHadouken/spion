#!/bin/bash
echo "Очистка кэша Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

echo "Очистка pytest кэша..."
rm -rf .pytest_cache/

echo "Очистка coverage..."
rm -rf .coverage htmlcov/

echo "Очистка mypy..."
rm -rf .mypy_cache/

echo "Очистка логов..."
rm -f *.log log.txt

echo "✅ Готово!"