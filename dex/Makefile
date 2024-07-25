PYTHON=python3.12

.PHONY: install run clean uninstall

run: install
	dex ./records.csv

uninstall: clean
	$(PYTHON) -m pip uninstall -y dex

install: uninstall
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -e .

clean:
	rm -rf *.egg-info || true
	rm -f *.json || true
