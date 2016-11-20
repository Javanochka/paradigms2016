#include "thread_pool.h"
#include "stdio.h"
#include "stdlib.h"
#include "stddef.h"
#include "string.h"

typedef struct sort_data {
	int* arr;
	Task_t* left;
	Task_t* right;	
	int len;
	int rec_step;
	ThreadPool_t* pool;
}sort_data_t;

void sort_data_init(sort_data_t* data, int *arr, int len, int rec_step, ThreadPool_t* pool) {
	data->left = NULL;
	data->right = NULL;
	data->arr = arr;
	data->len = len;
	data->rec_step = rec_step;
	data->pool = pool;
}

static int compare_int(const void* a, const void* b) {
	int* pa = (int*)a;
	int* pb = (int*)b;
	return *pa - *pb;
}

void swap(int *a, int *b) {
	int t = *a;
	*a = *b;
	*b = t;
}

void sort_fun(void* arg) {
	sort_data_t* data = arg;
	if(data->len <= 1) return;
	if(data->rec_step == 0) {
		qsort(data->arr, data->len, sizeof(int), compare_int);
		return;
	}
	int part_el = data->arr[data->len/2];
	int i = 0;
	int j = data->len-1;
	do {
		while (data->arr[i] < part_el) i++;
		while (data->arr[j] > part_el) j--;

		if(i <= j) {
			if (data->arr[i] > data->arr[j]) swap(&data->arr[i], &data->arr[j]);
			i++;
			j--;
		}
	} while (i <= j);
	if(i < data->len - 1) {
		sort_data_t* right = malloc(sizeof(*right));
		sort_data_init(right, data->arr + i, data->len - i, data->rec_step-1, data->pool);
		Task_t* task = new_task(sort_fun, (void*)(right));
		data->right = task;
		thpool_submit(right->pool, task);
	}
	if(0 < j) {
		sort_data_t* left = malloc(sizeof(*left));
		sort_data_init(left, data->arr, j+1, data->rec_step-1, data->pool);
		Task_t* task = new_task(sort_fun, (void*)(left));
		data->left = task;
		thpool_submit(left->pool, task);
	}
}

void wait_for_sort_tasks(Task_t* cur){
	if(cur == NULL) {
		return;
	}
	thpool_wait(cur);
	wait_for_sort_tasks(((sort_data_t*)(cur->arg))->left);
	wait_for_sort_tasks(((sort_data_t*)(cur->arg))->right);
	free(cur->arg);
	free(cur);
}

bool sorted(int* arr, int len) {
	for(int i = 1; i < len; i++) {
		if(arr[i] < arr[i-1]) {
			return false;
		}
	}
	return true;
}

int main(int argc, char* argv[]) {
	if(argc != 4) {
		printf("Format: threads_nm, array_len, rec_lim.\n");
		return 1;
	}
	int threads_nm = atoi(argv[1]);
	int array_len = atoi(argv[2]);
	int rec_lim = atoi(argv[3]);
	srand(42);

	int *arr = malloc(sizeof(int) * array_len);
	for(int i = 0; i < array_len; i++) {
		arr[i] = rand();
	}
	ThreadPool_t pool;
	thpool_init(&pool, threads_nm);
	sort_data_t* start = malloc(sizeof(*start));		
	sort_data_init(start, arr, array_len, rec_lim, &pool);
	Task_t* task = new_task(sort_fun, (void*)(start));
	thpool_submit(start->pool, task);
	wait_for_sort_tasks(task);

	if(!sorted(arr, array_len)) {
		printf("Sorry, I didn't manage to sort the array.\n");
		return 2;
	}

	thpool_finit(&pool);
	free(arr);
	pthread_exit(NULL);
	return 0;
}
