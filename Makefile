.PHONY: load dry-run

load:
	python3 event_sources/main.py

dry-run:
	python3 event_sources/main.py --dry-run --scenarios 1
