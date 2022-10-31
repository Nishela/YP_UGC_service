#!/bin/bash
echo "1. Настройка серверов конфигурации"
docker exec -it mongo-config-01 bash -c 'echo "rs.initiate({_id: \"rs-config-server\", configsvr: true, version: 1, members:[{_id:0, host: \"mongo-config-01:27017\"}, {_id: 1, host:\"mongo-config-02:27017\" }, {_id: 2, host:\"mongo-config-03:27017\"}]})" | mongosh'
echo "\n"

echo "2. Сборка набора реплик первого шарда"
docker exec -it shard-01-node-a bash -c 'echo "rs.initiate({_id: \"rs-shard-01\", version: 1, members: [{_id: 0, host : \"shard01-a:27017\" }, { _id: 1, host : \"shard01-b:27017\" }, { _id: 2, host : \"shard01-c:27017\" },]})" | mongosh'
sleep 5
echo "\n"

echo "3. Сборка набора реплик второго шарда"
docker exec -it shard-02-node-a bash -c 'echo "rs.initiate({ _id: \"rs-shard-02\", version: 1,members: [{ _id: 0, host : \"shard02-a:27017\" },{ _id: 1, host : \"shard02-b:27017\" }, { _id: 2, host : \"shard02-c:27017\" },]})" | mongosh'
sleep 5
echo "\n"

echo "4. Добавление первого шарда в маршрутизатор"
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-01/shard01-a:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-01/shard01-b:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-01/shard01-c:27017\")" | mongosh'
sleep 5
echo "\n"

echo "5. Добавление второго шарда в маршрутизатор"
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-02/shard02-a:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-02/shard02-b:27017\")" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.addShard(\"rs-shard-02/shard02-c:27017\")" | mongosh'
sleep 3
echo "\n"

echo "n6. Создание базы данных"
docker exec -it shard-01-node-a bash -c 'echo "use movies" | mongosh'
sleep 3
echo "\n"

echo "7. Включение шардирования базы данных"
docker exec -it router-01 bash -c 'echo "sh.enableSharding(\"movies\")" | mongosh'
sleep 3
echo "\n"

echo "8. Создание коллекций"
docker exec -it router-01 bash -c 'echo "db.createCollection(\"movies.votes\")" | mongosh'
docker exec -it router-01 bash -c 'echo "db.createCollection(\"movies.reviews\")" | mongosh'
docker exec -it router-01 bash -c 'echo "db.createCollection(\"movies.bookmarks\")" | mongosh'
sleep 3
echo "\n"

echo "9. Настройка шардирования по полю"
docker exec -it router-01 bash -c 'echo "sh.shardCollection(\"movies.votes\", {\"movie_id\": \"hashed\"})" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.shardCollection(\"movies.reviews\", {\"movie_id\": \"hashed\"})" | mongosh'
docker exec -it router-01 bash -c 'echo "sh.shardCollection(\"movies.bookmarks\", {\"user_id\": \"hashed\"})" | mongosh'
