StartTradeProducerContainer:
	docker start tradeproducer

StopTradeProducerContainer:
	docker stop tradeproducer

RmTradeProducerContainer:StopTradeProducerContainer
	docker rm tradeproducer

RmTradeProducerImage:RmTradeProducerContainer
	docker rmi tradeproducer

ComposeRedPanda:
	docker compose -f ./MicroServices/RedPanda.yml up -d

ShutDownRedPanda:
	docker compose -f ./MicroServices/RedPanda.yml down

BuildTradeProducerContainer:
	docker build -t tradeproducer . -f TradeProducer.Dockerfile

RunTradeProducerContainer:ComposeRedPanda BuildTradeProducerContainer
	docker run --network redpanda-network --name tradeproducer -d -it tradeproducer