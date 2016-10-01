#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <math.h>
//#include "mpi.h"
//#include "libASIcom.h"
//#include "libPRS_T000loc_VIS.h"

#define FALSE 0
#define TRUE !FALSE
//#define Csate 3
//#define Cpath 200

// SATELITES
static int CS_sate[3]={8,12,13};

// Versión 1.0, 09/2016 -- Rodrigo Alonso Suárez.

int main(int argc, char *argv[]){

	FILE * data;
	char* PATH;
	char* DATAspt;
	char sptCOD[15];
	int		h1, Ci, Cj, Ct;
	double	LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel;
	int * MSKmat;
	int * CNTmat;
	double * DATmat;
	double * LATmat; double * LONmat;
	double * LATvec; double * LONvec;

	// IMAGEN A PROCESAR
	PATH = "/rolo/WSolar/standalones/procesar_NetCDFs/data/goes13.2016.274.143507.BAND_01.nc";
	
	// ABRO ARCHIVO DE DATOS ESPACIAL
	DATAspt = argv[1];
	data = fopen(DATAspt, "ro"); if (data == NULL) {printf("No se encontro archivo de datos. Cerrando.\n"); return 0;}
	fscanf(data, "%lf\n", &LATmax);
	fscanf(data, "%lf\n", &LATmin);
	fscanf(data, "%lf\n", &LONmax);
	fscanf(data, "%lf\n", &LONmin);
	fscanf(data, "%lf\n", &dLATgri);
	fscanf(data, "%lf\n", &dLONgri);
	fscanf(data, "%lf\n", &dLATcel);
	fscanf(data, "%lf\n", &dLONcel);
	fscanf(data, "%s\n", &sptCOD);
	fclose(data);

	// TAMAÑO DE LA GRILLA ESPACIAL
	Ci = (int) (LATmax - LATmin)/dLATgri;
	Cj = (int) (LONmax - LONmin)/dLONgri;
	Ct = Ci*Cj;

	// ALOCO MEMORIA PARA LOS PROCESAMIENTOS
	if (!(MSKmat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(CNTmat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(DATmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(LATmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(LONmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(LATvec = (double *) malloc(Ci * sizeof(double *)))){return 0;}
	if (!(LONvec = (double *) malloc(Cj * sizeof(double *)))){return 0;}

	// VECTORES DE LATITUD Y LONGITUD
	for (h1=0; h1 < Ci; h1++){LATvec[h1] = LATmin + dLATgri*h1;}
	for (h1=0; h1 < Cj; h1++){LONvec[h1] = LONmin + dLONgri*h1;}

	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Archivos y Rutas -------------------------------------------------------------\n");
	printf("%s\n", PATH);
	printf("%s\n", DATA);
	printf("%s\n", sptCOD);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Resolucion Espacial ----------------------------------------------------------\n");
	printf("[Ci, Cj] = [%d, %d] --- Ct = [%d]\n", Ci, Cj, Ct);
	printf("LAT = [%+06.2f .. %+06.2f] --- GRILLA = [%+06.2f .. %+06.2f]\n", LATmax, LATmin, dLATgri, dLONgri);
	printf("LON = [%+06.2f .. %+06.2f] --- CELDAS = [%+06.2f .. %+06.2f]\n", LONmax, LONmin, dLATcel, dLONcel);
	printf("-----------------------------------------------------------------------------------\n");
	return 1;
}
