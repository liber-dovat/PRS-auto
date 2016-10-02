#define CMAXstr 200
int mostrar_vector_double(double *, int, int);
int mostrar_vector_double(double *, int, int);
int procesar_NetCDF_VIS_gri(double **, double **, double **, int **, int **,  int **,
	double, double, double, double, double, double, double, double, 
	int, int, int, char[CMAXstr]);
int generar_grilla(double **, double **, double **, double **,
	double, double, double, double, double, double, int*, int*, int*);
int cargar_calibracion_VIS(char[CMAXstr], int **, int **,
	double **, double **, double **, double **, double **);