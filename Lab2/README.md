# Cкрипт для тестирования MTU в канале

- Скрипт принимает на вход desstination_ip в аргументе host
- Проверяется доступность icmp
- Проверяется доступность адреса назначения
- Обрабатываются исключения
- Скрипт может работать на раличных ОС 

# Сборка образа
```shell
docker build -t optimal-mtu .
```

# Запуск контейнера
```shell
docker run --rm optimal-mtu --host [destination_ip/host]
```