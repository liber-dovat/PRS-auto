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

// Versión 1.0, 10/2016 -- Rodrigo Alonso Suárez.

int procesar_imagen_VIS(double * FRmat, double * RPmat, int * MSKmat,
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

		// SI EL PIXEL ESTÁ EN LA VENTANA A CONSIDERAR
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

	return 0;
}

int procesar_NetCDF_VIS(double * FRmat, double * RPmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj, char PATH[CMAXstr]){

	int		h1, Si, Sj, St, Band, Date, Time, yea, doy, hra, min, ste;
	int		nc_status, ncid, id_lat, id_lon, id_data, id_band, id_date, id_time;
	size_t	xi, xj;
	size_t start_data[] = {0,0,0}; // Formato {banda, isI, isJ}
	size_t count_data[] = {1,0,0}; // Formato {banda, isI, isJ} ¡El '1' es muy importante!
	size_t start_geo[] = {0,0}; // Formato {isI, isJ}
	size_t count_geo[] = {0,0}; // Formato {isI, isJ}
	char * str2token;
	char FileName[CFLNstr];
	char strSTE[1];
	char * token;
	int * BAND;
	int * DATE;
	int * TIME;
	int * BXdata;
	double * LATdata;
	double * LONdata;

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
	Si = (int) xi; // cast de size_y a int
	Sj = (int) xj; // cast de size_y a int
	St = Si*Sj;
	count_geo[0] = Si;
	count_geo[1] = Sj;
	count_data[1] = Si;
	count_data[2] = Sj;

	// ALOCAR MEMORIA para imagenes
	if (!(BAND = (int *) malloc(1 * sizeof(int *)))){return 0;}
	if (!(TIME = (int *) malloc(10 * sizeof(int *)))){return 0;}
	if (!(DATE = (int *) malloc(10 * sizeof(int *)))){return 0;}
	if (!(BXdata = (int *) malloc(St * sizeof(int *)))){return 0;}
	if (!(LATdata = (double *) malloc(St * sizeof(double *)))){return 0;}
	if (!(LONdata = (double *) malloc(St * sizeof(double *)))){return 0;}
	if (!(str2token = (char *) malloc(CMAXstr * sizeof(char *)))){return 0;}

	// OBTENGO DATOS DE LA IMAGEN
	nc_status = nc_get_vara_int(ncid, id_data, start_data, count_data, BXdata);
	nc_status = nc_get_vara_double(ncid, id_lat, start_geo, count_geo, LATdata);
	nc_status = nc_get_vara_double(ncid, id_lon, start_geo, count_geo, LONdata);
	nc_status = nc_get_var_int(ncid, id_band, BAND);
	nc_status = nc_get_var_int(ncid, id_date, DATE);
	nc_status = nc_get_var_int(ncid, id_time, TIME);
	if (nc_status != NC_NOERR){printf("No se pudo obtener lons. Cerrando.\n"); return 0;}
	
	// CIERRO LA IMAGEN!
	nc_close(ncid);

	// DATOS VARIOS NECESARIOS
	Band = (int) BAND[0]; // cast de int * a int
	Date = (int) DATE[0]; // cast de int * a int
	Time = (int) TIME[0]; // cast de int * a int
	yea = (int) ((Date/1000)%10) + 10*((Date/10000)%10) + 100*((Date/100000)%10) + 1000*((Date/1000000)%10);
	doy = (int) Date%10 + 10*((Date/10)%10) + 100*((Date/100)%10);
	hra = (int) ((Time/10000)%10) + 10*((Time/100000)%10);
	min = (int) ((Time/100)%10) + 10*((Time/1000)%10);

	printf("[%d, %d]\n", Si, Sj);

	// NOMBRE DE ARCHIVO y SATELITE
	strncpy(str2token, PATH, CMAXstr);
	while ((token = strsep(&str2token, "/"))){
		strncpy(FileName, token, CFLNstr);
	}
	strncpy(strSTE, FileName+4, 2);
	ste = atoi(strSTE); // SATELITE
	
	// PROCESAR LA IMAGEN
	if (Band == 1){ // CANAL VISIBLE, PROCESO
		printf("%s\n", FileName);
		procesar_imagen_VIS(&FRmat[0], &RPmat[0], &MSKmat[0], &CNT1mat[0], &CNT2mat[0],
			dLATgri, dLONgri, dLATcel, dLONcel,
			LATmax, LATmin, LONmax, LONmin,
			Ct, Ci, Cj, &BXdata[0], &LATdata[0], &LONdata[0], St);
		return 1;
	}
	return 0;
}

int mostrar_vector_double(double * vec, int cvec, int cmax){

	int		h1, h2;
	
	h2 = 1;
	for (h1 = 0; h1 < cvec; h1++){
		if (h2==cmax){
			printf("%+06.2f\n", vec[h1]); h2=1;
		}else{
			printf("%+06.2f  ", vec[h1]); h2=h2+1;
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
