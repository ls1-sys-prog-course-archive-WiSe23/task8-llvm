LLC=llc
OPT=opt
CC=clang
CFLAGS =
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
	PASS_PLUGIN = ../../tasks/memory-safety/build/libMemorySafety.so
endif
ifeq ($(UNAME_S),Darwin)
	PASS_PLUGIN = ../../tasks/memory-safety/build/libMemorySafety.dylib
endif
PASS_RTLIB = ../../tasks/memory-safety/build/libMemorySafetyRuntime.a

SRC = $(wildcard *.c)
LLS = $(patsubst %.c, build/%.ll, $(SRC))
LLS_SAN = $(patsubst %.c, build/%-san.ll, $(SRC))
PROGRAMS = $(patsubst %.c, build/%-san.out, $(SRC))

.PRECIOUS: $(LLS)
.PRECIOUS: $(LLS_SAN)
.PRECIOUS: $(OBJ)
.PRECIOUS: $(PROGRAMS)

all: clean build $(PROGRAMS) build/performance.out

.PHONY: clean
clean:
	rm -rf build

.PHONY:
build:
	mkdir -p build

.PHONY:
build/%.out: build/%.ll
	$(CC) -lstdc++ -g $< $(PASS_RTLIB) -o $@

# make sure the sanitized build step is _always_ executed
.PHONY: build/%-san.ll
build/%-san.ll: build/%.ll
	$(OPT) -load-pass-plugin $(PASS_PLUGIN) -passes=memory-safety -S -o $@ $<

build/%.ll: %.c
	@$(CC) -g -O1 -S -emit-llvm $< -o $@

.PHONY: check
check: all
	python3 test-malloc.py
	python3 test-use-after-free.py
	python3 test-stack.py
	python3 test-performance.py
