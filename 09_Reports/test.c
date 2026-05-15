#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int n; // nombre de threads
int compteur_arrivee = 0;

pthread_mutex_t mutex;
pthread_cond_t condition;

void pre_traitement(int id) {
    printf("Thread %d : pré-traitement...\n", id);
    sleep(rand() % 3);
}

void pret_ligne_depart(int id) {
    printf("Thread %d : prêt sur la ligne de départ\n", id);
    sleep(1);
}

void course(int id) {
    printf("Thread %d : en cours...\n", id);
    sleep(rand() % 5);
}

int arrivee(int id) {
    int rang;

    pthread_mutex_lock(&mutex);

    compteur_arrivee++;
    rang = compteur_arrivee;

    printf("Thread %d est arrivé au rang %d\n", id, rang);

    if (compteur_arrivee == n) {
        printf("Thread %d : dernier arrivé -> déclenchement !\n", id);
        pthread_cond_broadcast(&condition);
    } else {
        while (compteur_arrivee < n) {
            pthread_cond_wait(&condition, &mutex);
        }
    }

    pthread_mutex_unlock(&mutex);

    return rang;
}

void* fonction_thread(void* arg) {
    int id = *((int*)arg);

    pre_traitement(id);
    pret_ligne_depart(id);
    course(id);

    int rang = arrivee(id);

    printf("Thread %d continue après synchronisation (rang=%d)\n", id, rang);

    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    int i;

    if (argc != 2) {
        printf("Usage: %s <nombre_threads>\n", argv[0]);
        return 1;
    }

    n = atoi(argv[1]);

    if (n <= 0) {
        printf("Le nombre de threads doit être > 0\n");
        return 1;
    }

    pthread_t threads[n];
    int ids[n];

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&condition, NULL);

    srand(time(NULL));

    for (i = 0; i < n; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, fonction_thread, &ids[i]);
    }

    for (i = 0; i < n; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&condition);

    printf("Fin du programme\n");

    return 0;
}