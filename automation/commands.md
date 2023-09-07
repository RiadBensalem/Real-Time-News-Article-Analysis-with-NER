# Eland
```
curl -LfO ''
```

```
cd eland-main
docker build -t elastic/eland .
```

```
docker run -it --rm elastic/eland eland_import_hub_model --url https://username:password@url:port --hub-model-id elastic/distilbert-base-uncased-finetuned-conll03-english --task-type ner --start
```

```
empty
```


# Redpanda


```
docker run -d --network=host redpandadata/redpanda
```

```
docker run --network=host -p 8080:8080 -e KAFKA_BROKERS=localhost:9092 redpandadata/console
```

```
alias rpk='docker exec -it REPANDA_CONTAINER rpk'
```
