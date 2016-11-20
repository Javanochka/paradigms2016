SRCS = main.c thread_pool.c linkedlist.c queue.c squeue.c
INCLUDES = -I include
OBJS = $(SRCS:.c=.o)

pqsort: bin $(addprefix bin/, $(OBJS))
	gcc -std=c99 $(addprefix bin/, $(OBJS)) -o pqsort -lpthread

all: pqsort
	

bin: 
	mkdir -p bin

bin/main.o: src/main.c include/*.h
	gcc -std=c99 -c -g src/main.c -o bin/main.o $(INCLUDES)

bin/thread_pool.o: src/thread_pool.c include/*.h
	gcc -std=c99 -c -g src/thread_pool.c -o bin/thread_pool.o $(INCLUDES)

bin/queue.o: src/queue.c include/*.h
	gcc -std=c99 -c -g src/queue.c -o bin/queue.o $(INCLUDES)

bin/squeue.o: src/squeue.c include/*.h
	gcc -std=c99 -c -g src/squeue.c -o bin/squeue.o $(INCLUDES)

bin/linkedlist.o: src/linkedlist.c include/*.h
	gcc -std=c99 -c -g src/linkedlist.c -o bin/linkedlist.o $(INCLUDES)

clean:
	rm -rf bin pqsort
