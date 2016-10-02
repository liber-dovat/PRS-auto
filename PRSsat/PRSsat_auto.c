#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "lib_PRSsat.h"
//#include "mpi.h"
//#include "libASIcom.h"
//#include "libPRS_T000loc_VIS.h"

#define FALSE 0
#define TRUE !FALSE
#define CMAXstr 200
#define Cste 3

// SATELITES
static int GOES[Cste]={8,12,13};

// Versión 1.0, 09/2016 -- Rodrigo Alonso Suárez.

int main(int argc, char *argv[]){

	FILE * data;
	char PATHimg[CMAXstr];
	char RUTAcal[CMAXstr];
	char RUTAsal[CMAXstr];
	char DATAspatial[CMAXstr];
	char DATAfolders[CMAXstr];
	char CODEspatial[15];
	int		h1, h2, h3, Ci, Cj, Ct;
	double	LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel;
	int * MSKmat;
	int * CNT1mat;
	int * CNT2mat;
	double * FRmat;
	double * RPmat;
	double * N1mat;
	double * LATmat; double * LONmat;
	double * LATvec; double * LONvec;
	int * CALvis_iniYEA; int * CALvis_iniDOY;
	double * CALvis_Xspace;
	double * CALvis_M;
	double * CALvis_K;
	double * CALvis_alfa;
	double * CALvis_beta;

	// IMAGEN A PROCESAR
	strncpy(PATHimg, "/rolo/WSolar/standalones/procesar_NetCDFs/data/goes13.2016.274.143507.BAND_01.nc", CMAXstr);
	strncpy(DATAfolders, argv[1], CMAXstr);
	strncpy(DATAspatial, argv[2], CMAXstr);

	// ABRO ARCHIVO FOLDERS:
	data = fopen(DATAfolders, "ro");
	if (data == NULL) {printf("No se encontro archivo de datos. Cerrando.\n"); return 0;}
	fscanf(data, "%s\n", &RUTAcal[0]);
	fscanf(data, "%s\n", &RUTAsal[0]);
	fclose(data);

	// ABRO ARCHIVO SPATIAL:
	data = fopen(DATAspatial, "ro");
	if (data == NULL) {printf("No se encontro archivo de datos. Cerrando.\n"); return 0;}
	fscanf(data, "%lf\n", &LATmax);
	fscanf(data, "%lf\n", &LATmin);
	fscanf(data, "%lf\n", &LONmax);
	fscanf(data, "%lf\n", &LONmin);
	fscanf(data, "%lf\n", &dLATgri);
	fscanf(data, "%lf\n", &dLONgri);
	fscanf(data, "%lf\n", &dLATcel);
	fscanf(data, "%lf\n", &dLONcel);
	fscanf(data, "%s\n",  &CODEspatial[0]);
	fclose(data);

	// PROCESAR IMAGEN
	cargar_calibracion_VIS(RUTAcal, &CALvis_iniYEA, &CALvis_iniDOY, &CALvis_Xspace,
		&CALvis_M, &CALvis_K, &CALvis_alfa, &CALvis_beta);
	generar_grilla(&LATmat, &LONmat, &LATvec, &LONvec,
		LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, &Ci, &Cj, &Ct);
	procesar_NetCDF_VIS_gri(&FRmat, &RPmat, &N1mat, &MSKmat, &CNT1mat, &CNT2mat,
	 	dLATgri, dLONgri, dLATcel, dLONcel, LATmax, LATmin, LONmax, LONmin,
	 	Ct, Ci, Cj, PATHimg);
	mostrar_vector_double(FRmat, Ct, Cj);
	mostrar_vector_double(N1mat, Ct, Cj);
	mostrar_vector_double(LATmat, Ct, Cj);
	mostrar_vector_double(LONmat, Ct, Cj);

	// MUESTRO VECTORES
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Archivos y Rutas -------------------------------------------------------------\n");
	printf("FOLDERS: %s\n", &DATAfolders[0]);
	printf("SPATIAL: %s\n", &DATAspatial[0]);
	printf("IMAGEN : %s\n", &PATHimg[0]);
	printf("RUTAcal: %s\n", &RUTAcal[0]);
	printf("RUTAsal: %s\n", &RUTAsal[0]);
	printf("CODIGO : %s\n", &CODEspatial[0]);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Resolucion Espacial ----------------------------------------------------------\n");
	printf("[Ci, Cj] = [%d, %d] --- Ct = [%d]\n", Ci, Cj, Ct);
	printf("LAT = [%+06.2f .. %+06.2f] --- GRILLA = [%+06.2f, %+06.2f]\n", LATmax, LATmin, dLATgri, dLONgri);
	printf("LON = [%+06.2f .. %+06.2f] --- CELDAS = [%+06.2f, %+06.2f]\n", LONmax, LONmin, dLATcel, dLONcel);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Vectores Regulares -----------------------------------------------------------\n");
	printf("LATITUDES:\n");
	mostrar_vector_double(LATvec, Ci, 10);
	printf("LONGITUDES:\n");
	mostrar_vector_double(LONvec, Cj, 10);
	printf("CALIBRACION:\n");
	mostrar_vector_int(CALvis_iniYEA, Cste, 10);
	mostrar_vector_int(CALvis_iniDOY, Cste, 10);
	mostrar_vector_double(CALvis_Xspace, Cste, 10);
	mostrar_vector_double(CALvis_M, Cste, 10);
	mostrar_vector_double(CALvis_K, Cste, 10);
	mostrar_vector_double(CALvis_alfa, Cste, 10);
	mostrar_vector_double(CALvis_beta, Cste, 10);
	printf("-----------------------------------------------------------------------------------\n");

	return 1;
}