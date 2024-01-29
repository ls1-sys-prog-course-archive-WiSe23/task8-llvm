all:
	mkdir -p build
	cd build; cmake -G Ninja -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
	ninja -Cbuild

.PHONY clean:
	rm -rf build target
