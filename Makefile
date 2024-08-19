#------------------------#
# Linting and Formatting #
#------------------------#

LintCode:
	@cd ./MicroServices/FeaturePipeline/TradeProducer && poetry run ruff check --fix
	@cd ./MicroServices/FeaturePipeline/OHLCTradeAggregator && poetry run ruff check --fix

FormatCode:
	@cd ./MicroServices/FeaturePipeline/TradeProducer && poetry run ruff format
	@cd ./MicroServices/FeaturePipeline/OHLCTradeAggregator && poetry run ruff format

#------------------------------#
# Compose RedPanda Up and Down #
#------------------------------#

ComposeRedPanda:
	@docker compose -f ./MicroServices/RedPandaKafkaBroker/RedPanda.yml up -d

ShutDownRedPanda:
	@docker compose -f ./MicroServices/RedPandaKafkaBroker/RedPanda.yml down

#---------------------------------#
# MicroServices -  Trade Producer #
#---------------------------------#

BuildTradeProducerContainer:
	docker build -t tradeproducer ./MicroServices/FeaturePipeline/TradeProducer -f ./MicroServices/FeaturePipeline/TradeProducer/TradeProducer.Dockerfile

RunTradeProducerContainer: ComposeRedPanda BuildTradeProducerContainer
	docker run --network redpanda-network --name tradeproducer -d -it tradeproducer

StartTradeProducerContainer:
	docker start tradeproducer

StopTradeProducerContainer:
	docker stop tradeproducer

RmTradeProducerContainer: StopTradeProducerContainer
	docker rm tradeproducer

RmTradeProducerImage: StopTradeProducerContainer RmTradeProducerContainer
	docker rmi tradeproducer

RebuildTradeProducerContainer: RmTradeProducerImage RunTradeProducerContainer
	@echo "Rebuilt Image and ReRan Trade Producer Container"

BuildLiteTradeProducerContainer:
	DOCKER_BUILDKIT=1 docker build --target=Runtime -t litetradeproducer ./MicroServices/FeaturePipeline/TradeProducer -f ./MicroServices/FeaturePipeline/TradeProducer/LiteProducer.Dockerfile

RmLiteProducerImage: 
	docker rmi litetradeproducer

TerminalIntoTradeProducer:
	docker exec -it -u root tradeproducer /bin/bash

#-----------------------------------#
# MicroServices -  Trade Aggregator #
#-----------------------------------#

BuildTradeAggregatorContainer:
	docker build -t tradeaggregator ./MicroServices/FeaturePipeline/OHLCTradeAggregator -f ./MicroServices/FeaturePipeline/OHLCTradeAggregator/TradeAggregator.Dockerfile

RunTradeAggregatorContainer: ComposeRedPanda BuildTradeAggregatorContainer
	docker run --network redpanda-network --name tradeaggregator -d -it tradeaggregator

StartTradeAggregatorContainer:
	docker start tradeaggregator

StopTradeAggregatorContainer:
	docker stop tradeaggregator

RmTradeAggregatorContainer: StopTradeAggregatorContainer
	docker rm tradeaggregator

RmTradeAggregatorImage: StopTradeAggregatorContainer RmTradeAggregatorContainer
	docker rmi tradeaggregator

RebuildTradeAggregatorContainer: RmTradeAggregatorImage RunTradeAggregatorContainer
	@echo "Rebuilt Image and ReRan Trade Aggregator Container"

BuildLiteTradeAggregatorContainer:
	DOCKER_BUILDKIT=1 docker build --target=Runtime -t litetradeaggregator ./MicroServices/FeaturePipeline/OHLCTradeAggregator -f ./MicroServices/FeaturePipeline/OHLCTradeAggregator/LiteAggregator.Dockerfile

RmLiteAggregatorImage: 
	docker rmi litetradeaggregator
	
TerminalIntoTradeAggregator:
	docker exec -it -u root tradeaggregator /bin/bash

#------------------------#
# Bundles and Wrapped Up #
#------------------------#

StartUp: ComposeRedPanda RunTradeProducerContainer RunTradeAggregatorContainer
	@echo "Containers Fired Up, here are the Logs"
	docker ps -a
	docker logs tradeproducer
	docker logs tradeaggregator

ShutDown: RmTradeProducerImage RmTradeAggregatorImage ShutDownRedPanda	
	@echo "Everything Shat Down"
	docker images
	docker ps -a 

Restart: ShutDown StartUp