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

}