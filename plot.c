#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

int find( char c, char * in) {
	int i;
	for( i = 0; i < strlen(in); i++ )
		if(in[i] == c)
			return i;
	return -1;
}

char * substring( char * in, int start, int end ) {
	char * out = (char *) malloc(end - start);
	int i;
	for( i = start; i < end; i++ ) {
		out[i - start] = in[i];
	}
	return out;
}

int main( int argc, char ** args ) {
	char * line, * x_str, * y_str;

	size_t buffer = 10000;
	size_t data_size = 100000;

	int sep, x, y, count, i;

	line = (char *) malloc(buffer + 1);
	count = 0;

	int data[2][data_size];

	while( !feof( stdin ) ) {
		getline( &line, &buffer, stdin );
	
		sep = find('\t', line);
		if(sep < 0 || strlen(line) <= 1) {
			continue;
		} else {
			x_str = substring( line, 0, sep );
			y_str = substring( line, sep + 1, strlen(line) - 1);

			x = atoi( x_str );
			y = atoi( y_str );

			data[0][count] = x;
			data[1][count] = y;
			count++;
		}
	}

	free( line );
	
	for( i = 0; i < count; i++ ) {
		printf("%d - %d\n", data[0][i], data[1][i]);
	}
}
