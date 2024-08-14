StartTradeProducerContainer:
	docker start tradeproducer

StopTradeProducerContainer:
	docker stop tradeproducer

RmTradeProducerContainer:StopTradeProducerContainer
	docker rm tradeproducer

RmTradeProducerImage:StopTradeProducerContainer:RmTradeProducerContainer
	docker rmi tradeproducer

ComposeRedPanda:
	docker compose -f ./MicroServices/RedPanda.yml up -d

ShutDownRedPanda:
	docker compose -f ./MicroServices/RedPanda.yml down

BuildTradeProducerContainer:
	docker build -t tradeproducer ./MicroServices/TradeProducer -f ./MicroServices/TradeProducer/TradeProducer.Dockerfile

RunTradeProducerContainer:ComposeRedPanda BuildTradeProducerContainer
	docker run --network redpanda-network --name tradeproducer -d -it tradeproducer

LintCode:
	cd ./MicroServices/TradeProducer && poetry run ruff check --fix

FormatCode:
	cd ./MicroServices/TradeProducer && poetry run ruff format