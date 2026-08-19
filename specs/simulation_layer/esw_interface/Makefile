# --------------------------------------------------------------------
# Hera Call for Ideas, ESW 
# --------------------------------------------------------------------

CC = sparc-gaisler-elf-gcc
OBJCOPY = sparc-gaisler-elf-objcopy

TARGET = hera_test.elf

SRCS = start.S test_main.c hera_client_stub.c

OBJS = $(SRCS:.c=.o)
OBJS := $(OBJS:.S=.o)
CFLAGS = -mcpu=leon3 -g -O0 -Wall

LDFLAGS = -nostartfiles -Ttext=0x40000000

all: $(TARGET)

$(TARGET): $(OBJS)
	@echo " [LINK] $@"
	@$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

%.o: %.c
	@echo " [CC]   $<"
	@$(CC) $(CFLAGS) -c $< -o $@

%.o: %.S
	@echo " [ASM]  $<"
	@$(CC) $(CFLAGS) -c $< -o $@

run: $(TARGET)
	@echo "--------------------------------------------------"
	@echo "Starting QEMU LEON3... (Ctrl+C to exit)"
	@echo "--------------------------------------------------"
	qemu-system-sparc -M leon3_generic -display none -serial stdio -kernel $(TARGET)

debug: $(TARGET)
	@echo "QEMU waiting for GDB connection on port 1234..."
	qemu-system-sparc -M leon3_generic -display none -serial stdio -kernel $(TARGET) -s -S

clean:
	rm -f $(OBJS) $(TARGET)
