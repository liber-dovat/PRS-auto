CC       = gcc
CPPFLAGS = -Wall -Werror -Wextra -ansi -pedantic -O2
XTRFLAGS = -ggdb
FLAGS    = -lnetcdf -lm -lproj
Obj      = lib_PRS_R.o
SrcDir   = ./
ObjDir   = ./
BIN      = PRS_auto_R PRS_proc_R

All: $(BIN)

PRS_auto_R: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_auto_R.c
	@echo -n "Making PRS_auto_R"
	@$(CC) $? $(XTRFLAGS) $(FLAGS) -o $@
	@echo "                                                       [ DONE ]"

PRS_proc_R: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_proc_R.c
	@echo -n "Making PRS_proc_R"
	@$(CC) $? $(XTRFLAGS) $(FLAGS) -o $@
	@echo "                                                       [ DONE ]"

lib_PRS_R.o: $(SrcDir)lib_PRS_R.c $(SrcDir)lib_PRS_R.h
	@echo -n "Making lib_PRS_R "
	@$(CC) $(XTRFLAGS) $(FLAGS) -c $(SrcDir)lib_PRS_R.c -o $(ObjDir)$@
	@echo "                                                       [ DONE ]"

clean:
	@echo -n "Cleaning        "
	@rm -rf $(ObjDir)*.o
	@rm -rf $(BIN)
	@echo "                                                       [ DONE ]"

# $@ : nombre del objetivo
# $< : primer prerequisito
# $? : todos los prerequisitos
# instalar proj.4-master desde github https://github.com/OSGeo/proj.4 https://proj4.org/
# instalar libnetcdf-dev
# instalar automake autotools-dev libtool