#------------------------#
# Linting and Formatting #
#------------------------#

LintCode:
	@cd ./MicroServices/FeaturePipeline/TradeProducer && poetry run ruff check --fix
	@cd ./MicroServices/FeaturePipeline/OHLCTradeAggregator && poetry run ruff check --fix
	@cd ./MicroServices/FeaturePipeline/KafkaToFeatureStore && poetry run ruff check --fix

FormatCode:
	@cd ./MicroServices/FeaturePipeline/TradeProducer && poetry run ruff format
	@cd ./MicroServices/FeaturePipeline/OHLCTradeAggregator && poetry run ruff format
	@cd ./MicroServices/FeaturePipeline/KafkaToFeatureStore && poetry run ruff format

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

#--------------------------------------#
# MicroServices -  KafkaToFeatureStore #
#--------------------------------------#

#Similar Command to BuildLiteKafkaToFS but had to manage dependencies through multi-stage Docker Build
BuildKafkaToFSContainer:
	DOCKER_BUILDKIT=1 docker build --target=Runtime -t kafkatofs ./MicroServices/FeaturePipeline/KafkaToFeatureStore -f ./MicroServices/FeaturePipeline/KafkaToFeatureStore/KafkaToFS.Dockerfile

RunKafkaToFSContainer: ComposeRedPanda BuildKafkaToFSContainer
	docker run --network redpanda-network --name kafkatofs -d -it kafkatofs

StartKafkaToFSContainer:
	docker start kafkatofs

StopKafkaToFSContainer:
	docker stop kafkatofs

RmKafkaToFSContainer: StopKafkaToFSContainer
	docker rm kafkatofs

RmKafkaToFSImage: StopKafkaToFSContainer RmKafkaToFSContainer
	docker rmi kafkatofs

RebuildKafkaToFSContainer: RmKafkaToFSImage RunKafkaToFSContainer
	@echo "Rebuilt Image and ReRan Kafka To Feature Store Container"

BuildLiteKafkaToFSContainer:
	DOCKER_BUILDKIT=1 docker build --target=Runtime -t litekafkatofs ./MicroServices/FeaturePipeline/KafkaToFeatureStore -f ./MicroServices/FeaturePipeline/KafkaToFeatureStore/LiteKafkaToFS.Dockerfile

RmLiteKafkaToFSImage: 
	docker rmi litekafkatofs
	
TerminalIntoKafkaToFS:
	docker exec -it -u root kafkatofs /bin/bash

#------------------------#
# Bundles and Wrapped Up #
#------------------------#

# StartUp: ComposeRedPanda RunTradeProducerContainer RunTradeAggregatorContainer RunKafkaToFSContainer
#	@echo "Containers Fired Up, here are the Logs"
#	docker ps -a
#	docker logs tradeproducer
#	docker logs tradeaggregator
#	docker logs kafkatofs

ComposeFeaturePipeline:
	@docker compose -f ./MicroServices/FeaturePipeline/DockerComposeBundles/FeaturePipeline.yml up -d

StartUp: ComposeRedPanda ComposeFeaturePipeline

ShutDown: RmTradeProducerImage RmTradeAggregatorImage RmKafkaToFSImage ShutDownRedPanda	
	@echo "Everything Shat Down"
	docker images
	docker ps -a 

Restart: ShutDown StartUp