StartTradeProducerContainer:
	docker start tradeproducer

StopTradeProducerContainer:
	docker stop tradeproducer

RmTradeProducerContainer: StopTradeProducerContainer
	docker rm tradeproducer

RmTradeProducerImage: StopTradeProducerContainer RmTradeProducerContainer
	docker rmi tradeproducer

RmLiteProducerImage: 
	docker rmi litetradeproducer

ComposeRedPanda:
	docker compose -f ./MicroServices/RedPanda.yml up -d

ShutDownRedPanda:
	docker compose -f ./MicroServices/RedPanda.yml down

BuildTradeProducerContainer:
	docker build -t tradeproducer ./MicroServices/TradeProducer -f ./MicroServices/TradeProducer/TradeProducer.Dockerfile

RebuildTradeProducerContainer: RmTradeProducerImage RunTradeProducerContainer
	@echo "Rebuilt Image and ReRun Trade Producer Container"

BuildLiteTradeProducerContainer:
	DOCKER_BUILDKIT=1 docker build --target=Runtime -t litetradeproducer ./MicroServices/TradeProducer -f ./MicroServices/TradeProducer/LiteProducer.Dockerfile

RunTradeProducerContainer: ComposeRedPanda BuildTradeProducerContainer
	docker run --network redpanda-network --name tradeproducer -d -it tradeproducer

LintCode:
	cd ./MicroServices/TradeProducer && poetry run ruff check --fix
	pwd
	cd ./MicroServices/OHLCTradeAggregator && poetry run ruff check --fix

FormatCode:
	cd ./MicroServices/TradeProducer && poetry run ruff format
	cd ./MicroServices/OHLCTradeAggregator && poetry run ruff format

TerminalIntoTradeProducer:
	docker exec -it tradeproducer /bin/bash

StartUp: ComposeRedPanda RunTradeProducerContainer
	@echo "Containers Fired Up, here are the Logs"
	docker ps -a
	docker logs tradeproducer

ShutDown: RmTradeProducerImage ShutDownRedPanda	
	@echo "Everything Shut Down"
	docker images
	docker ps -a 