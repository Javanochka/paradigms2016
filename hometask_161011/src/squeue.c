#include "squeue.h"

void squeue_init(squeue_t *squeue)
{
	queue_init(&squeue->queue);
	pthread_mutex_init(&squeue->mutex, NULL);
	pthread_cond_init(&squeue->cond, NULL);
}

void squeue_finit(squeue_t *squeue)
{
	pthread_mutex_destroy(&squeue->mutex);
	pthread_cond_destroy(&squeue->cond);
}

void squeue_push(squeue_t *squeue, list_node_t *node)
{
	pthread_mutex_lock(&squeue->mutex);
	queue_push(&squeue->queue, node);
	pthread_cond_signal(&squeue->cond);
	pthread_mutex_unlock(&squeue->mutex);
}

int squeue_size(squeue_t* queue) {
	return queue_size(&queue->queue);
}

list_node_t *squeue_pop(squeue_t *squeue)
{
	list_node_t *node;

	pthread_mutex_lock(&squeue->mutex);
	node = queue_pop(&squeue->queue);
	pthread_mutex_unlock(&squeue->mutex);
	return node;
}

void squeue_notify(squeue_t* queue) {
	pthread_mutex_lock(&queue->mutex);
	pthread_cond_signal(&queue->cond);
	pthread_mutex_unlock(&queue->mutex);
}

void squeue_notify_all(squeue_t* queue) {
	pthread_mutex_lock(&queue->mutex);
	pthread_cond_broadcast(&queue->cond);
	pthread_mutex_unlock(&queue->mutex);
}
