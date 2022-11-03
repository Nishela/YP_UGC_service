## Запуск кластера mongo: 
### Запуск:
- сборка компоуза
```shell
docker-compose -f docker-compose-mongo.yml up --build -d
```
 - предоставление прав shell скрипту и запуск конфигураций кластера mongo
```shell
chmod +x ./mongo_setup.sh 
chmod +x ./mongo_setup.sh
```
- кластер готов к работе

---