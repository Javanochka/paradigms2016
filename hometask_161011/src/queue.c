#include "string.h"
#include "queue.h"

void queue_init(queue_t *queue) {
	queue->head.prev = &queue->head;
	queue->head.next = &queue->head;
	queue->size = 0;
}

unsigned long queue_size(queue_t *queue) {
	return queue->size;
}

void queue_push(queue_t *queue, list_node_t *node) {
	list_insert(&queue->head, node);
	queue->size += 1;
}

list_node_t *queue_pop(queue_t *queue) {
	list_node_t *node = queue->head.prev;
	if (!queue_size(queue))
		return NULL;
	list_remove(node);
	queue->size -= 1;
	return node;
}
