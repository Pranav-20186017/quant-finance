# Compiler and flags
CXX = g++
CXXFLAGS = -I . -lm

# Source files
SRCS = main.cpp Option.cpp Option_Price.cpp StdNormalCDF.cpp test.cpp
OBJS = $(SRCS:.cpp=.o)

# Output binary
TARGET = main

# Build rules
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)
