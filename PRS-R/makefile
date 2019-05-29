CC       = gcc
CPPFLAGS = -Wall -Werror -Wextra -ansi -pedantic -O2
XTRFLAGS = -ggdb
FLAGS    = -lnetcdf -lm -lproj
Obj      = lib_PRS_R.o
SrcDir   = ./
ObjDir   = ./
BIN      = PRS_auto_R PRS_proc_R PRS_file

All: $(BIN)

PRS_auto_R: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_auto_R.c
	@echo -n "Making PRS_auto_R"
	@$(CC) $? $(XTRFLAGS) $(FLAGS) -o $@
	@echo "                                                       [ DONE ]"

PRS_proc_R: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_proc_R.c
	@echo -n "Making PRS_proc_R"
	@$(CC) $? $(XTRFLAGS) $(FLAGS) -o $@
	@echo "                                                       [ DONE ]"

PRS_file: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_file.c
	@echo -n "Making PRS_file"
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

# cd /usr/share/
# ls
# mv proj proj.lnx
# ls /root/
# mv proj.* /root/
# ls
# cp -R /home/ldovat/proj .
# chown -R root:root proj/
# chmod -R +x proj/
# ls -la.4
# apt-cache search proj
# apt-cache search proj.4
# apt-get install python-mpltoolkits.basemap
# exit
# reboot
# mv libproj.so.0 libproj.so.0.old
# ln -s libproj.so.13 libproj.so.0
# ls -la
# ls -la libproj*
