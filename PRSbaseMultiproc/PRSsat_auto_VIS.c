#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "lib_PRSsat.h"

#define FALSE   0
#define TRUE    !FALSE
#define CMAXstr 200
#define CINPstr 42
#define CSPTstr 23

// Versión 1.0, 09/2016 -- Rodrigo Alonso Suárez.

int main(int argc, char *argv[]){

	FILE * data;
	char PATHimg[CMAXstr];
	char RUTAent[CMAXstr];
	char RUTAsal[CMAXstr];
	char RUTAcal[CMAXstr];
	char Filename[CMAXstr];
	char imgs[CINPstr];
	char CODEspatial[CSPTstr];
	int	 Ci, Cj, Ct, tag, OK;
	double	LATmax, LATmin, LONmax, LONmin, dLATgri, dLONgri, dLATcel, dLONcel;
	int * MSKmat;
	int * CNT1mat;
	int * CNT2mat;
	double * FRmat;
	double * LATmat; double * LONmat;
	double * LATvec; double * LONvec;
	int      CALvis_iniYEA; int CALvis_iniDOY;
	double   CALvis_Xspace;
	double   CALvis_M;
	double   CALvis_K;
	double   CALvis_alfa;
	double   CALvis_beta;

	// printf("PRSsat_auto_VIS running, num param: %d\n", argc);

	// IMAGEN A PROCESAR
	strncpy(RUTAent,  argv[1], CMAXstr);
	strncpy(RUTAsal,  argv[2], CMAXstr);
	strncpy(Filename, argv[3], CMAXstr);

	LATmax        = atof(argv[4]);
	LATmin        = atof(argv[5]);
	LONmax        = atof(argv[6]);
	LONmin        = atof(argv[7]);
	dLATgri       = atof(argv[8]);
	dLONgri       = atof(argv[9]);
	dLATcel       = atof(argv[10]);
	dLONcel       = atof(argv[11]);

  Ci            = atoi(argv[12]);
  Cj            = atoi(argv[13]);
  Ct            = atoi(argv[14]);

	strncpy(CODEspatial, argv[15], CSPTstr); CODEspatial[CSPTstr] = '\0';

	CALvis_iniYEA = atoi(argv[16]);
	CALvis_iniDOY = atoi(argv[17]);

	CALvis_Xspace = atof(argv[18]);
	CALvis_M      = atof(argv[19]);
	CALvis_K      = atof(argv[20]);
	CALvis_alfa   = atof(argv[21]);
	CALvis_beta   = atof(argv[22]);

	// INIT
	OK = 0;

	// RUTA DE SALIDA
	// strcat(RUTAsal, CODEspatial); strcat(RUTAsal, "/");

	// INFORMACION DE LOS ARCHIVOS CARGADOS
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Archivos y Rutas -------------------------------------------------------------\n");
	printf("FILENAME: %s\n", &Filename[0]);
	printf("RUTAent:  %s\n", &RUTAent[0]);
	printf("RUTAsal:  %s\n", &RUTAsal[0]);
	printf("CODIGO :  %s\n", &CODEspatial[0]);
	printf("-----------------------------------------------------------------------------------\n");
	printf("---- Resolucion Espacial ----------------------------------------------------------\n");
	printf("LAT = [%+07.3f .. %+07.3f] --- GRILLA = [%+07.3f, %+07.3f]\n", LATmax, LATmin, dLATgri, dLONgri);
	printf("LON = [%+07.3f .. %+07.3f] --- CELDAS = [%+07.3f, %+07.3f]\n", LONmax, LONmin, dLATcel, dLONcel);
	printf("-----------------------------------------------------------------------------------\n");

	printf("-----------------------------------------------------------------------------------\n");	
	printf("---- Imagenes procesadas ----------------------------------------------------------\n");

	// RUTA A LA IMAGEN
	strncpy(PATHimg, RUTAent, CMAXstr); // copio en PATHimg la ruta
	strcat(PATHimg, Filename);          // agrego al final de PATHimg el nombre del archivo

	printf("PATHimg :  %s\n", &PATHimg[0]);

	// PROCESO IMAGEN
	OK = procesar_NetCDF_VIS_gri(&FRmat, &MSKmat, &CNT1mat, &CNT2mat, &tag,
   		dLATgri, dLONgri, dLATcel, dLONcel, LATmax, LATmin, LONmax, LONmin,
   		Ct, Ci, Cj, PATHimg, RUTAsal, 
   		CALvis_iniYEA, CALvis_iniDOY, CALvis_Xspace,
  		CALvis_M, CALvis_K, CALvis_alfa, CALvis_beta);

	// SI NO SE USA, BORRO
	free(FRmat); free(MSKmat); free(CNT1mat); free(CNT2mat);

	// FINAL IMAGEN
	printf("IMAGEN : %s. TAG = [%d]. OK = [%d].\n", &PATHimg[0], tag, OK);

	printf("-----------------------------------------------------------------------------------\n");

	return 1;
}
