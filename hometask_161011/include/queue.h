#ifndef __QUEUE_H__
#define __QUEUE_H__

#include "linkedlist.h"

typedef struct queue {
	struct list_node head;
	unsigned long size;
} queue_t;

void queue_init(queue_t *queue);
unsigned long queue_size(queue_t *queue);
void queue_push(queue_t *queue, list_node_t *node);
list_node_t *queue_pop(queue_t *queue);

#endif
