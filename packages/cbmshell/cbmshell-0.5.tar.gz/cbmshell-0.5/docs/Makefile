SPHINX_BUILD = sphinx-build-3
OPTS = -nvWT
OUTPUT_DIR = out


.PHONY: html
html:
	$(SPHINX_BUILD) -b html $(OPTS) . $(OUTPUT_DIR)

.PHONY: clean
clean:
	rm -rf $(OUTPUT_DIR)
