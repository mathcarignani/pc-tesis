CC := g++
CFLAGS := -Wall -Werror -Wextra -ansi -pedantic -g

BUILDDIR := build
SRCDIR := src
SRCEXT := cpp
TARGET := app
LIB :=
INC := -I include

SOURCES := $(shell find $(SRCDIR) -type f -name *.$(SRCEXT))
OBJECTS := $(patsubst $(SRCDIR)/%,$(BUILDDIR)/%,$(SOURCES:.$(SRCEXT)=.o))

$(TARGET): $(OBJECTS)
		@echo " Linking..."
		@echo " $(CC) $^ -o $(TARGET) $(LIB)"; $(CC) $^ -o $(TARGET) $(LIB) -dynamic

$(BUILDDIR)/%.o: $(SRCDIR)/%.$(SRCEXT)
		@mkdir -p $(BUILDDIR)
		@echo " $(CC) $(CFLAGS) $(INC) -c -o -O2 $@ $<"; $(CC) $(CFLAGS) $(INC) -c -o $@ $<

clean:
		@echo " Cleaning...";
		@echo " $(RM) -r $(BUILDDIR) $(TARGET)"; $(RM) -r $(BUILDDIR) $(TARGET)

.PHONY: clean
	