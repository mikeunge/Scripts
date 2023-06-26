FRAMEWORK_PATH = -F/System/Library/PrivateFrameworks
FRAMEWORK      = -framework Carbon -framework Cocoa -framework CoreServices -framework SkyLight -framework ScriptingBridge -framework IOKit
BUILD_FLAGS    = -std=c99 -Wall -DDEBUG -g -O0 -fvisibility=hidden -mmacosx-version-min=10.13
BUILD_PATH     = ./bin
TARGET         = bettery
BINS           = $(BUILD_PATH)/$(TARGET)
CC             = clang

ifeq ($(PREFIX),)
    PREFIX := /usr/local/bin
endif

.PHONY: all clean install

all: clean $(BINS)

install: $(TARGET).m
	mkdir -p $(BUILD_PATH)
	$(CC) $^ $(BUILD_FLAGS) $(FRAMEWORK_PATH) $(FRAMEWORK) -o $(BUILD_PATH)/$(TARGET)
	cp -v $(BINS) $(PREFIX)

clean:
	rm -rf $(BUILD_PATH)

build: $(TARGET).m
	mkdir -p $(BUILD_PATH)
	$(CC) $^ $(BUILD_FLAGS) $(FRAMEWORK_PATH) $(FRAMEWORK) -o $(BUILD_PATH)/$(TARGET)
