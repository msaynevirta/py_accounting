CXX=g++
RM=rm -f
CPPFLAGS=-g
LDFLAGS=-g
SRCS=data_handling/data_core.cpp data_handling/file_readers/common_reader.cpp data_handling/bank_data/bank_data.cpp data_handling/bank_data/bank_data_op.cpp data_handling/bank_data/bank_data_nordea.cpp main.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

JSONCPP=jsoncpp/build/debug/src/lib_json/libjsoncpp.a

all: main

main: $(OBJS)
	$(CXX) $(LDFLAGS) -o main $(OBJS) $(JSONCPP) -lm

depend: .depend

.depend: $(SRCS)
	$(RM) ./.(depend)
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) main
	