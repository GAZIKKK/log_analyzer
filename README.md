# log_analyzer

CLI-приложение для анализа логов Django-приложения и формирования отчётов. Отчёт выводится в консоль.

## Использование

Запуск приложения: 
bash
python main.py "C:\Users\Владелец\Desktop\logs\app1.log" "C:\Users\Владелец\Desktop\logs\app2.log" "C:\Users\Владелец\Desktop\logs\app3.log" --report handlers

- Укажите пути к лог-файлам как аргументы.
- Флаг `--report handlers` определяет тип отчёта (в данном случае — по обработчикам).
