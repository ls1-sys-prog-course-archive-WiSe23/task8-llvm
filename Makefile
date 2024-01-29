# this target should build all executables for all tests
all: dce memory-safety

.PHONY clean:
	$(MAKE) -C tasks/dead-code-elimination clean
	$(MAKE) -C tasks/memory-safety clean
	$(MAKE) -C tests/memory-safety clean

dce:
	$(MAKE) -C tasks/dead-code-elimination

memory-safety:
	$(MAKE) -C tasks/memory-safety
	$(MAKE) -C tests/memory-safety

check: check-dce check-memory-safety


check-dce: dce
	$(MAKE) -C tests/dce check

check-memory-safety: memory-safety
	$(MAKE) -C tests/memory-safety check
