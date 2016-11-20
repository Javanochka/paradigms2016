#include "thread_pool.h"
#include "stdio.h"


void *consumer(void *data) {
	ThreadPool_t* pool = (ThreadPool_t*)data;	
	squeue_t *queue = &pool->task_queue;

	while (pool->cont || squeue_size(queue)) {
		pthread_mutex_lock(&queue->mutex);
		while (pool->cont && !squeue_size(queue)) {
			pthread_cond_wait(&queue->cond, &queue->mutex);
		}
		list_node_t* node = queue_pop(&queue->queue);
		pthread_mutex_unlock(&queue->mutex);
		if (node) {
			Task_t *task = (Task_t *)node;
			pthread_mutex_lock(&task->mutex);
			task->f(task->arg);
			task->done = true;
			pthread_cond_signal(&task->cond);
			pthread_mutex_unlock(&task->mutex);
		}
	}
	return NULL;
}

Task_t* new_task(void (*f)(void *), void* arg) {
	Task_t* task = malloc(sizeof(*task));
	task->f = f;
	task->arg = arg;

	task->done = false;
	pthread_mutex_init(&task->mutex, NULL);
	pthread_cond_init(&task->cond, NULL);
	return task;
}

void thpool_init(ThreadPool_t* pool, unsigned threads_nm) {
	pool->cont = 1;
	pool->threads_nm = threads_nm;
	pool->all_threads = malloc(threads_nm*sizeof(pthread_t));
	squeue_init(&pool->task_queue);
	for(int i = 0; i < threads_nm; i++) {
		pthread_create(&pool->all_threads[i], NULL, consumer, pool);
	}
}

void thpool_submit(ThreadPool_t* pool, Task_t* task) {
	squeue_push(&pool->task_queue, (list_node_t*)task);
}

void thpool_wait(Task_t* task) {
	if(!task) {
		return;
	}
	pthread_mutex_lock(&task->mutex);
	while(!task->done) {
		pthread_cond_wait(&task->cond, &task->mutex);
	}
	pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(ThreadPool_t* pool) {
	pthread_mutex_lock(&pool->task_queue.mutex);
	pool->cont = 0;
	pthread_mutex_unlock(&pool->task_queue.mutex);
	
	squeue_notify_all(&pool->task_queue);
	for (int i = 0; i < pool->threads_nm; i++) {
		pthread_join(pool->all_threads[i], NULL);
	}
	free(pool->all_threads);
	squeue_finit(&pool->task_queue);
}
