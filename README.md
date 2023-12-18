# Сервис распознавания жестов

### Команды для запуска

Запуск через pip:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 4000
```

Запуск через Docker:
```bash
docker build -t app .
docker run -d -p 4000:4000 app
```
