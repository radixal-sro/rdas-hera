# Makefile for Radixal Deep-Space Autonomy Suite (R-DAS)
# Target: GR712RC Dual-Core LEON3 (SPARC V8 @ 50 MHz), Core 1 Bare-Metal

CC = sparc-gaisler-elf-gcc
CFLAGS = -mcpu=leon3 -O2 -Wall -Wextra -Wpedantic -std=c99 \
         -ffreestanding -nostdlib -fno-builtin \
         -I../podklady/simulation_layer/esw_interface

LDFLAGS = -Ttext=0x40000000 -nostartfiles

OBJS = rdas_wavelet.o rdas_saliency.o rdas_main.o

all: rdas_core1.elf

rdas_core1.elf: $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) rdas_core1.elf

.PHONY: all clean
