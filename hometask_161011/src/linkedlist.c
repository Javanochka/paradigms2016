#include "linkedlist.h"

void list_insert(list_node_t *node, list_node_t *new) {
	new->prev = node;
	new->next = node->next;
	node->next->prev = new;
	node->next = new;
}

void list_remove(list_node_t *node) {
	node->prev->next = node->next;
	node->next->prev = node->prev;
}
