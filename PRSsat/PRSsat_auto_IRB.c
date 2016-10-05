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
#define CFLNstr 34
#define Cste 3

// SATELITES
static int GOES[Cste]={8,12,13};

// Versión 1.0, 09/2016 -- Rodrigo Alonso Suárez.

int main(int argc, char *argv[]){

	FILE * data;
	char PATHimg[CMAXstr];
	char RUTAent[CMAXstr];
	char RUTAsal[CMAXstr];
	char RUTAcal[CMAXstr];
	char DATAspatial[CMAXstr];
	char DATAfolders[CMAXstr];
	char DATAimglist[CMAXstr];
	char imgs[CFLNstr];
	char CODEspatial[23];
	int		h1, h2, h3, Ci, Cj, Ct, tag, Cimgs;
	double	LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel;
	int * MSKmat;
	int * CNT1mat;
	int * CNT2mat;
	double * FRmat;
	double * RPmat;
	double * N1mat;
	double * CZmat;
	double * LATmat; double * LONmat;
	double * LATvec; double * LONvec;
	int * CALvis_iniYEA; int * CALvis_iniDOY;
	double * CALvis_Xspace;
	double * CALvis_M;
	double * CALvis_K;
	double * CALvis_alfa;
	double * CALvis_beta;

	// IMAGEN A PROCESAR
	strncpy(DATAfolders, argv[1], CMAXstr);
	strncpy(DATAspatial, argv[2], CMAXstr);
	strncpy(DATAimglist, argv[3], CMAXstr);

	// ABRO ARCHIVO FOLDERS:
	data = fopen(DATAfolders, "ro");
	if (data == NULL) {printf("No se encontro archivo folders. Cerrando.\n"); return 0;}
	fscanf(data, "%s\n", &RUTAent[0]);
	fscanf(data, "%s\n", &RUTAsal[0]);
	fscanf(data, "%s\n", &RUTAcal[0]);
	fclose(data);

	// ABRO ARCHIVO SPATIAL:
	data = fopen(DATAspatial, "ro");
	if (data == NULL) {printf("No se encontro archivo spatial. Cerrando.\n"); return 0;}
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

	// ABRO ARCHIVO IMGLIST:
	Cimgs = 0;
	data = fopen(DATAimglist, "ro");
	if (data == NULL) {printf("No se encontro archivo imglist. Cerrando.\n"); return 0;}
	while(fscanf(data, "%s\n", &imgs[0]) != EOF){
		Cimgs = Cimgs + 1;
	}
	fclose(data);
	char array_imgs[Cimgs][CFLNstr]; 
	Cimgs = 0;
	data = fopen(DATAimglist, "ro");
	if (data == NULL) {printf("No se encontro archivo imglist. Cerrando.\n"); return 0;}
	while(fscanf(data, "%s\n", &imgs[0]) != EOF){
		strcpy(array_imgs[Cimgs], &imgs[0]);
		Cimgs = Cimgs + 1;
	}
	fclose(data);

	// IMAGEN A PROCESAR
	strncpy(PATHimg, RUTAent, CMAXstr); strcat(PATHimg, array_imgs[0]);

	// RUTA DE SALIDA
	strcat(RUTAsal, CODEspatial); strcat(RUTAsal, "/");	

	// PROCESAR IMAGEN
	generar_grilla(&LATmat, &LONmat, &LATvec, &LONvec,
		LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, &Ci, &Cj, &Ct);
	guardar_grilla(RUTAsal, Ci, Cj, Ct, LATmax, dLATgri, LONmin, dLONgri,
		&LATvec[0], &LONvec[0], &LATmat[0], &LONmat[0]);
	cargar_calibracion_VIS(RUTAcal, &CALvis_iniYEA, &CALvis_iniDOY, &CALvis_Xspace,
		&CALvis_M, &CALvis_K, &CALvis_alfa, &CALvis_beta);
	procesar_NetCDF_VIS_gri(&FRmat, &RPmat, &N1mat, &CZmat,
		&MSKmat, &CNT1mat, &CNT2mat, &tag,
	 	dLATgri, dLONgri, dLATcel, dLONcel, LATmax, LATmin, LONmax, LONmin,
	 	Ct, Ci, Cj, PATHimg, RUTAsal, 
	 	CALvis_iniYEA, CALvis_iniDOY, CALvis_Xspace,
		CALvis_M, CALvis_K, CALvis_alfa, CALvis_beta);
	//mostrar_vector_double(FRmat, Ct, Cj);
	//mostrar_vector_double(CZmat, Ct, Cj);
	//mostrar_vector_double(RPmat, Ct, Cj);
	//mostrar_vector_int(MSKmat, Ct, Cj);

	// MUESTRO VECTORES
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Archivos y Rutas -------------------------------------------------------------\n");
	printf("FOLDERS: %s\n", &DATAfolders[0]);
	printf("SPATIAL: %s\n", &DATAspatial[0]);
	printf("IMGLIST: %s\n", &DATAimglist[0]);
	printf("IMAGEN : %s\n", &PATHimg[0]);
	printf("RUTAent: %s\n", &RUTAent[0]);
	printf("RUTAsal: %s\n", &RUTAsal[0]);
	printf("RUTAcal: %s\n", &RUTAcal[0]);
	printf("CODIGO : %s\n", &CODEspatial[0]);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Resolucion Espacial ----------------------------------------------------------\n");
	printf("[Ci, Cj] = [%d, %d] --- Ct = [%d]\n", Ci, Cj, Ct);
	printf("LAT = [%+06.2f .. %+06.2f] --- GRILLA = [%+06.2f, %+06.2f]\n", LATmax, LATmin, dLATgri, dLONgri);
	printf("LON = [%+06.2f .. %+06.2f] --- CELDAS = [%+06.2f, %+06.2f]\n", LONmax, LONmin, dLATcel, dLONcel);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Lista de imagenes ------------------------------------------------------------\n");
	for (h1=0; h1<Cimgs; h1++){
		printf("%s\n", array_imgs[h1]);
	}	
	//printf("---- Vectores Regulares -----------------------------------------------------------\n");
	//printf("LATITUDES:\n");
	//mostrar_vector_double(LATvec, Ci, 10);
	//printf("LONGITUDES:\n");
	//mostrar_vector_double(LONvec, Cj, 10);
	//printf("CALIBRACION:\n");
	//mostrar_vector_int(CALvis_iniYEA, Cste, 10);
	//mostrar_vector_int(CALvis_iniDOY, Cste, 10);
	//mostrar_vector_double(CALvis_Xspace, Cste, 10);
	//mostrar_vector_double(CALvis_M, Cste, 10);
	//mostrar_vector_double(CALvis_K, Cste, 10);
	//mostrar_vector_double(CALvis_alfa, Cste, 10);
	//mostrar_vector_double(CALvis_beta, Cste, 10);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Datos de la imagen -----------------------------------------------------------\n");
	printf("TAG: %d\n", tag);
	printf("-----------------------------------------------------------------------------------\n");

	return 1;
}