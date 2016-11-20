#ifndef __LINKED_LIST_H__
#define __LINKED_LIST_H__

typedef struct list_node {
	struct list_node *next;
	struct list_node *prev;
}list_node_t;

void list_insert(list_node_t *node, list_node_t *new_node);
void list_remove(list_node_t *node);

#endif
