CFLAGS = -march=native -O3

# march=native and O3 are optimization flags
# lz is zlib
# lm is the math library
# fpic is useful for shared libraries as it allows to move the library:
#      "Position Independent Code means that the generated machine code is not
#       dependent on being located at a specific address in order to work."

IIOLIBS = -lm

default: fpc

# generic rule for building binary objects from C sources
%.o : %.c
	$(CC) -fpic $(CFLAGS) -c $< -o $@

fpc: filt-3D-point-cloud.so

filt-3D-point-cloud.so: filt-3D-point-cloud.o
	$(CC) -shared $^ -o $@

clean:
	$(RM) *.o *.so

