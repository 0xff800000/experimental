#include <math.h>
#define LUT 256
char sinelut[LUT];

void main(){
	// Init sine look-up-table
	for(int i=0; i<LUT; i++){
		sinelut[i] = (char)255*sin(i*(double)(2*3.14)/LUT);
		sinelut[i] = 'a';
	}
	while(1){
		for(int i=0;;i++)
		{
			// putchar(i++<<2+i);
			if(i>LUT-1)i=0;
			putchar(sinelut[i]);
		}
	}
}
