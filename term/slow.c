#include <signal.h>
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
//#include <allegro.h>

int main(int argc, char **argv){
	struct sigaction usr_action;
	sigset_t block_mask;
	pid_t target = atoi(argv[1]);

	while(1){
		kill(target, SIGSTOP);
		usleep(500);
		kill(target, SIGCONT);
		usleep(50);
	}

	return 0;
}