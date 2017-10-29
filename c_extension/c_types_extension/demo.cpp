extern "C" {

int sum_int(int first, int second) {
    return first + second;
}

float sum_float(float first, float second) {
    return first + second;
}

double sum_double(double first, double second) {
    return first + second;
}

char modify_char(char input){
    return input + 1;
}

bool modify_bool(bool input){
    if(input)
        return false;
    else
        return true;
}

int sum_array(int array[], int size){
    int sum = 0;
    for(int i=0; i<size; i++){
        sum += array[i];
    }
    return sum;
}

float *sum_float_pointer(float *f, int size){
    for(int i=0; i<size; i++){
        f[i] += 0.09;
    }
    return f;
}

char *upper_char_array(char *array, int size){
    for(int i=0; i<size; i++){
        array[i] -= 32;
    }
    return array;
}

void modify_array(int &e, int *&f)
{
    e=10;
    f=new int[e];
    for(int i=0;i<e;i++)
        f[i]=i;
}

// pointer char
// structure
// ref &
// *&
}