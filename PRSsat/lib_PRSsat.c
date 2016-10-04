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
#define Cste 3
#define celMIN 0.5
#define imgTHR1 1.00
#define imgTHR2 0.99
#define imgTHR3 0.85
#define imgTHR4 0.30
//#define Ccods 1200
//#define coszTHR 0.05
//#define n1THR 0.465
//#define Rmin 0.06
//#define Rmax 0.465

// SATELITES
static int GOES[Cste]={8,12,13};

// Versión 1.0, 10/2016 -- Rodrigo Alonso Suárez.

int procesar_NetCDF_VIS_gri(double ** FRmat, double ** RPmat, double ** N1mat,
	double ** CZmat, int ** MSKmat, int ** CNT1mat, int ** CNT2mat, int *tag,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj, char PATH[CMAXstr], char RUTAsal[CMAXstr],
	int * CALvis_iniYEA, int * CALvis_iniDOY, double * CALvis_Xspace,
	double * CALvis_M, double * CALvis_K, double * CALvis_alfa, double * CALvis_beta){

	int		h1, Si, Sj, St, Band, yea, doy, hra, min, sec, ste, kste;
	double	Fn, DELTArad, EcTmin, fracMK;
	char FileName[CFLNstr];
	int * BXdata;
	double * LATdata;
	double * LONdata;

	*tag = 0;

	open_NetCDF_file(PATH, &BXdata, &LATdata, &LONdata,
		&Si, &Sj, &St, &Band, &yea, &doy, &hra, &min, &sec, &ste, &FileName);

	printf("IMAGEN = %s :: [%d, %d] = %d :: Banda = [%d] :: Fecha = [%d-%d] :: Hora = [%d%d-%ds] :: Satelite = [GOES%d]\n",
		FileName, Si, Sj, St, Band, yea, doy, hra, min, sec, ste);

	// ALOCO MEMORIA PARA LOS PROCESAMIENTOS
	if (!(*FRmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*RPmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*N1mat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*CZmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*MSKmat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(*CNT1mat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(*CNT2mat = (int *) malloc(Ct * sizeof(int *)))){return 0;}

	// VACIO DATASETS (inicializo en zero)
	for (h1=0; h1<Ct; h1++){
	 	(*FRmat)[h1] = 0; (*RPmat)[h1] = 0; (*N1mat)[h1] = 0;
		(*CZmat)[h1] = 0;
	 	(*MSKmat)[h1] = 0;
	 	(*CNT1mat)[h1] = 0;
	 	(*CNT2mat)[h1] = 0;
	}

	// PROCESAR LA IMAGEN
	if (Band == 1){ // CANAL VISIBLE, PROCESO
		
		// Elijo satelite para calibracion
		if (ste == 8){ kste=0;}
		if (ste == 12){kste=1;}
		if (ste == 13){kste=2;}

		// calculo solar diario
		calculo_solar_diario(yea, doy, &Fn, &DELTArad, &EcTmin);

		// proceso imagen
		procesar_VIS_gri((*FRmat), (*RPmat), (*CZmat),
			(*MSKmat), (*CNT1mat), (*CNT2mat), &*tag, &fracMK,
			dLATgri, dLONgri, dLATcel, dLONcel,
			LATmax, LATmin, LONmax, LONmin,
			Ct, Ci, Cj, &BXdata[0], &LATdata[0], &LONdata[0], St,
			CALvis_iniYEA[kste], CALvis_iniDOY[kste], CALvis_Xspace[kste],
			CALvis_M[kste], CALvis_K[kste], CALvis_alfa[kste], CALvis_beta[kste],
			Fn, DELTArad, EcTmin, yea, doy, hra, min, sec);

		calcular_nubosidad_GL((*RPmat), (*N1mat), Ct);

		// GUARDAR IMAGEN
		guardar_imagen_VIS(RUTAsal, Ct, yea, doy, hra, min, sec, 
			(*FRmat), (*RPmat), (*N1mat), (*MSKmat), *tag, fracMK);

		// GUARDAR IMAGEN TEST
		guardar_imagen_double(RUTAsal, Ct, yea, doy, hra, min, sec,
			(*CZmat), "CZ");
		guardar_imagen_int(RUTAsal, Ct, yea, doy, hra, min, sec,
			(*CNT1mat), "C1");

		return 1;
	}

	// LIBERO MEMORIA
	free(BXdata); free(LATdata); free(LONdata);

	return 0;
}

int open_NetCDF_file(char PATH[CMAXstr],
	int ** BXdata, double ** LATdata, double ** LONdata,
	int *Si, int *Sj, int *St, int *Band,
	int *yea, int *doy, int *hra, int *min, int *sec, int *ste,
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
	*sec = (int) (Time%10) + 10*((Time/10)%10);

	// NOMBRE DE ARCHIVO y SATELITE
	strncpy(str2token, PATH, CMAXstr);
	while ((token = strsep(&str2token, "/"))){
		strncpy(FileName, token, CFLNstr);
	}
	strncpy(strSTE, FileName+4, 2);
	*ste = atoi(strSTE); // SATELITE

	return 1;
}

int procesar_VIS_gri(double * FRmat, double * RPmat, double * CZmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat, int *tag, double *fracMK,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj,
	int * BXdata, double * LATdata, double * LONdata, int St,
	int CALvis_iniYEA, int CALvis_iniDOY, double CALvis_Xspace,
	double CALvis_M, double CALvis_K, double CALvis_alfa, double CALvis_beta,
	double Fn, double DELTArad, double EcTmin,
	int yea, int doy, int hra, int min, int sec){

	int 	Braw;
	int 	h1, h2, N, mk, sumaMK, cnt1, cnt2;
	int 	m, n, mI, mS, nI, nS;
	double 	lat, latI, latS, hLATcel;
	double 	lon, lonI, lonS, hLONcel;
	double	mId, mSd, nId, nSd;
	double 	cosz, fc, ls, fr, rp, frac;

	// INCREMENTOS SOBRE DOS
	hLATcel = dLATcel/2;
	hLONcel = dLONcel/2;

	// FACTOR POST-LAUNCH fc
	nDESDEfecha(CALvis_iniYEA, CALvis_iniDOY, yea, doy, &N);
	fc = (CALvis_alfa*N/1000) + CALvis_beta;

	//printf("%d %d %6.2f %6.2f %6.2f %6.2f %6.2f %8.4f %8.4f %8.4f %8.4f\n",
	//	CALvis_iniYEA, CALvis_iniDOY, CALvis_Xspace,
	//	CALvis_M, CALvis_K, CALvis_alfa, CALvis_beta,
	//	Fn, DELTArad, EcTmin, fc);

	// RECORRO LA IMAGEN
	for (h1=0;h1<(St);h1++){

		// DATO DE CADA PIXEL
		Braw = BXdata[h1]; lat = LATdata[h1]; lon = LONdata[h1];
		ls = 0; fr = 0; rp = 0; mk = 0;

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

						// COSENO DEL ANGULO CENITAL
						cosz = 0;
						calculo_cosz_INS(DELTArad, EcTmin, hra, min, sec, lat, lon, &cosz);
						if (cosz < 0){cosz=0;}

						// CALCULO DE PRODUCTOS
						if (Braw > 0){
							calculo_productos_VIS(Braw, cosz, Fn, fc, 
								CALvis_Xspace, CALvis_M, CALvis_K, &fr, &rp);
							mk = 1;
						}

						// ACUMULO EN LA CELDA CORRESPONDIENTE
						for (m=mI;m<(mS+1);m++){
							for (n=nI;n<(nS+1);n++){
								h2 = (Ci - 1 - m)*Cj + n;
								if (mk == 1){
									FRmat[h2] = FRmat[h2] + fr;
									RPmat[h2] = RPmat[h2] + rp;
									CZmat[h2] = CZmat[h2] + cosz;
									CNT1mat[h2] = CNT1mat[h2] + 1;
								}
								CNT2mat[h2] = CNT2mat[h2] + 1;
							}
						}
					}
				}
			}
		}
	}

	// CALCULO DE PROMEDIOS y FLAGS
	sumaMK = 0;
	for (h1=0;h1<(Ct);h1++){
		frac = 0;
		cnt1 = CNT1mat[h1];
		cnt2 = CNT2mat[h1];
		if (cnt1>0){
			FRmat[h1] = FRmat[h1]/cnt1;
			RPmat[h1] = RPmat[h1]/cnt1;
			CZmat[h1] = CZmat[h1]/cnt1;
		}
		if (cnt2>0){
			frac = cnt1/cnt2;
		}
		if (frac >= celMIN){
			MSKmat[h1] = 1; // cero por defecto
		}
		sumaMK = sumaMK + MSKmat[h1]; // Calcular sumatoria de MK[i]
	}

	// ASIGNACION DE BANDERA = {0 img no OK, 1 img OK, 2 img impainting, 3 img mal}
	*tag = 0;
	*fracMK = (double) sumaMK / (double) Ct; // calcular el cociente ZMK / Ct = cociente
	if (*fracMK == imgTHR1){*tag = 1;}
	if ((*fracMK < imgTHR1)&&(*fracMK >= imgTHR2)){*tag = 2;}
	if ((*fracMK < imgTHR2)&&(*fracMK >= imgTHR3)){*tag = 3;}
	if ((*fracMK < imgTHR3)&&(*fracMK >= imgTHR4)){*tag = 4;}
	if ((*fracMK < imgTHR4)){*tag = 5;}

	return 1;
}

int calcular_nubosidad_GL(double * RPmat, double * N1mat, int Ct){

	int 	h1;
	double 	Rmax, Rmin, rp, n1;

	Rmax = 0.465;
	Rmin = 0.060;

	for (h1=0;h1<(Ct);h1++){
		rp = RPmat[h1]/100; // De porcentaje a un valor entre [0, 1]
		n1 = (rp - Rmin)/(Rmax - Rmin);
		if (rp < Rmin){n1 = 0;};
		if (rp > Rmax){n1 = 1;};
		N1mat[h1] = n1;
	}
}

int calculo_productos_VIS(int Braw, double cosz, double Fn, double fc,
	double CALvis_Xspace, double CALvis_M, double CALvis_K,
	double *fr, double *rp){
			
	double 	ls;

	ls = (double) ((double) (Braw/32) - CALvis_Xspace)*CALvis_M; // Radiancia pre-launch
	ls = ls * fc; // Radiancia post-launch
	*fr = (ls * CALvis_K)/(10 * Fn); // (x100) - En porcentaje. (/1000) - Parámetro K expresado por mil.
	if (*fr > 100){*fr = 100;}
	if (*fr < 0){*fr = 0;}
	*rp = *fr / cosz;
	if (*rp > 100){*rp = 100;};
	if (*rp < 0){*rp = 0;};
	
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
	return 1;
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
	
	return 1;
}

int calculo_solar_diario(int yea, int doy, double *Fn, double *DELTArad, double *EcTmin){

	double gam;

	gam = 2*PI*(doy - 1)/365;
	if (is_leap_year(yea) == 1){
		gam = 2*PI*(doy - 1)/366;
	}
	
	*DELTArad = 0.006918 - 0.399912*cos(gam) + 0.070257*sin(gam) - 0.006758*cos(2*gam) + 0.000907*sin(2*gam) - 0.002697*cos(3*gam) + 0.001480*sin(3*gam);
	*Fn = 1.000110 + 0.034221*cos(gam) + 0.001280*sin(gam) + 0.000719*cos(2*gam) + 0.000077*sin(2*gam);
	*EcTmin = 229.2*(0.000075 + 0.001868*cos(gam) - 0.032077*sin(gam) - 0.014615*cos(2*gam) - 0.04089*sin(2*gam));

	return 1;
}

int is_leap_year(int yea){

	int p, q, r;
	
	p = yea % 4; q = yea % 100; r = yea % 400;
	if ((p == 0)&&((q != 0)||(r == 0))){return 1;}else{return 0;}
}

int calculo_cosz_INS(double DELTArad, double EcTmin, int horaUTC, int minu, int sec, double LATdeg, double LONdeg, double *cosz){

	double hsol, Wrad, LATrad;

	LATrad = PI*LATdeg/180;
	hsol = horaUTC + (EcTmin + 4*LONdeg + minu + (sec/60))/60; // LONdeg negativo
	Wrad = (hsol-12)*PI/12;
	*cosz = sin(LATrad)*sin(DELTArad) + cos(LATrad)*cos(DELTArad)*cos(Wrad);

	return 1;
}

int nDESDEfecha(int iniYEA, int iniDOY, int finYEA, int finDOY, int *N){

	int			p, q, r, h1, dias_yea;

	*N = 0;

	// Si sólo tengo una año de diferencia
	if (iniYEA == finYEA){
	    *N = finDOY - iniDOY + 1;
	}else{
    	for (h1=iniYEA;h1<(finYEA+1);h1++){
        
        	// Defino si el año es bisiesto o no, y su cantidad de días
			dias_yea = 365;
        	if (is_leap_year(h1) == 1){dias_yea = 366;}
        
	        //Contamos los días
        	if (h1 == iniYEA){*N = dias_yea - iniDOY + 1;}
        	else{
            	if (h1 == finYEA){*N = *N + finDOY;}
            	else{*N = *N + dias_yea;}
			}
		}
	}
	*N = *N - 1;
}

int guardar_grilla(char RUTAsal[CMAXstr], int Ci, int Cj, int Ct,
	double PSIlat, double dLATgri, double PSIlon, double dLONgri,
	double * LATvec, double * LONvec, double * LATmat, double * LONmat){

	FILE * fid;
	int		h1, Cmeta;
	char RUTAmeta[CMAXstr];
	char RUTA_LATvec[CMAXstr];
	char RUTA_LONvec[CMAXstr];
	char RUTA_LATmat[CMAXstr];
	char RUTA_LONmat[CMAXstr];
	float * SAVE_META;
	float * SAVE_LATvec;
	float * SAVE_LONvec;
	float * SAVE_LATmat;
	float * SAVE_LONmat;

	Cmeta = 6;

	if (!(SAVE_META = (float *) malloc(Cmeta * sizeof(float *)))){return 0;}
	if (!(SAVE_LATvec = (float *) malloc(Ci * sizeof(float *)))){return 0;}
	if (!(SAVE_LONvec = (float *) malloc(Cj * sizeof(float *)))){return 0;}
	if (!(SAVE_LATmat = (float *) malloc(Ct * sizeof(float *)))){return 0;}
	if (!(SAVE_LONmat = (float *) malloc(Ct * sizeof(float *)))){return 0;}

	// ARMAR DATASETS A GUARDAR
	for (h1=0;h1<(Ci);h1++){
		SAVE_LATvec[h1] = (float) (LATvec[h1]); // SE HACE PARA GUARDAR UN FLOAT
	}
	for (h1=0;h1<(Cj);h1++){
		SAVE_LONvec[h1] = (float) (LONvec[h1]); // SE HACE PARA GUARDAR UN FLOAT
	}
	for (h1=0;h1<(Ct);h1++){
		SAVE_LATmat[h1] = (float) (LATmat[h1]); // SE HACE PARA GUARDAR UN FLOAT
	}
	for (h1=0;h1<(Ct);h1++){
		SAVE_LONmat[h1] = (float) (LONmat[h1]); // SE HACE PARA GUARDAR UN FLOAT
	}
	SAVE_META[0] = (float) (Ci);
	SAVE_META[1] = (float) (Cj);
	SAVE_META[2] = (float) (PSIlat);
	SAVE_META[3] = (float) (dLATgri);
	SAVE_META[4] = (float) (PSIlon);
	SAVE_META[5] = (float) (dLONgri);

//[O]
	printf("[%d] :: [%d] :: [%2.5f] :: [%2.5f] :: [%2.5f] :: [%2.5f]\n", Ci, Cj, PSIlat, dLATgri, PSIlon, dLONgri);

	// RUTAS
	strcpy(RUTAmeta, RUTAsal); strcat(RUTAmeta, "meta/T000gri.META");
	strcpy(RUTA_LATvec, RUTAsal); strcat(RUTA_LATvec, "meta/T000gri.LATvec");
	strcpy(RUTA_LONvec, RUTAsal); strcat(RUTA_LONvec, "meta/T000gri.LONvec");
	strcpy(RUTA_LATmat, RUTAsal); strcat(RUTA_LATmat, "meta/T000gri.LATmat");
	strcpy(RUTA_LONmat, RUTAsal); strcat(RUTA_LONmat, "meta/T000gri.LONmat");

	printf("%s\n", &RUTAmeta[0]);
	fid = fopen(RUTAmeta, "wb"); fwrite(SAVE_META, sizeof(float), Cmeta, fid); fclose(fid);
	fid = fopen(RUTA_LATvec, "wb"); fwrite(SAVE_LATvec, sizeof(float), Ci, fid); fclose(fid);
	fid = fopen(RUTA_LONvec, "wb"); fwrite(SAVE_LONvec, sizeof(float), Cj, fid); fclose(fid);
	fid = fopen(RUTA_LATmat, "wb"); fwrite(SAVE_LATmat, sizeof(float), Ct, fid); fclose(fid);
	fid = fopen(RUTA_LONmat, "wb"); fwrite(SAVE_LONmat, sizeof(float), Ct, fid); fclose(fid);

	// Libero la memoria
	free(SAVE_META);
	free(SAVE_LATvec);
	free(SAVE_LONvec);
	free(SAVE_LATmat);
	free(SAVE_LONmat);

	return 1;
}

int generar_strings_temporales(int yea, int doy, int hra, int min, int sec,
	char strTMP[23], char strYEA[4], char strDOY[3],
	char strHRA[2], char strMIN[2], char strSEC[2]){

    // STRINGS NECESARIOS
    sprintf(strYEA, "%d", yea);
    sprintf(strDOY, "%d", doy);
	if (doy < 10){
		sprintf(strDOY, "00%d", doy);
	}else{
		if (doy < 100){
			sprintf(strDOY, "0%d", doy);
		}
	}
    sprintf(strHRA, "%d", hra);
    if (hra < 10){
		sprintf(strHRA, "0%d", hra);
	}
    sprintf(strMIN, "%d", min);
    if (min < 10){
		sprintf(strMIN, "0%d", min);
	}
    sprintf(strSEC, "%d", sec);
    if (sec < 10){
		sprintf(strSEC, "0%d", sec);
	}

	// CODIGO TEMPORAL
	sprintf(strTMP, "/T000gri_%s%s_%s%s%s", strYEA, strDOY, strHRA, strMIN, strSEC);

	return 1;
}

int guardar_imagen_VIS(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, 
	double * FRmat, double * RPmat, double * N1mat, int * MKmat,
	int tag, double fracMK){

	FILE * fid;
	int		h1;
	char RUTA_MK[CMAXstr];
	char RUTA_FR[CMAXstr];
	char RUTA_RP[CMAXstr];
	char RUTA_N1[CMAXstr];
	char RUTA_TG[CMAXstr];
	char strTAG[35];
	char strTMP[23];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	short * SAVE_MK;
	float * SAVE_FR;
	float * SAVE_RP;
	float * SAVE_N1;

	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

 	// GUARDAR TAG
 	sprintf(strTAG, "%s,%s,%s,%s,%s,%d,%7.5f\n", strYEA, strDOY, strHRA, strMIN, strSEC, tag, fracMK); // escribo en la variable tag el valor que me pasan en tag_value
 	strcpy(RUTA_TG, RUTAsal); strcat(RUTA_TG, "zCRR/TAGs_"); strcat(RUTA_TG, strYEA); strcat(RUTA_TG, ".TG");
 	fid = fopen(RUTA_TG, "ab"); fwrite(strTAG, sizeof(char), strlen(strTAG), fid); fclose(fid);

 	// ARMAR DATASETS A GUARDAR CASTEADO A FLOAT (no DOUBLE)
 	if (!(SAVE_MK = (short *) malloc(Ct * sizeof(short *)))){return 0;}
 	if (!(SAVE_FR = (float *) malloc(Ct * sizeof(float *)))){return 0;}
 	if (!(SAVE_RP = (float *) malloc(Ct * sizeof(float *)))){return 0;}
 	if (!(SAVE_N1 = (float *) malloc(Ct * sizeof(float *)))){return 0;}
 	for (h1=0;h1<(Ct);h1++){
 		SAVE_MK[h1] = (short) (MKmat[h1]); // SE HACE PARA CASTEAR A SHORT
 		SAVE_FR[h1] = (float) (FRmat[h1]); // SE HACE PARA CASTEAR A FLOAT
 		SAVE_RP[h1] = (float) (RPmat[h1]); // SE HACE PARA CASTEAR A FLOAT
 		SAVE_N1[h1] = (float) (N1mat[h1]); // SE HACE PARA CASTEAR A FLOAT
 	}

 	if ((tag == 1)||(tag == 2)||(tag == 3)){
 		// RUTA MK, FR, RP, N1
 		strcpy(RUTA_MK, RUTAsal); strcat(RUTA_MK, "B01-MK/"); strcat(RUTA_MK, strYEA);
 		strcat(RUTA_MK, "/"); strcat(RUTA_MK, strTMP); strcat(RUTA_MK, ".MK");
 		strcpy(RUTA_FR, RUTAsal); strcat(RUTA_FR, "B01-FR/"); strcat(RUTA_FR, strYEA);
 		strcat(RUTA_FR, "/"); strcat(RUTA_FR, strTMP); strcat(RUTA_FR, ".FR");
 		strcpy(RUTA_RP, RUTAsal); strcat(RUTA_RP, "B01-RP/"); strcat(RUTA_RP, strYEA);
 		strcat(RUTA_RP, "/"); strcat(RUTA_RP, strTMP); strcat(RUTA_RP, ".RP");
 		strcpy(RUTA_N1, RUTAsal); strcat(RUTA_N1, "B01-N1/"); strcat(RUTA_N1, strYEA);
 		strcat(RUTA_N1, "/"); strcat(RUTA_N1, strTMP); strcat(RUTA_N1, ".N1");
 		// Guardo!
 		fid = fopen(RUTA_MK, "wb"); fwrite(SAVE_MK, sizeof(short), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_FR, "wb"); fwrite(SAVE_FR, sizeof(float), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_RP, "wb"); fwrite(SAVE_RP, sizeof(float), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_N1, "wb"); fwrite(SAVE_N1, sizeof(float), Ct, fid); fclose(fid);
 	}

 	if ((tag == 3)||(tag == 4)||(tag == 5)){
 		// RUTA MK, FR, RP, N1
 		strcpy(RUTA_MK, RUTAsal); strcat(RUTA_MK, "zIMP/B01-MK/"); strcat(RUTA_MK, strYEA);
 		strcat(RUTA_MK, "/"); strcat(RUTA_MK, strTMP); strcat(RUTA_MK, ".MK");
 		strcpy(RUTA_FR, RUTAsal); strcat(RUTA_FR, "zIMP/B01-FR/"); strcat(RUTA_FR, strYEA);
 		strcat(RUTA_FR, "/"); strcat(RUTA_FR, strTMP); strcat(RUTA_FR, ".FR");
 		strcpy(RUTA_RP, RUTAsal); strcat(RUTA_RP, "zIMP/B01-RP/"); strcat(RUTA_RP, strYEA);
 		strcat(RUTA_RP, "/"); strcat(RUTA_RP, strTMP); strcat(RUTA_RP, ".RP");
 		strcpy(RUTA_N1, RUTAsal); strcat(RUTA_N1, "zIMP/B01-N1/"); strcat(RUTA_N1, strYEA);
 		strcat(RUTA_N1, "/"); strcat(RUTA_N1, strTMP); strcat(RUTA_N1, ".N1");
 		// Guardo!
 		fid = fopen(RUTA_MK, "wb"); fwrite(SAVE_MK, sizeof(short), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_FR, "wb"); fwrite(SAVE_FR, sizeof(float), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_RP, "wb"); fwrite(SAVE_RP, sizeof(float), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_N1, "wb"); fwrite(SAVE_N1, sizeof(float), Ct, fid); fclose(fid);
 	}

 	// Libero memoria
 	free(SAVE_MK);
 	free(SAVE_FR);
 	free(SAVE_RP);
 	free(SAVE_N1);

	// FIN
	return 1;

}

int guardar_imagen_double(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, double * DATA, char * tipo){

	FILE * fid;
	int		h1;
	char RUTA[CMAXstr];
	char strTMP[23];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	float * SAVE;
	
	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

 	// ARMAR DATASETS A GUARDAR CASTEADO A FLOAT (no DOUBLE)
 	if (!(SAVE = (float *) malloc(Ct * sizeof(float *)))){return 0;}
 	for (h1=0;h1<(Ct);h1++){
 		SAVE[h1] = (float) (DATA[h1]); // SE HACE PARA CASTEAR A FLOAT
 	}

	// RUTA MK, FR, RP, N1
	strcpy(RUTA, RUTAsal); strcat(RUTA, "test/");
	strcat(RUTA, strTMP); strcat(RUTA, "."); strcat(RUTA, tipo);
	
	// Guardo!
	fid = fopen(RUTA, "wb"); fwrite(SAVE, sizeof(float), Ct, fid); fclose(fid);

 	free(SAVE);

	// FIN
	return 1;

}

int guardar_imagen_int(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, int * DATA, char * tipo){

	FILE * fid;
	int		h1;
	char RUTA[CMAXstr];
	char strTMP[23];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	short * SAVE;
	
	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

 	// ARMAR DATASETS A GUARDAR CASTEADO A FLOAT (no DOUBLE)
 	if (!(SAVE = (short *) malloc(Ct * sizeof(short *)))){return 0;}
 	for (h1=0;h1<(Ct);h1++){
 		SAVE[h1] = (short) (DATA[h1]); // SE HACE PARA CASTEAR A FLOAT
 	}

	// RUTA MK, FR, RP, N1
	strcpy(RUTA, RUTAsal); strcat(RUTA, "test/");
	strcat(RUTA, strTMP); strcat(RUTA, "."); strcat(RUTA, tipo);
	
	// Guardo!
	fid = fopen(RUTA, "wb"); fwrite(SAVE, sizeof(short), Ct, fid); fclose(fid);

 	free(SAVE);

	// FIN
	return 1;

}