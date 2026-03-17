#include <stdio.h>
#include <stdlib.h>

// ==================== Doubly Linked List ====================
typedef struct dll_node {
    int data;
    struct dll_node *prev;
    struct dll_node *next;
} dll_node;

// Helper to create a new node (for demonstration)
dll_node* dll_create_node(int value) {
    dll_node *new_node = malloc(sizeof(dll_node));
    if (new_node) {
        new_node->data = value;
        new_node->prev = NULL;
        new_node->next = NULL;
    }
    return new_node;
}

// Insert at beginning (example)
void dll_insert_begin(dll_node **head, int value) {
    dll_node *new_node = dll_create_node(value);
    if (!new_node) return;
    new_node->next = *head;
    if (*head) (*head)->prev = new_node;
    *head = new_node;
}

// dll_next_element: return pointer to next element or NULL
dll_node* dll_next_element(dll_node *element) {
    return element ? element->next : NULL;
}

// dll_prev_element: return pointer to previous element or NULL
dll_node* dll_prev_element(dll_node *element) {
    return element ? element->prev : NULL;
}

// ==================== Singly Linked List ====================
typedef struct sll_node {
    int data;
    struct sll_node *next;
} sll_node;

// Helper for singly linked list
sll_node* sll_create_node(int value) {
    sll_node *new_node = malloc(sizeof(sll_node));
    if (new_node) {
        new_node->data = value;
        new_node->next = NULL;
    }
    return new_node;
}

void sll_insert_begin(sll_node **head, int value) {
    sll_node *new_node = sll_create_node(value);
    if (!new_node) return;
    new_node->next = *head;
    *head = new_node;
}

// sll_prev_element: return pointer to previous element (must traverse from head)
sll_node* sll_prev_element(sll_node *head, sll_node *element) {
    if (!head || !element || head == element) return NULL;
    sll_node *current = head;
    while (current && current->next != element) {
        current = current->next;
    }
    return current; // will be NULL if element not found or no previous
}

// ==================== Stack (using singly linked list) ====================
typedef struct stack {
    sll_node *top;
} stack;

stack* stack_create() {
    stack *s = malloc(sizeof(stack));
    if (s) s->top = NULL;
    return s;
}

void stack_push(stack *s, int value) {
    if (!s) return;
    sll_node *new_node = sll_create_node(value);
    if (!new_node) return;
    new_node->next = s->top;
    s->top = new_node;
}

// Returns 0 on success, -1 on error (empty stack)
int stack_pop(stack *s, int *result) {
    if (!s || !s->top) return -1;
    sll_node *temp = s->top;
    *result = temp->data;
    s->top = temp->next;
    free(temp);
    return 0;
}

// ==================== Queue (using singly linked list with head and tail) ====================
typedef struct queue {
    sll_node *front;
    sll_node *rear;
} queue;

queue* queue_create() {
    queue *q = malloc(sizeof(queue));
    if (q) {
        q->front = q->rear = NULL;
    }
    return q;
}

void queue_enqueue(queue *q, int value) {
    if (!q) return;
    sll_node *new_node = sll_create_node(value);
    if (!new_node) return;
    if (q->rear == NULL) {
        q->front = q->rear = new_node;
    } else {
        q->rear->next = new_node;
        q->rear = new_node;
    }
}

// Returns 0 on success, -1 on error (empty queue)
int queue_dequeue(queue *q, int *result) {
    if (!q || !q->front) return -1;
    sll_node *temp = q->front;
    *result = temp->data;
    q->front = temp->next;
    if (q->front == NULL) q->rear = NULL;
    free(temp);
    return 0;
}

// ==================== Test (optional) ====================
int main() {
    // Test doubly linked list
    dll_node *dll_head = NULL;
    dll_insert_begin(&dll_head, 10);
    dll_insert_begin(&dll_head, 20);
    dll_insert_begin(&dll_head, 30);
    printf("Doubly linked list forward: ");
    for (dll_node *p = dll_head; p; p = dll_next_element(p))
        printf("%d ", p->data);
    printf("\nBackward: ");
    dll_node *last = dll_head;
    while (last && last->next) last = last->next;
    for (dll_node *p = last; p; p = dll_prev_element(p))
        printf("%d ", p->data);
    printf("\n");

    // Test singly linked list prev_element
    sll_node *sll_head = NULL;
    sll_insert_begin(&sll_head, 5);
    sll_insert_begin(&sll_head, 15);
    sll_insert_begin(&sll_head, 25);
    sll_node *target = sll_head->next; // 15
    sll_node *prev = sll_prev_element(sll_head, target);
    if (prev)
        printf("Previous of %d is %d\n", target->data, prev->data);
    else
        printf("No previous element\n");

    // Test stack
    stack *s = stack_create();
    stack_push(s, 100);
    stack_push(s, 200);
    int val;
    if (stack_pop(s, &val) == 0) printf("Stack pop: %d\n", val);
    if (stack_pop(s, &val) == 0) printf("Stack pop: %d\n", val);
    if (stack_pop(s, &val) == -1) printf("Stack empty\n");

    // Test queue
    queue *q = queue_create();
    queue_enqueue(q, 1);
    queue_enqueue(q, 2);
    queue_enqueue(q, 3);
    if (queue_dequeue(q, &val) == 0) printf("Queue dequeue: %d\n", val);
    if (queue_dequeue(q, &val) == 0) printf("Queue dequeue: %d\n", val);
    if (queue_dequeue(q, &val) == 0) printf("Queue dequeue: %d\n", val);
    if (queue_dequeue(q, &val) == -1) printf("Queue empty\n");

    // Free memory (not strictly necessary for this demo, but good practice)
    // For simplicity, we skip full cleanup. In real code, you'd free all nodes.

    return 0;
}