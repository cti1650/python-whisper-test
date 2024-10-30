conv:
	docker compose run --rm python3 python main.py

conv_sub:
	docker compose run --rm python3 python sub.py

sample:
	docker compose run --rm python3 python sample.py

sample2:
	docker compose run --rm python3 python sample2.py

sample3:
	docker compose run --rm python3 python sample3.py

build:
	docker compose build

down:
	docker compose down

clean:
	docker compose down --volumes

all-clean:
	docker compose down --rmi all --volumes --remove-orphans