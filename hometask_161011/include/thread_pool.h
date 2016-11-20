#ifndef _THREADPOOL_H_

#include "pthread.h"
#include "stdlib.h"
#include "stdbool.h"
#include "squeue.h"

typedef struct Task {
	list_node_t node; //it is in queue
	void (*f)(void *); //some function
	void* arg; //some data, which will be written especially for YOUR task 
	
	bool done;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
} Task_t;
typedef struct ThreadPool {
	pthread_t* all_threads;
	unsigned threads_nm;
	squeue_t task_queue; //queue of Tasks
	volatile bool cont;
	
} ThreadPool_t;

Task_t* new_task(void (*f)(void *), void* arg);

void thpool_init(ThreadPool_t* pool, unsigned threads_nm);
void thpool_submit(ThreadPool_t* pool, Task_t* task);
void thpool_wait(Task_t* task);
void thpool_finit(ThreadPool_t* pool);
#endif
