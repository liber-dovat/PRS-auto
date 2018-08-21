#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <netcdf.h>
#include <proj_api.h>

#include "lib_PRS_R.h"

#define FALSE 0
#define TRUE !FALSE
#define Cste 3
#define Cirb 4
#define PI 3.1415926
#define celMIN 0.5
#define imgTHR1 1.00
#define imgTHR2 0.99
#define imgTHR3 0.85
#define imgTHR4 0.30
#define coszTHR 0.10
#define CFLNstr 34
#define COUTstr 18

// SATELITES
static int GOES[Cste]={8,12,13};
static int IRBS[Cirb]={2,3,4,6};

// Versión 1.0, 10/2016 -- Rodrigo Alonso Suárez.

// FORDWARD DECLARATION

int open_NetCDF_file(char PATH[CMAXstr],
	double ** BXdata, double ** LATdata, double ** LONdata,
	int *Si, int *Sj, int *St, int *Band,
	int *yea, int *doy, int *hra, int *min, int *sec, int *ste,
	char FileName[CFLNstr]);

int elegir_satelite_VIS(int *kste, int ste);
int elegir_satelite_IRB(int *k, int ste, int band);
int calculo_solar_diario(int yea, int doy, double *Fn, double *DELTArad, double *EcTmin);
int calcular_nubosidad_GL(double * RPmat, double * N1mat, int Ct);
int calculo_cosz_INS(double DELTArad, double EcTmin, int horaUTC, int minu, int sec, double LATdeg, double LONdeg, double *cosz);
int realizar_promedio(double * SUMA, int * CNT, int Ct);
int enmascarar_por_CZ(double * VAR, double * CZ, int Ct, double thr);
int generar_mascara(int * CNT1, int * CNT2, int Ct, int * MSK, int *sumaMK);
int asignar_tag(double fracMK, int *tag);
int guardar_tag(char RUTAsal[CMAXstr], char strTMP[COUTstr], char strYEA[4], char strDOY[3], char strHRA[2],
	char strMIN[2], char strSEC[2], char strBANDA[2], int tag, double fracMK);
int is_leap_year(int yea);

int procesar_VIS_gri(double * FRmat, double * RPmat, double * CZmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat, int *tag, double *fracMK,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj,
	double * BXdata, double * LATdata, double * LONdata, int St,
	double Fn, double DELTArad, double EcTmin,
	int yea, int doy, int hra, int min, int sec);

int procesar_IRB_gri(double * TXmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat, int *tag, double *fracMK,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj,
	double * BXdata, double * LATdata, double * LONdata, int St);

int guardar_imagen_VIS(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, 
	double * FRmat, double * RPmat, double * N1mat, int * MKmat,
	int tag, double fracMK, int Band);

int guardar_imagen_IRB(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, 
	double * TXmat, int * MKmat, int tag, double fracMK, int Band);

int hallar_limites_en_grilla(int Ci, int Cj, double lat, double lon,
	double dLATgri, double dLONgri, double hLATcel, double hLONcel,
	double LATmin, double LONmin, int *nI, int *nS, int *mI, int *mS);

//#####################

int yisleap(int year){
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
} // yisleap

int getDOY(int mon, int day, int year){
    static const int days[2][13] = {
        {0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334},
        {0, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335}
    };
    int leap = yisleap(year);

    return days[leap][mon] + day;
} // getDOY

//#####################

int procesar_NetCDF_VIS_gri(double ** FRmat, double ** RPmat, double ** N1mat,
	double ** CZmat, int ** MSKmat, int ** CNT1mat, int ** CNT2mat, int *tag,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj, char PATH[CMAXstr], char RUTAsal[CMAXstr]
  /*,
	int * CALvis_iniYEA, int * CALvis_iniDOY, double * CALvis_Xspace,                // chr 01
	double * CALvis_M, double * CALvis_K, double * CALvis_alfa, double * CALvis_beta*/){

	int		h1, Si, Sj, St, Band, yea, doy, hra, min, sec, ste, kste;
	double	Fn, DELTArad, EcTmin, fracMK;
	char FileName[CFLNstr];
	double * BXdata;
	double * LATdata;
	double * LONdata;

	*tag = 0;

	printf("%s\n", "open_NetCDF_file begin");
	if (open_NetCDF_file(PATH, &BXdata, &LATdata, &LONdata,
		&Si, &Sj, &St, &Band, &yea, &doy, &hra, &min, &sec, &ste, &FileName)==0){return 0;}
	printf("%s\n", "open_NetCDF_file end");

	printf("OPENING: %s :: [%04d, %04d] = %09d :: Banda = [%02d] :: Fecha = [%04d-%03d] :: Hora = [%02dhs-%02dmin-%02dsec] :: Satelite = [GOES%02d]\n",
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
	if (Band == 2){ // CANAL VISIBLE ROJO, PROCESO
		
	 	// Elijo satelite para calibracion
	 	elegir_satelite_VIS(&kste, ste);

	 	// calculo solar diario
	 	calculo_solar_diario(yea, doy, &Fn, &DELTArad, &EcTmin);

	 	// proceso imagen
	 	procesar_VIS_gri((*FRmat), (*RPmat), (*CZmat),
	 	 	(*MSKmat), (*CNT1mat), (*CNT2mat), &*tag, &fracMK,
	 	 	dLATgri, dLONgri, dLATcel, dLONcel,
	 	 	LATmax, LATmin, LONmax, LONmin,
	 	 	Ct, Ci, Cj, &BXdata[0], &LATdata[0], &LONdata[0], St,
	 	 	// CALvis_iniYEA[kste], CALvis_iniDOY[kste], CALvis_Xspace[kste], // chr 02
	 	 	// CALvis_M[kste], CALvis_K[kste], CALvis_alfa[kste], CALvis_beta[kste],
	 	 	Fn, DELTArad, EcTmin, yea, doy, hra, min, sec);
 		calcular_nubosidad_GL((*RPmat), (*N1mat), Ct);

	 	// GUARDAR IMAGEN
	 	guardar_imagen_VIS(RUTAsal, Ct, yea, doy, hra, min, sec, 
	 	 	(*FRmat), (*RPmat), (*N1mat), (*MSKmat), *tag, fracMK, Band);

	 	// GUARDAR IMAGEN TEST
	 	// guardar_imagen_double(RUTAsal, Ct, yea, doy, hra, min, sec,
	 	//   	(*CZmat), "CZ", Band);
	 	// guardar_imagen_int(RUTAsal, Ct, yea, doy, hra, min, sec,
	 	//   	(*CNT1mat), "C1", Band);

		// LIBERO MEMORIA
		free(BXdata); free(LATdata); free(LONdata);
	 	return 1;
	}

	// LIBERO MEMORIA
	free(BXdata); free(LATdata); free(LONdata);
	return 0;
}

int procesar_NetCDF_IRB_gri(double ** TXmat,
	int ** MSKmat, int ** CNT1mat, int ** CNT2mat, int *tag,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj, char PATH[CMAXstr], char RUTAsal[CMAXstr]
  // ,
	// double * CALirb_m, double * CALirb_n, double * CALirb_a, // chr 03
	// double * CALirb_b1, double * CALirb_b2
  ){

	int		 h1, Si, Sj, St, Band, yea, doy, hra, min, sec, ste, k;
	double 	 fracMK;
	char 	 FileName[CFLNstr];
	double * BXdata;
	double * LATdata;
	double * LONdata;

	*tag = 0;

	printf("%s\n", "open_NetCDF_file begin");
	if(open_NetCDF_file(PATH, &BXdata, &LATdata, &LONdata,
		&Si, &Sj, &St, &Band, &yea, &doy, &hra, &min, &sec, &ste, &FileName)==0){return 0;}
	printf("%s\n", "open_NetCDF_file end");

	printf("OPENING: %s :: [%04d, %04d] = %09d :: Banda = [%02d] :: Fecha = [%04d-%03d] :: Hora = [%02dhs-%02dmin-%02dsec] :: Satelite = [GOES%02d]\n",
		FileName, Si, Sj, St, Band, yea, doy, hra, min, sec, ste);

	// ALOCO MEMORIA PARA LOS PROCESAMIENTOS
	if (!(*TXmat = (double *) malloc(Ct * sizeof(double *)))){return 0;}
	if (!(*MSKmat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(*CNT1mat = (int *) malloc(Ct * sizeof(int *)))){return 0;}
	if (!(*CNT2mat = (int *) malloc(Ct * sizeof(int *)))){return 0;}

	// VACIO DATASETS (inicializo en zero)
	for (h1=0; h1<Ct; h1++){
	 	(*TXmat)[h1] = 0;
	  	(*MSKmat)[h1] = 0;
	  	(*CNT1mat)[h1] = 0;
	  	(*CNT2mat)[h1] = 0;
	}

	// PROCESAR LA IMAGEN
	if (Band > 1){ // CANAL VISIBLE, PROCESO
		
	 	// Elijo satelite para calibracion
	 	elegir_satelite_IRB(&k, ste, Band);

	 	// proceso imagen
	 	procesar_IRB_gri((*TXmat),
	 	  	(*MSKmat), (*CNT1mat), (*CNT2mat), &*tag, &fracMK,
	 	  	dLATgri, dLONgri, dLATcel, dLONcel,
	 	  	LATmax, LATmin, LONmax, LONmin,
	 	  	Ct, Ci, Cj, &BXdata[0], &LATdata[0], &LONdata[0], St
        // ,
	 	  	// CALirb_m[k], CALirb_n[k], CALirb_a[k], // chr 04
	 	  	// CALirb_b1[k], CALirb_b2[k]
        );

	 	// GUARDAR IMAGEN
	 	guardar_imagen_IRB(RUTAsal, Ct, yea, doy, hra, min, sec, 
	 	  	(*TXmat), (*MSKmat), *tag, fracMK, Band);

	 	// // GUARDAR IMAGEN TEST
	 	// guardar_imagen_int(RUTAsal, Ct, yea, doy, hra, min, sec,
	 	//   	(*CNT1mat), "C1", Band);

 		// LIBERO MEMORIA
		free(BXdata); free(LATdata); free(LONdata);
	 	return 1;
	}

	// LIBERO MEMORIA
	free(BXdata); free(LATdata); free(LONdata);
	return 0;
}

int elegir_satelite_VIS(int *kste, int ste){
	
	// Elijo satelite para calibracion
	if (ste == 8){ *kste=0;}
	if (ste == 12){*kste=1;}
	if (ste == 13){*kste=2;}
	return 1;
}

int elegir_satelite_IRB(int *k, int ste, int band){

	int kste, kband;

	if (ste == 8){ kste=0;}
	if (ste == 12){kste=1;}
	if (ste == 13){kste=2;}

	if (band == 2){kband=0;}
	if (band == 3){kband=1;}
	if (band == 4){kband=2;}
	if (band == 6){kband=3;}

	*k = kste*Cirb + kband;
	return 1;
}

int open_NetCDF_file(char PATH[CMAXstr],
	double ** BXdata, double ** LATdata, double ** LONdata,
	int *Si, int *Sj, int *St, int *Band,
	int *yea, int *doy, int *hra, int *min, int *sec, int *ste,
	char FileName[CFLNstr]){

	int     * BXdataTMP;
	double  * Xdata;
	double  * Ydata;
	double  * x_mat;
	double  * y_mat;
	float     x_scale_factor;
	float     y_scale_factor;
  float     data_scale_factor;
	float     x_add_offset;
	float     y_add_offset;
	float     data_add_offset;
	int       Date, Time;
	int       nc_status, ncid, id_x, id_y, id_data, id_band, id_date, id_time, gip_id, sat_h_id, sat_lon_id;
	int       h1, h2, x_len, y_len;
	size_t    xi, xj;
	// size_t    start_data[] = {0,0,0}; // Formato {banda, isI, isJ}
	// size_t    count_data[] = {1,0,0}; // Formato {banda, isI, isJ} ¡El '1' es muy importante!
	size_t    start_data[] = {0,0}; // Formato {banda, isI, isJ}
	size_t    count_data[] = {0,0}; // Formato {banda, isI, isJ} ¡El '1' es muy importante!
	size_t    start_geo[]  = {0}; // Formato {isI}
	size_t    count_geo[]  = {0}; // Formato {isJ}
	size_t    start_time[] = {0}; // Formato {isJ}
	size_t    count_time[] = {0}; // Formato {isJ}
	char      strSTE[1];
	char    * str2token;
	char    * token;
	char    * TimeCoverage;
	int     * BAND;
	int     * DATE;
	int     * TIME;

	printf("%s\n",PATH);

	// ABRO LA IMAGEN
	nc_status = nc_open(PATH, 0, &ncid);
	nc_status = nc_inq_dimlen(ncid, 1, &xi);
	nc_status = nc_inq_dimlen(ncid, 0, &xj);
	nc_status = nc_inq_varid (ncid, "band_id", &id_band);
	nc_status = nc_inq_varid (ncid, "CMI", &id_data);
	nc_status = nc_inq_varid (ncid, "x", &id_x);
	nc_status = nc_inq_varid (ncid, "y", &id_y);
	nc_status = nc_inq_attid (ncid, NC_GLOBAL, "time_coverage_start", &id_date);			      // NC_CHAR = 2
	nc_status = nc_inq_varid (ncid, "goes_imager_projection", &gip_id);
	nc_status = nc_inq_attid (ncid, gip_id, "perspective_point_height", &sat_h_id); 			  // NC_DOUBLE = 6
	nc_status = nc_inq_attid (ncid, gip_id, "longitude_of_projection_origin", &sat_lon_id); // NC_DOUBLE = 6
	if (nc_status != NC_NOERR){printf("No se encontro imagen. Cerrando. Err: %i\n",nc_status); return 0;}

	printf("id_band: %d\n", id_band);
	printf("id_data: %d\n", id_data);
	printf("id_x:    %d\n", id_x);
	printf("id_y:    %d\n", id_y);
	printf("id_date: %d\n", id_date);
	printf("sat_h_id: %d\n", sat_h_id);
	printf("sat_lon_id: %d\n", sat_lon_id);

	// SIZE DE LA IMAGEN: Misterioso por NC
	x_len 			  = (int) xi;
	y_len 			  = (int) xj;
	*Si           = x_len; // cast de size_y a int
	*Sj           = y_len; // cast de size_y a int
	*St           = (*Si)*(*Sj);
	count_geo[0]  = *Si;
	count_geo[1]  = *Sj;
	count_data[0] = *Si;
	count_data[1] = *Sj;

	printf("%i\n", *Si);
	printf("%i\n", *Sj);
	printf("%i\n", *St);

  printf("%s\n", "ALOCAR MEMORIA para imagenes");

	// https://github.com/Unidata/netcdf-c/blob/8de0b3cf3c359f5e859a698a7208aa3fb6f7a1a6/nc_test4/tst_types.c
	// https://github.com/Unidata/netcdf-c/blob/98dd736a40a9ffae67e2ba9d13ae8bd1b38ce3bd/libdispatch/dcopy.c
  // unsigned char * TimeCoverage; // 2018-02-22T17:00:39.2Z
  // https://www.unidata.ucar.edu/software/netcdf/docs/netcdf_8h_source.html // tipos


  // determino el tipo del atributo global "time_coverage_start"
  // nc_type xtypep;
  // nc_inq_atttype(ncid, NC_GLOBAL, "time_coverage_start", &xtypep); // NC_CHAR = 2
 	// printf("xtypep: %d\n", (int)xtypep);

  // nc_type xtypep;
  // nc_inq_vartype(ncid, "x", &xtypep); // NC_CHAR = 2
 	// printf("x type: %d\n", (int)xtypep);

  // calculo el tamaño del atributo global "time_coverage_start"
  size_t len_time = sizeof(size_t);
  nc_inq_attlen(ncid, NC_GLOBAL, "time_coverage_start", &len_time); printf("len_time: %d\n", (int)len_time);
  TimeCoverage = malloc( ((int)len_time) * sizeof(char) );

  double sat_h;
  double sat_lon;
  // sweep_angle_axis = "x" en los GOES-R

	// ALOCAR MEMORIA para imagenes
	if (!(BAND 		  = (int *)    malloc(1       * sizeof(int *))    )){return 0;}
	if (!(TIME 		  = (int *)    malloc(10      * sizeof(int *))    )){return 0;}
	if (!(DATE 		  = (int *)    malloc(10      * sizeof(int *))    )){return 0;}
	if (!(Xdata     = (double *) malloc(*Si     * sizeof(double *)) )){return 0;}
	if (!(Ydata     = (double *) malloc(*Sj     * sizeof(double *)) )){return 0;}
	if (!(BXdataTMP = (int *)    malloc(*St     * sizeof(int *))    )){return 0;}
	if (!(*BXdata   = (double *) malloc(*St     * sizeof(double *)) )){return 0;}
  if (!(str2token = (char *)   malloc(CMAXstr * sizeof(char *))   )){return 0;}

	printf("%s\n", "OBTENGO DATOS DE LA IMAGEN");
	// OBTENGO DATOS DE LA IMAGEN
	nc_status = nc_get_var_int    (ncid, id_band,   BAND); //	printf("BAND: %d\n", *BAND);
	nc_status = nc_get_vara_double(ncid, id_x,      start_geo,  count_geo,  Xdata);
	nc_status = nc_get_vara_double(ncid, id_y,      start_geo,  count_geo,  Ydata);
	nc_status = nc_get_vara_int   (ncid, id_data,   start_data, count_data, BXdataTMP);
	nc_status = nc_get_att_text   (ncid, NC_GLOBAL, "time_coverage_start", TimeCoverage); printf("%s\n", TimeCoverage);
	nc_status = nc_get_att_double (ncid, gip_id,    "perspective_point_height", &sat_h); printf("%f\n", sat_h);
	nc_status = nc_get_att_double (ncid, gip_id,    "longitude_of_projection_origin", &sat_lon); printf("%f\n", sat_lon);

  nc_status = nc_get_att_float  (ncid, id_x,      "scale_factor", &x_scale_factor); printf("x_scale_factor: %f\n", x_scale_factor);
  nc_status = nc_get_att_float  (ncid, id_x,      "add_offset",   &x_add_offset);   printf("x_add_offset: %f\n", x_add_offset);

  nc_status = nc_get_att_float  (ncid, id_y,      "scale_factor", &y_scale_factor); printf("y_scale_factor: %f\n", y_scale_factor);
  nc_status = nc_get_att_float  (ncid, id_y,      "add_offset",   &y_add_offset);   printf("y_add_offset: %f\n", y_add_offset);

  nc_status = nc_get_att_float  (ncid, id_data,      "scale_factor", &data_scale_factor); printf("data_scale_factor: %f\n", data_scale_factor);
  nc_status = nc_get_att_float  (ncid, id_data,      "add_offset",   &data_add_offset);   printf("data_add_offset: %f\n", data_add_offset);
	if (nc_status != NC_NOERR){printf("No se pudo obtener lons. Cerrando. Err: %i\n",nc_status); return 0;}


	for (h1=0; h1<*St; h1++){ // en el canal 13 pej los datos están en Kelvin
	  (*BXdata)[h1] = ( (double)BXdataTMP[h1] * data_scale_factor) + data_add_offset;
	  // printf("%f\n", (*BXdata)[h1] );
	} // for

	// CIERRO LA IMAGEN!
  printf("%s\n", "Cierro el archivo NC");
	nc_close(ncid);

	// https://github.com/blaylockbk/pyBKB_v2/blob/master/BB_goes16/mapping_GOES16_data.ipynb
	// |> https://proj4.org/operations/projections/geos.html?highlight=projection
  // The projection x and y coordinates equals the scanning angle (in radians) multiplied by the satellite height:
  // scanning_angle (radians) = projection_coordinate / h

	if (!(x_mat = malloc(x_len * y_len * sizeof(double)))){return 0;}
	if (!(y_mat = malloc(x_len * y_len * sizeof(double)))){return 0;}

	// Genero las _matrices_ de x e y
	// Desempaqueto los valores de x e y
  printf("%s\n", "Genero las _matrices_ de x e y");
	for (h1=0; h1 < x_len; h1++){
		for (h2=0; h2 < y_len; h2++){
			x_mat[h2 * x_len + h1] = ((Xdata[h1]*x_scale_factor) + x_add_offset) * sat_h;
			y_mat[h2 * x_len + h1] = ((Ydata[h2]*y_scale_factor) + y_add_offset) * sat_h;
		}
	}
  printf("%s\n", "END Genero las _matrices_ de x e y");

	//##################### Operaciones con Lat y Lon

	// ALOCO MEMORIA PARA LAT Y LON
	if (!(*LATdata = (double *) malloc(*St * sizeof(double *)))){return 0;}
	if (!(*LONdata = (double *) malloc(*St * sizeof(double *)))){return 0;}

	// CONVIERTO (x, y) en (lat, lon)
	// https://github.com/OSGeo/proj.4/wiki/ProjAPI

  projPJ pj_geos, pj_latlon;
	char pj_geos_param[CMAXstr];
  char char_sat_h[CMAXstr];
	char char_sat_lon[CMAXstr];

  snprintf(char_sat_h, CMAXstr, "%f", sat_h);
  snprintf(char_sat_lon, CMAXstr, "%f", sat_lon);

	strncpy(pj_geos_param, "", CMAXstr);			        // genero un string vacio
	strcat(pj_geos_param, "+proj=geos +inv +h=");
	strcat(pj_geos_param, char_sat_h);
	strcat(pj_geos_param, " +lon_0=");
	strcat(pj_geos_param, char_sat_lon);

	printf("pj_geos_param: %s\n", pj_geos_param);

  printf("%s\n", "Genero proyecciones");
	if ( !(pj_geos   = pj_init_plus(pj_geos_param)) ){return 0;}
  if ( !(pj_latlon = pj_latlong_from_proj(pj_geos)) ){return 0;}
	
	printf("%s\n", "CONVIERTO (x, y) en (lat, lon)");
	// int log_pj_transform = pj_transform( pj_geos, pj_latlon, *St, 1, x_mat, y_mat, NULL );
	// if (log_pj_transform!=0){ printf("Error log_pj_transform: %d\n", log_pj_transform); return 0;}
	printf("%s\n", "END CONVIERTO (x, y) en (lat, lon)");

	printf("%s\n", "Asigno valores a LATdata y LONdata");
	for (h1=0; h1 < *St; h1++){
		(*LATdata)[h1] = y_mat[h1] * RAD_TO_DEG;
		(*LONdata)[h1] = x_mat[h1] * RAD_TO_DEG;
	  // printf("%17f %17f \n", (*LATdata)[h1], (*LONdata)[h1]);
	}
	printf("%s\n", "END Asigno valores a LATdata y LONdata");

	printf("%s\n", "Libero memoria");
	pj_free(pj_geos);
	pj_free(pj_latlon);
	free(x_mat);
	free(y_mat);
	printf("%s\n", "END Libero memoria");

	//##################### Operaciones con fechas

  printf("%s\n", "Proceso Fechas");

	// 2018-03-01T17:15:41.8Z

	char * yea_str = malloc(5*sizeof(char));
	char * mes_str = malloc(3*sizeof(char));
	char * dia_str = malloc(3*sizeof(char));
	char * hra_str = malloc(3*sizeof(char));
	char * min_str = malloc(3*sizeof(char));
	char * sec_str = malloc(3*sizeof(char));
	printf("%s\n", TimeCoverage);

	//                           ini  cant
	memcpy( yea_str, TimeCoverage,    4 ); yea_str[4] = '\0'; // printf("%s\n", yea_str);
	memcpy( mes_str, TimeCoverage+5,  2 ); mes_str[2] = '\0'; // printf("%s\n", mes_str);
	memcpy( dia_str, TimeCoverage+8,  2 ); dia_str[2] = '\0'; // printf("%s\n", dia_str);
	memcpy( hra_str, TimeCoverage+11, 2 ); hra_str[2] = '\0'; // printf("%s\n", hra_str);
	memcpy( min_str, TimeCoverage+14, 2 ); min_str[2] = '\0'; // printf("%s\n", min_str);
	memcpy( sec_str, TimeCoverage+17, 2 ); sec_str[2] = '\0'; // printf("%s\n", sec_str);

	int day = atoi(dia_str);
	int mes = atoi(mes_str);
	*yea = atoi(yea_str);
	*doy = getDOY(mes, day, *yea);
	*hra = atoi(hra_str);
	*min = atoi(min_str);
	*sec = atoi(sec_str);

	// printf("%d\n", *yea);
	// printf("%d\n", *doy);
	// printf("%d\n", *hra);
	// printf("%d\n", *min);
	// printf("%d\n", *sec);

	// DATOS VARIOS NECESARIOS
	// *Band = (int) BAND[0]; // cast de int * a int
	// Date  = (int) DATE[0]; // cast de int * a int
	// Time  = (int) TIME[0]; // cast de int * a int
	// *yea  = (int) ((Date/1000)%10) + 10*((Date/10000)%10) + 100*((Date/100000)%10) + 1000*((Date/1000000)%10);
	// *doy  = (int) Date%10 + 10*((Date/10)%10) + 100*((Date/100)%10);
	// *hra  = (int) ((Time/10000)%10) + 10*((Time/100000)%10);
	// *min  = (int) ((Time/100)%10) + 10*((Time/1000)%10);
	// *sec  = (int) (Time%10) + 10*((Time/10)%10);

	// NOMBRE DE ARCHIVO y SATELITE
	strncpy(str2token, PATH, CMAXstr);
	while ((token = strsep(&str2token, "/"))){
		strncpy(FileName, token, CFLNstr);
	} // while
	strncpy(strSTE, FileName+4, 2);
	*ste = atoi(strSTE); // SATELITE

	// LIBERO MEMORIA
	free(BAND); free(DATE); free(TIME); free(Xdata); free(Ydata); free(str2token);
  free(yea_str); free(mes_str); free(dia_str); free(hra_str); free(min_str); free(sec_str);

	return 1;
} // open_NetCDF_file

int procesar_VIS_gri(double * FRmat, double * RPmat, double * CZmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat, int *tag, double *fracMK,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj,
	double * BXdata, double * LATdata, double * LONdata, int St,
	// int CALvis_iniYEA, int CALvis_iniDOY, double CALvis_Xspace,
	// double CALvis_M, double CALvis_K, double CALvis_alfa, double CALvis_beta,
	double Fn, double DELTArad, double EcTmin,
	int yea, int doy, int hra, int min, int sec){

	int 	Braw;
	int 	h1, h2, N, mk, sumaMK;
	int 	m, n, mI, mS, nI, nS;
	double 	lat, hLATcel;
	double 	lon, hLONcel;
	double 	cosz, fc, ls, fr, rp;

	// INCREMENTOS SOBRE DOS
	hLATcel = dLATcel/2;
	hLONcel = dLONcel/2;

	// FACTOR POST-LAUNCH fc
	// nDESDEfecha(CALvis_iniYEA, CALvis_iniDOY, yea, doy, &N); // chr 05
	// fc = (CALvis_alfa*N/1000) + CALvis_beta;

	// RECORRO LA IMAGEN
	for (h1=0;h1<(St);h1++){

		// DATO DE CADA PIXEL
		Braw = BXdata[h1]; lat = LATdata[h1]; lon = LONdata[h1];
		ls = 0; fr = 0; rp = 0; mk = 0;

		// // SI EL PIXEL ESTÁ EN LA VENTANA A CONSIDERAR
		if ((lat >= (LATmin - hLATcel))&&(lat <= (LATmax + hLATcel))){
			if ((lon >= (LONmin - hLONcel))&&(lon <= (LONmax + hLONcel))){

				// HALLAR LOS INDICES EN LA MATRIZ
				hallar_limites_en_grilla(Ci, Cj, lat, lon,
					dLATgri, dLONgri, hLATcel, hLONcel, LATmin, LONmin,
					&nI, &nS, &mI, &mS);
				
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
							// calculo_productos_VIS(Braw, cosz, Fn, fc,      // chr 06
							// 	CALvis_Xspace, CALvis_M, CALvis_K, &fr, &rp);
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

	// CALCULO DE PROMEDIOS
	realizar_promedio(FRmat, CNT1mat, Ct);
	realizar_promedio(RPmat, CNT1mat, Ct);
	realizar_promedio(CZmat, CNT1mat, Ct);

	// ENMASCARADOS VARIOS
	sumaMK = 0;
	enmascarar_por_CZ(RPmat, CZmat, Ct, coszTHR);
	enmascarar_por_CZ(FRmat, CZmat, Ct, 0);
	generar_mascara(CNT1mat, CNT2mat, Ct, MSKmat, &sumaMK);

	// ASIGNACION DE TAG
	*fracMK = ((double) sumaMK) / ((double) Ct); // calcular el cociente ZMK / Ct = cociente
	asignar_tag(*fracMK, &*tag);
	return 1;
} // procesar_VIS_gri

int procesar_IRB_gri(double * TXmat, int * MSKmat,
	int * CNT1mat, int * CNT2mat, int *tag, double *fracMK,
	double dLATgri, double dLONgri, double dLATcel, double dLONcel,
	double LATmax, double LATmin, double LONmax, double LONmin,
	int Ct, int Ci, int Cj,
	double * BXdata, double * LATdata, double * LONdata, int St/*,
	double CALirb_m, double CALirb_n, double CALirb_a, // chr 07
	double CALirb_b1, double CALirb_b2*/
  ){

	int 	Braw;
	int 	h1, h2, N, mk, sumaMK;
	int 	m, n, mI, mS, nI, nS;
	double 	lat, hLATcel;
	double 	lon, hLONcel;
	double 	lx, tx;

	// INCREMENTOS SOBRE DOS
	hLATcel = dLATcel/2;
	hLONcel = dLONcel/2;

	// RECORRO LA IMAGEN
	for (h1=0;h1<(St);h1++){

		// DATO DE CADA PIXEL
		Braw = BXdata[h1]; lat = LATdata[h1]; lon = LONdata[h1];
		lx = 0; tx = 0; mk = 0;

		// // SI EL PIXEL ESTÁ EN LA VENTANA A CONSIDERAR
		if ((lat >= (LATmin - hLATcel))&&(lat <= (LATmax + hLATcel))){
			if ((lon >= (LONmin - hLONcel))&&(lon <= (LONmax + hLONcel))){

				// HALLAR LOS INDICES EN LA MATRIZ
				hallar_limites_en_grilla(Ci, Cj, lat, lon,
					dLATgri, dLONgri, hLATcel, hLONcel, LATmin, LONmin,
					&nI, &nS, &mI, &mS);
				
				// PROCESO EL PIXEL SOLO SI TIENE UBICACION
				// CHEQUEO DE PUNTAS
				if ((mI<=mS)&&(mI<Ci)&&(mS>=0)){
					if ((nI<=nS)&&(nI<Cj)&&(nS>=0)){

						// CALCULO DE PRODUCTOS
						if (Braw > 0){
							// calculo_productos_IRB(Braw,    // chr 08
							// 	CALirb_m, CALirb_n, CALirb_a,
							// 	CALirb_b1, CALirb_b2, &tx);
							mk = 1;
						}

						// ACUMULO EN LA CELDA CORRESPONDIENTE
						for (m=mI;m<(mS+1);m++){
							for (n=nI;n<(nS+1);n++){
								h2 = (Ci - 1 - m)*Cj + n;
								if (mk == 1){
									TXmat[h2] = TXmat[h2] + tx;
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

	// CALCULO DE PROMEDIOS
	realizar_promedio(TXmat, CNT1mat, Ct);

	// ENMASCARADOS VARIOS
	sumaMK = 0;
	generar_mascara(CNT1mat, CNT2mat, Ct, MSKmat, &sumaMK);

	// ASIGNACION DE TAG
	*fracMK = ((double) sumaMK) / ((double) Ct); // calcular el cociente ZMK / Ct = cociente
	asignar_tag(*fracMK, &*tag);
	return 1;
} // procesar_IRB_gri

int realizar_promedio(double * SUMA, int * CNT, int Ct){
	int 	h1, cnt;
	for (h1=0;h1<(Ct);h1++){
		cnt = CNT[h1];
		if (cnt>0){
			SUMA[h1] = SUMA[h1]/cnt;
		}
	}
	return 1;
}

int enmascarar_por_CZ(double * VAR, double * CZ, int Ct, double thr){
	int 	h1;
	for (h1=0;h1<(Ct);h1++){
		if (CZ[h1] < thr){
			VAR[h1] = 0;
		}
	}
	return 1;
}

int generar_mascara(int * CNT1, int * CNT2, int Ct, int * MSK, int *sumaMK){

	int 	h1, cnt1, cnt2;
	double 	frac;

	*sumaMK = 0;
	for (h1=0;h1<(Ct);h1++){
		frac = 0;
		cnt1 = CNT1[h1];
		cnt2 = CNT2[h1];
		if (cnt2>0){
			frac = cnt1/cnt2;
		}
		if (frac >= celMIN){
			MSK[h1] = 1; // cero por defecto
		}
		*sumaMK = *sumaMK + MSK[h1]; // Calcular sumatoria de MK[i]
	}
	return 1;
}


int hallar_limites_en_grilla(int Ci, int Cj, double lat, double lon,
	double dLATgri, double dLONgri, double hLATcel, double hLONcel,
	double LATmin, double LONmin, int *nI, int *nS, int *mI, int *mS){

	double nId, nSd, mId, mSd;
	double latI, latS, lonI, lonS;

	// HALLO LIMITES EN LA GRILLA.
	latI = lat - hLATcel;
	latS = lat + hLATcel;
	mId = (latI - LATmin)/dLATgri;
	mSd = (latS - LATmin)/dLATgri;
	*mI = (int) (mId + 1);
	*mS = (int) (mSd);
	lonI = lon - hLONcel;
	lonS = lon + hLONcel;
	nId = (lonI - LONmin)/dLONgri;
	nSd = (lonS - LONmin)/dLONgri;
	*nI = (int) (nId + 1);
	*nS = (int) (nSd);
	if (*mI < 0){  *mI = 0;}
	if (*mS >= Ci){*mS = (Ci-1);}
	if (mSd < 0){  *mS = -1;}
	if (*nI < 0){  *nI = 0;}
	if (*nS >= Cj){*nS = (Cj-1);}
	if (nSd < 0){  *nS = -1;}

	return 1;
}

int asignar_tag(double fracMK, int *tag){

	// ASIGNACION DE BANDERA = {0 img no OK, 1 img OK, 2 img impainting, 3 img mal}
	*tag = 0;
	if ( fracMK == imgTHR1){*tag = 1;}
	if ((fracMK < imgTHR1)&&(fracMK >= imgTHR2)){*tag = 2;}
	if ((fracMK < imgTHR2)&&(fracMK >= imgTHR3)){*tag = 3;}
	if ((fracMK < imgTHR3)&&(fracMK >= imgTHR4)){*tag = 4;}
	if ((fracMK < imgTHR4)){*tag = 5;}

	return 1;
}

int calculo_productos_VIS(int Braw, double cosz, double Fn, double fc,
	double CALvis_Xspace, double CALvis_M, double CALvis_K, // chr 09
	double *fr, double *rp){
			
	double 	ls;

	ls = ((Braw/32) - CALvis_Xspace)*CALvis_M; // Radiancia pre-launch
	ls = ls * fc; // Radiancia post-launch
	*fr = (ls * CALvis_K)/(10 * Fn); // (x100) - En porcentaje. (/1000) - Parámetro K expresado por mil.
	if (*fr > 100){*fr = 100;}
	if (*fr < 0){*fr = 0;}
	*rp = *fr / cosz;
	if (*rp > 100){*rp = 100;};
	if (*rp < 0){*rp = 0;};
	
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
	return 1;
}

// chr 10
// int calculo_productos_IRB(int Braw,
// 	double CALirb_m, double CALirb_n, double CALirb_a,
// 	double CALirb_b1, double CALirb_b2, double *tx){
	
// 	double lx, aux, Teff, C1, C2;

// 	// Parametros de calibracion
// 	C1 = 0.000011911;
// 	C2 = 1.438833;

// 	lx = ((Braw/32) - CALirb_b1)/CALirb_m; // Radiancia pre-launch
// 	aux = 1 + (C1*CALirb_n*CALirb_n*CALirb_n/lx);
// 	Teff = (C2 * CALirb_n)/log(aux);
// 	*tx = CALirb_a + CALirb_b2*Teff;

// 	return 1;
// }

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
} // cargar_calibracion_VIS

int cargar_calibracion_IRB(char RUTAcal[CMAXstr],
	double ** CALvis_m, double ** CALvis_n, double ** CALvis_a,
	double ** CALvis_b1, double ** CALvis_b2){

	FILE * data;
	char PATH[CMAXstr];
	char STRste[2];
	char STRirb[2];
	int     k, h1, h2, ste, ARCHste, Ccal;
	double	m, n, a, b1, b2;

	// TAMANO DE LOS VECTORES DE CALIBRACION IRB
	Ccal = Cirb * Cste;

	// ALOCAR MEMORIA REQUERIDA
	if (!(*CALvis_m  = (double *) malloc(Ccal * sizeof(double *)))){return 0;}
	if (!(*CALvis_n  = (double *) malloc(Ccal * sizeof(double *)))){return 0;}
	if (!(*CALvis_a  = (double *) malloc(Ccal * sizeof(double *)))){return 0;}
	if (!(*CALvis_b1 = (double *) malloc(Ccal * sizeof(double *)))){return 0;}
	if (!(*CALvis_b2 = (double *) malloc(Ccal * sizeof(double *)))){return 0;}
	
	// CARGO ARCHIVOS
	for (h1 = 0; h1 < Cste; h1++){ // LOOP EN SATELITE

		// STRING DEL SATELITE
		ste = GOES[h1];
		if (ste < 10){sprintf(STRste, "0%d", ste);}else{sprintf(STRste, "%d", ste);}


		for (h2 = 0; h2 < Cirb; h2++){ // LOOP EN CANALES

			sprintf(STRirb, "0%d", IRBS[h2]);
			strcpy(PATH, RUTAcal); strcat(PATH, "B"); strcat(PATH, STRirb);
			strcat(PATH, "_GOES"); strcat(PATH, STRste);

			//printf("%s\n", PATH);

			// DATA CALIBRACION POS-LAUNCH, cierro ejecucion si no se encuentra
			data = fopen(PATH, "ro");
			if (data == NULL) {printf("No se encontro archivo de calibracion POS. Cerrando.\n"); return 0;}
			fscanf(data, "%d\n", &ARCHste);
			fscanf(data, "%lf\n", &m);
			fscanf(data, "%lf\n", &b1);
			fscanf(data, "%lf\n", &n);
			fscanf(data, "%lf\n", &a);
			fscanf(data, "%lf\n", &b2);
			fclose(data);
			if (ARCHste != ste){printf("No se pudo verificar el CHK POS. Cerrando.\n"); return 0;}

			// ASIGNO DATOS DE CALIBRACION
			k = h1*Cirb + h2;
			(*CALvis_m)[k] = m;
			(*CALvis_n)[k] = n;
			(*CALvis_a)[k] = a;
			(*CALvis_b1)[k] = b1;
			(*CALvis_b2)[k] = b2;
		}
	}
	return 1;
} // cargar_calibracion_IRB

int mostrar_vector_double(double * vec, int cvec, int cmax){

	int		h1, h2;
	
	h2 = 1;
	for (h1 = 0; h1 < cvec; h1++){
		if (h2==cmax){
			printf("%+010.4f\n", vec[h1]); h2=1;
		}else{
			printf("%+010.4f\t", vec[h1]); h2=h2+1;
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
			printf("%08d\n", vec[h1]); h2=1;
		}else{
			printf("%08d  ", vec[h1]); h2=h2+1;
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
	return 1;
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
//	printf("[%d] :: [%d] :: [%2.5f] :: [%2.5f] :: [%2.5f] :: [%2.5f]\n", Ci, Cj, PSIlat, dLATgri, PSIlon, dLONgri);

	// RUTAS
	strcpy(RUTAmeta, RUTAsal); strcat(RUTAmeta, "meta/T000gri.META");
	strcpy(RUTA_LATvec, RUTAsal); strcat(RUTA_LATvec, "meta/T000gri.LATvec");
	strcpy(RUTA_LONvec, RUTAsal); strcat(RUTA_LONvec, "meta/T000gri.LONvec");
	strcpy(RUTA_LATmat, RUTAsal); strcat(RUTA_LATmat, "meta/T000gri.LATmat");
	strcpy(RUTA_LONmat, RUTAsal); strcat(RUTA_LONmat, "meta/T000gri.LONmat");

//	printf("%s\n", &RUTAmeta[0]);
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
} // guardar_grilla

int generar_strings_temporales(int yea, int doy, int hra, int min, int sec,
	char strTMP[COUTstr], char strYEA[4], char strDOY[3],
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
	sprintf(strTMP, "ART_%s%s_%s%s%s", strYEA, strDOY, strHRA, strMIN, strSEC);

	return 1;
}

int guardar_imagen_VIS(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, 
	double * FRmat, double * RPmat, double * N1mat, int * MKmat,
	int tag, double fracMK, int Band){

	FILE * fid;
	int		h1;
	char RUTA_MK[CMAXstr];
	char RUTA_FR[CMAXstr];
	char RUTA_RP[CMAXstr];
	char RUTA_N1[CMAXstr];
	char strTMP[COUTstr];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	char strBANDA[2];
	short * SAVE_MK;
	float * SAVE_FR;
	float * SAVE_RP;
	float * SAVE_N1;

	// STRINGS
	sprintf(strBANDA, "0%d", Band);
	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

 	// GUARDAR TAG
	guardar_tag(RUTAsal, strTMP, strYEA, strDOY, strHRA, strMIN, strSEC, strBANDA,
		tag, fracMK);

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

 	// GUARDO IMAGEN ACEPTABLE
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
		// printf("%s\n", RUTA_MK);
 		// printf("%s\n", RUTA_FR);
 		// printf("%s\n", RUTA_RP);
 		// printf("%s\n", RUTA_N1);
 		fid = fopen(RUTA_MK, "wb"); fwrite(SAVE_MK, sizeof(short), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_FR, "wb"); fwrite(SAVE_FR, sizeof(float), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_RP, "wb"); fwrite(SAVE_RP, sizeof(float), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_N1, "wb"); fwrite(SAVE_N1, sizeof(float), Ct, fid); fclose(fid);
 	}

	// GUARDO IMPAINTING
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
 		// printf("%s\n", RUTA_MK);
 		// printf("%s\n", RUTA_FR);
 		// printf("%s\n", RUTA_RP);
 		// printf("%s\n", RUTA_N1);
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
} // guardar_imagen_VIS

int guardar_imagen_IRB(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, 
	double * TXmat, int * MKmat, int tag, double fracMK, int Band){

	FILE * fid;
	int		h1;
	char RUTA_MK[CMAXstr];
	char RUTA_TX[CMAXstr];
	char strTMP[COUTstr];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	char strBANDA1[2];
	char strBANDA2[2];
	short * SAVE_MK;
	float * SAVE_TX;
	
	// STRINGS
	sprintf(strBANDA1, "%d", Band);
	sprintf(strBANDA2, "0%d", Band);
	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

	// GUARDAR TAG
	guardar_tag(RUTAsal, strTMP, strYEA, strDOY, strHRA, strMIN, strSEC, strBANDA2,
		tag, fracMK);

 	// ARMAR DATASETS A GUARDAR CASTEADO A FLOAT (no DOUBLE)
 	if (!(SAVE_MK = (short *) malloc(Ct * sizeof(short *)))){return 0;}
 	if (!(SAVE_TX = (float *) malloc(Ct * sizeof(float *)))){return 0;}
 	for (h1=0;h1<(Ct);h1++){
 		SAVE_MK[h1] = (short) (MKmat[h1]); // SE HACE PARA CASTEAR A SHORT
 		SAVE_TX[h1] = (float) (TXmat[h1]); // SE HACE PARA CASTEAR A FLOAT
 	}

 	if ((tag == 1)||(tag == 2)||(tag == 3)){
 		// RUTA MK, TX
 		strcpy(RUTA_MK, RUTAsal); strcat(RUTA_MK, "B"); strcat(RUTA_MK, strBANDA2);
 		strcat(RUTA_MK, "-MK/"); strcat(RUTA_MK, strYEA); strcat(RUTA_MK, "/");
 		strcat(RUTA_MK, strTMP); strcat(RUTA_MK, ".MK");
 		strcpy(RUTA_TX, RUTAsal); strcat(RUTA_TX, "B"); strcat(RUTA_TX, strBANDA2);
 		strcat(RUTA_TX, "-T"); strcat(RUTA_TX, strBANDA1);
 		strcat(RUTA_TX, "/"); strcat(RUTA_TX, strYEA); strcat(RUTA_TX, "/");
 		strcat(RUTA_TX, strTMP); strcat(RUTA_TX, ".T"); strcat(RUTA_TX, strBANDA1);
 		// Guardo!
		// printf("%s\n", RUTA_MK);
 	// 	printf("%s\n", RUTA_TX);
 		fid = fopen(RUTA_MK, "wb"); fwrite(SAVE_MK, sizeof(short), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_TX, "wb"); fwrite(SAVE_TX, sizeof(float), Ct, fid); fclose(fid);
 	}

 	if ((tag == 3)||(tag == 4)||(tag == 5)){
 		// RUTA MK, TX
 	 	strcpy(RUTA_MK, RUTAsal); strcat(RUTA_MK, "zIMP/B"); strcat(RUTA_MK, strBANDA2);
 		strcat(RUTA_MK, "-MK/"); strcat(RUTA_MK, strYEA); strcat(RUTA_MK, "/");
 		strcat(RUTA_MK, strTMP); strcat(RUTA_MK, ".MK");
 		strcpy(RUTA_TX, RUTAsal); strcat(RUTA_TX, "zIMP/B"); strcat(RUTA_TX, strBANDA2);
 		strcat(RUTA_TX, "-T"); strcat(RUTA_TX, strBANDA1);
 		strcat(RUTA_TX, "/"); strcat(RUTA_TX, strYEA); strcat(RUTA_TX, "/");
 		strcat(RUTA_TX, strTMP); strcat(RUTA_TX, ".T"); strcat(RUTA_TX, strBANDA1);
 		// Guardo!
 		// printf("%s\n", RUTA_MK);
 		// printf("%s\n", RUTA_TX);
 		fid = fopen(RUTA_MK, "wb"); fwrite(SAVE_MK, sizeof(short), Ct, fid); fclose(fid);
 		fid = fopen(RUTA_TX, "wb"); fwrite(SAVE_TX, sizeof(float), Ct, fid); fclose(fid);
 	}

 	// Libero memoria
 	free(SAVE_MK);
 	free(SAVE_TX);

	// FIN
	return 1;
} // guardar_imagen_IRB

int guardar_tag(char RUTAsal[CMAXstr], char strTMP[COUTstr], char strYEA[4], char strDOY[3], char strHRA[2],
	char strMIN[2], char strSEC[2], char strBANDA[2], int tag, double fracMK){

	FILE * fid;
	char RUTA_TG[CMAXstr];
	char strTAG[35];

	// GUARDAR TAG
 	sprintf(strTAG, "%s,%s,%s,%s,%s,%d,%7.5f\n", strYEA, strDOY, strHRA, strMIN, strSEC, tag, fracMK); // escribo en la variable tag el valor que me pasan en tag_value
 	strcpy(RUTA_TG, RUTAsal); strcat(RUTA_TG, "zCRR/TAGs_B"); strcat(RUTA_TG, strBANDA);
 	strcat(RUTA_TG, "_");strcat(RUTA_TG, strYEA); strcat(RUTA_TG, ".TG");
 	fid = fopen(RUTA_TG, "ab"); fwrite(strTAG, sizeof(char), strlen(strTAG), fid); fclose(fid);

 	return 1;
}

int guardar_imagen_double(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, double * DATA, char * tipo, int Band){

	FILE * fid;
	int		h1;
	char RUTA[CMAXstr];
	char strTMP[COUTstr];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	char strBANDA2[2];
	float * SAVE;
	
	// STRINGS
	sprintf(strBANDA2, "0%d", Band);
	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

 	// ARMAR DATASETS A GUARDAR CASTEADO A FLOAT (no DOUBLE)
 	if (!(SAVE = (float *) malloc(Ct * sizeof(float *)))){return 0;}
 	for (h1=0;h1<(Ct);h1++){
 		SAVE[h1] = (float) (DATA[h1]); // SE HACE PARA CASTEAR A FLOAT
 	}

	// RUTA
	strcpy(RUTA, RUTAsal); strcat(RUTA, "test/B"); strcat(RUTA, strBANDA2);
	strcat(RUTA, "_"); strcat(RUTA, strTMP); strcat(RUTA, "."); strcat(RUTA, tipo);
	
	// Guardo!
	fid = fopen(RUTA, "wb"); fwrite(SAVE, sizeof(float), Ct, fid); fclose(fid);

 	free(SAVE);

	// FIN
	return 1;
}

int guardar_imagen_int(char RUTAsal[CMAXstr], int Ct,
	int yea, int doy, int hra, int min, int sec, int * DATA, char * tipo, int Band){

	FILE * fid;
	int		h1;
	char RUTA[CMAXstr];
	char strTMP[COUTstr];
	char strYEA[4];
	char strDOY[3];
	char strHRA[2];
	char strMIN[2];
	char strSEC[2];
	char strBANDA2[2];
	short * SAVE;

	// STRINGS
	sprintf(strBANDA2, "0%d", Band);
	generar_strings_temporales(yea, doy, hra, min, sec,
		&strTMP[0], &strYEA[0], &strDOY[0], &strHRA[0], &strMIN[0], &strSEC[0]);

 	// ARMAR DATASETS A GUARDAR CASTEADO A FLOAT (no DOUBLE)
 	if (!(SAVE = (short *) malloc(Ct * sizeof(short *)))){return 0;}
 	for (h1=0;h1<(Ct);h1++){
 		SAVE[h1] = (short) (DATA[h1]); // SE HACE PARA CASTEAR A FLOAT
 	}

	// RUTA
	strcpy(RUTA, RUTAsal); strcat(RUTA, "test/B"); strcat(RUTA, strBANDA2);
	strcat(RUTA, "_"); strcat(RUTA, strTMP); strcat(RUTA, "."); strcat(RUTA, tipo);
	
	// Guardo!
	fid = fopen(RUTA, "wb"); fwrite(SAVE, sizeof(short), Ct, fid); fclose(fid);

 	free(SAVE);

	// FIN
	return 1;
}
