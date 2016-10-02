#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <netcdf.h>

#define CMAXstr 200
#define CFLNstr 34
#define PI 3.1415926
#define FALSE 0
#define TRUE !FALSE
#define coszTHR 0.05
#define n1THR 0.465
#define Rmin 0.06
#define Rmax 0.465
#define Ccods 1200
#define Cste 3

// SATELITES
static int GOES[Cste]={8,12,13};

// Versión 1.0, 10/2016 -- Rodrigo Alonso Suárez.

int procesar_NetCDF_VIS_gri(double ** FRmat, double ** RPmat, double ** N1mat,
	int ** MSKmat, int ** CNT1mat, int ** CNT2mat,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj, char PATH[CMAXstr]){

	int		h1, Si, Sj, St, Band, yea, doy, hra, min, ste;
	char FileName[CFLNstr];
	int * BXdata;
	double * LATdata;
	double * LONdata;

	open_NetCDF_file(PATH, &BXdata, &LATdata, &LONdata,
		&Si, &Sj, &St, &Band, &yea, &doy, &hra, &min, &ste, &FileName);

	printf("[%d, %d, %d, %d, %d, %d, %d, %d, %d, %s]\n",
		Si, Sj, St, Band, yea, doy, hra, min, ste, FileName);

	// ALOCO MEMORIA PARA LOS PROCESAMIENTOS
	if (!(*FRmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*RPmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*N1mat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*MSKmat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(*CNT1mat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(*CNT2mat = (int *) malloc(Ct * sizeof(int *)))){return 0;}

	// VACIO DATASETS (inicializo en zero)
	for (h1=0; h1<Ct; h1++){
	 	(*FRmat)[h1] = 0; (*RPmat)[h1] = 0; (*N1mat)[h1] = 0; (*MSKmat)[h1] = 0;
	 	(*CNT1mat)[h1] = 0;
	 	(*CNT2mat)[h1] = 0;
	}

	// PROCESAR LA IMAGEN
	if (Band == 1){ // CANAL VISIBLE, PROCESO
		printf("%s\n", FileName);
		procesar_VIS_gri((*FRmat), (*RPmat), (*MSKmat), (*CNT1mat), (*CNT2mat),
			dLATgri, dLONgri, dLATcel, dLONcel,
			LATmax, LATmin, LONmax, LONmin,
			Ct, Ci, Cj, &BXdata[0], &LATdata[0], &LONdata[0], St);
		return 1;
	}
	return 0;
}

int open_NetCDF_file(char PATH[CMAXstr],
	int ** BXdata, double ** LATdata, double ** LONdata,
	int *Si, int *Sj, int *St, int *Band,
	int *yea, int *doy, int *hra, int *min, int *ste,
	char FileName[CFLNstr]){

	int		Date, Time;
	int		nc_status, ncid, id_lat, id_lon, id_data, id_band, id_date, id_time;
	size_t	xi, xj;
	size_t start_data[] = {0,0,0}; // Formato {banda, isI, isJ}
	size_t count_data[] = {1,0,0}; // Formato {banda, isI, isJ} ¡El '1' es muy importante!
	size_t start_geo[] = {0,0}; // Formato {isI, isJ}
	size_t count_geo[] = {0,0}; // Formato {isI, isJ}
	char * str2token;
	char strSTE[1];
	char * token;
	int * BAND;
	int * DATE;
	int * TIME;

	// ABRO LA IMAGEN
	nc_status = nc_open(PATH, 0, &ncid);
	nc_status = nc_inq_dimlen(ncid, 1, &xi);
	nc_status = nc_inq_dimlen(ncid, 0, &xj);
	nc_status = nc_inq_varid (ncid, "data", &id_data);
	nc_status = nc_inq_varid (ncid, "bands", &id_band);
	nc_status = nc_inq_varid (ncid, "lat", &id_lat);
	nc_status = nc_inq_varid (ncid, "lon", &id_lon);
	nc_status = nc_inq_varid (ncid, "imageDate", &id_date);
	nc_status = nc_inq_varid (ncid, "imageTime", &id_time);
	if (nc_status != NC_NOERR){printf("No se encontro imagen. Cerrando.\n"); return 0;}

	// SIZE DE LA IMAGEN
	*Si = (int) xi; // cast de size_y a int
	*Sj = (int) xj; // cast de size_y a int
	*St = (*Si)*(*Sj);
	count_geo[0] = *Si;
	count_geo[1] = *Sj;
	count_data[1] = *Si;
	count_data[2] = *Sj;

	// ALOCAR MEMORIA para imagenes
	if (!(BAND = (int *) malloc(1 * sizeof(int *)))){return 0;}
	if (!(TIME = (int *) malloc(10 * sizeof(int *)))){return 0;}
	if (!(DATE = (int *) malloc(10 * sizeof(int *)))){return 0;}
	if (!(*BXdata = (int *) malloc(*St * sizeof(int *)))){return 0;}
	if (!(*LATdata = (double *) malloc(*St * sizeof(double *)))){return 0;}
	if (!(*LONdata = (double *) malloc(*St * sizeof(double *)))){return 0;}
	if (!(str2token = (char *) malloc(CMAXstr * sizeof(char *)))){return 0;}

	// OBTENGO DATOS DE LA IMAGEN
	nc_status = nc_get_vara_int(ncid, id_data, start_data, count_data, *BXdata);
	nc_status = nc_get_vara_double(ncid, id_lat, start_geo, count_geo, *LATdata);
	nc_status = nc_get_vara_double(ncid, id_lon, start_geo, count_geo, *LONdata);
	nc_status = nc_get_var_int(ncid, id_band, BAND);
	nc_status = nc_get_var_int(ncid, id_date, DATE);
	nc_status = nc_get_var_int(ncid, id_time, TIME);
	if (nc_status != NC_NOERR){printf("No se pudo obtener lons. Cerrando.\n"); return 0;}
	
	// CIERRO LA IMAGEN!
	nc_close(ncid);

	// DATOS VARIOS NECESARIOS
	*Band = (int) BAND[0]; // cast de int * a int
	Date = (int) DATE[0]; // cast de int * a int
	Time = (int) TIME[0]; // cast de int * a int
	*yea = (int) ((Date/1000)%10) + 10*((Date/10000)%10) + 100*((Date/100000)%10) + 1000*((Date/1000000)%10);
	*doy = (int) Date%10 + 10*((Date/10)%10) + 100*((Date/100)%10);
	*hra = (int) ((Time/10000)%10) + 10*((Time/100000)%10);
	*min = (int) ((Time/100)%10) + 10*((Time/1000)%10);

	// NOMBRE DE ARCHIVO y SATELITE
	strncpy(str2token, PATH, CMAXstr);
	while ((token = strsep(&str2token, "/"))){
		strncpy(FileName, token, CFLNstr);
	}
	strncpy(strSTE, FileName+4, 2);
	*ste = atoi(strSTE); // SATELITE

	return 1;
}

int procesar_VIS_gri(double * FRmat, double * RPmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat, 
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj,
	int * BXdata, double * LATdata, double * LONdata, int St){

	int 	Braw;
	int 	h1, h2;
	int 	m, n, mI, mS, nI, nS;
	double 	lat, latI, latS, hLATcel;
	double 	lon, lonI, lonS, hLONcel;
	double	mId, mSd, nId, nSd;

	hLATcel = dLATcel/2;
	hLONcel = dLONcel/2;

	// RECORRO LA IMAGEN
	for (h1=0;h1<(St);h1++){

		// DATO DE CADA PIXEL
		Braw = BXdata[h1]; lat = LATdata[h1]; lon = LONdata[h1];

		// // SI EL PIXEL ESTÁ EN LA VENTANA A CONSIDERAR
		if ((lat >= (LATmin - hLATcel))&&(lat <= (LATmax + hLATcel))){
			if ((lon >= (LONmin - hLONcel))&&(lon <= (LONmax + hLONcel))){

				// HALLO LIMITES EN LA GRILLA.
				latI = lat - hLATcel;
				latS = lat + hLATcel;
				mId = (latI - LATmin)/dLATgri;
				mSd = (latS - LATmin)/dLATgri;
				mI = (int) (mId + 1);
				mS = (int) (mSd);
				lonI = lon - hLONcel;
				lonS = lon + hLONcel;
				nId = (lonI - LONmin)/dLONgri;
				nSd = (lonS - LONmin)/dLONgri;
				nI = (int) (nId + 1);
				nS = (int) (nSd);
				if (mI < 0){mI = 0;}
				if (mS >= Ci){mS = (Ci-1);}
				if (mSd < 0){mS = -1;}
				if (nI < 0){nI = 0;}
				if (nS >= Cj){nS = (Cj-1);}
				if (nSd < 0){nS = -1;}
				
				// PROCESO EL PIXEL SOLO SI TIENE UBICACION
				// CHEQUEO DE PUNTAS
				if ((mI<=mS)&&(mI<Ci)&&(mS>=0)){
					if ((nI<=nS)&&(nI<Cj)&&(nS>=0)){

						// ACUMULO EN LA CELDA CORRESPONDIENTE
						for (m=mI;m<(mS+1);m++){
							for (n=nI;n<(nS+1);n++){

								// Indice en el array
								h2 = (Ci - 1 - m)*Cj + n;
								FRmat[h2] = FRmat[h2] + Braw;
								CNT1mat[h2] = CNT1mat[h2] + 1;
							}
						}
					}
				}
			}
		}
	}

	// CALCULO DE PROMEDIOS
	for (h1=0;h1<(Ct);h1++){
		if (CNT1mat[h1]>0){
			FRmat[h1] = FRmat[h1]/CNT1mat[h1];
		}
	}

	return 1;
}

int generar_grilla(double ** LATmat, double ** LONmat,
	double ** LATvec, double ** LONvec,
	double LATmax, double LATmin, double LONmax, double LONmin,
	double dLATgri, double dLONgri, int *Ci, int *Cj, int *Ct){

	int 	h1, h2, h3;

	// TAMAÑO DE LA GRILLA ESPACIAL
	*Ci = (int) 1 + (LATmax - LATmin)/dLATgri;
	*Cj = (int) 1 + (LONmax - LONmin)/dLONgri;
	*Ct = (*Ci)*(*Cj);

	if (!(*LATmat = (double *) malloc(*Ct * sizeof(double *)))){return 0;}
	if (!(*LONmat = (double *) malloc(*Ct * sizeof(double *)))){return 0;}
	if (!(*LATvec = (double *) malloc(*Ci * sizeof(double *)))){return 0;}
	if (!(*LONvec = (double *) malloc(*Cj * sizeof(double *)))){return 0;}

	// VECTORES DE LATITUD Y LONGITUD
	for (h1=0; h1 < *Ci; h1++){(*LATvec)[h1] = LATmin + dLATgri*h1;}
	for (h1=0; h1 < *Cj; h1++){(*LONvec)[h1] = LONmin + dLONgri*h1;}

	// MATRICES DE LATITUD Y LONGITUD
	for (h1=0; h1<*Ci; h1++){
		for (h2=0; h2<*Cj; h2++){
			h3 = (*Ci - 1 - h1)*(*Cj) + h2;
			(*LATmat)[h3] = (*LATvec)[h1];
			(*LONmat)[h3] = (*LONvec)[h2];
		}
	}
	return 1;
}

int cargar_calibracion_VIS(char RUTAcal[CMAXstr],
	int ** CALvis_iniYEA, int ** CALvis_iniDOY,
	double ** CALvis_Xspace, double ** CALvis_M, double ** CALvis_K,
	double ** CALvis_alfa, double ** CALvis_beta){

	FILE * data;
	char PATHpre[CMAXstr];
	char PATHpos[CMAXstr];
	char STRste[2];
	int     h1, ste, iniYEA, iniDOY, ARCHste;
	double	M, Xspace, alfa, beta, K;

	// ALOCAR MEMORIA REQUERIDA
	if (!(*CALvis_iniYEA = (int *) malloc(Cste * sizeof(int *)))){return 0;}
	if (!(*CALvis_iniDOY = (int *) malloc(Cste * sizeof(int *)))){return 0;}
	if (!(*CALvis_Xspace = (double *) malloc(Cste * sizeof(double *)))){return 0;}
	if (!(*CALvis_M = (double *) malloc(Cste * sizeof(double *)))){return 0;}
	if (!(*CALvis_K = (double *) malloc(Cste * sizeof(double *)))){return 0;}
	if (!(*CALvis_alfa = (double *) malloc(Cste * sizeof(double *)))){return 0;}
	if (!(*CALvis_beta = (double *) malloc(Cste * sizeof(double *)))){return 0;}
	
	// CARGO ARCHIVOS
	for (h1 = 0; h1 < Cste; h1++){
		
		// RUTAS A LOS ARCHIVOS PRE-LAUNCH y POST-LAUNCH
		ste = GOES[h1];
		if (ste < 10){sprintf(STRste, "0%d", ste);}else{sprintf(STRste, "%d", ste);}
		strcpy(PATHpre, RUTAcal); strcat(PATHpre, "B01_GOES"); strcat(PATHpre, STRste); strcat(PATHpre, "pre");
		strcpy(PATHpos, RUTAcal); strcat(PATHpos, "B01_GOES"); strcat(PATHpos, STRste); strcat(PATHpos, "pos");

		// DATA CALIBRACION PRE-LAUNCH, cierro ejecucion si no se encuentra
		data = fopen(PATHpre, "ro");
		if (data == NULL) {printf("No se encontro archivo de calibracion PRE. Cerrando.\n"); return 0;}
		fscanf(data, "%d\n",  &ARCHste);
		fscanf(data, "%lf\n", &M);
		fscanf(data, "%lf\n", &Xspace);
		fscanf(data, "%lf\n", &K);
		fclose(data);
		if (ARCHste != ste){printf("No se pudo verificar el CHK PRE. Cerrando.\n"); return 0;}

		// DATA CALIBRACION POS-LAUNCH, cierro ejecucion si no se encuentra
		data = fopen(PATHpos, "ro");
		if (data == NULL) {printf("No se encontro archivo de calibracion POS. Cerrando.\n"); return 0;}
		fscanf(data, "%d\n", &ARCHste);
		fscanf(data, "%d %d\n", &iniYEA, &iniDOY);
		fscanf(data, "%lf\n", &alfa);
		fscanf(data, "%lf\n", &beta);
		fclose(data);
		if (ARCHste != ste){printf("No se pudo verificar el CHK POS. Cerrando.\n"); return 0;}

		// ASIGNO DATOS DE CALIBRACION
		(*CALvis_iniYEA)[h1] = iniYEA;
		(*CALvis_iniDOY)[h1] = iniDOY;
		(*CALvis_Xspace)[h1] = Xspace;
		(*CALvis_M)[h1] = M;
		(*CALvis_K)[h1] = K;
		(*CALvis_alfa)[h1] = alfa;
		(*CALvis_beta)[h1] = beta;
	}

}

int mostrar_vector_double(double * vec, int cvec, int cmax){

	int		h1, h2;
	
	h2 = 1;
	for (h1 = 0; h1 < cvec; h1++){
		if (h2==cmax){
			printf("%+06.2f\n", vec[h1]); h2=1;
		}else{
			printf("%+06.2f\t", vec[h1]); h2=h2+1;
		}
	}
	if (h2 > 1){printf("\n");}
	
	// FIN
	return 1;
}

int mostrar_vector_int(int * vec, int cvec, int cmax){

	int		h1, h2;
	
	h2 = 1;
	for (h1 = 0; h1 < cvec; h1++){
		if (h2==cmax){
			printf("%d\n", vec[h1]); h2=1;
		}else{
			printf("%d  ", vec[h1]); h2=h2+1;
		}
	}
	if (h2 > 1){printf("\n");}
	
	// FIN
	return 1;
}
