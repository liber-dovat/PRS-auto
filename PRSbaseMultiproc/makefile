CC       = gcc
CPPFLAGS = -Wall -Werror -Wextra -ansi -pedantic -O2
XTRFLAGS = -ggdb
FLAGS    = -lnetcdf -lm
# FLAGS    = -lnetcdf -lm -lprj
Obj      = lib_PRSsat.o
SrcDir   = ./
ObjDir   = ./
BIN      =  PRSsat_auto_VIS PRSsat_auto_IRB

All: $(BIN)

PRSsat_auto_VIS: $(ObjDir)lib_PRSsat.o $(SrcDir)PRSsat_auto_VIS.c
	@echo -n "Making PRSsat_auto_VIS"
	@$(CC) $? $(XTRFLAGS) $(FLAGS) -o $@
	@echo "                                                       [ DONE ]"

PRSsat_auto_IRB: $(ObjDir)lib_PRSsat.o $(SrcDir)PRSsat_auto_IRB.c
	@echo -n "Making PRSsat_auto_IRB"
	@$(CC) $? $(XTRFLAGS) $(FLAGS) -o $@
	@echo "                                                       [ DONE ]"

lib_PRSsat.o: $(SrcDir)lib_PRSsat.c $(SrcDir)lib_PRSsat.h
	@echo -n "Making lib_PRSsat "
	@$(CC) $(XTRFLAGS) $(FLAGS) -c $(SrcDir)lib_PRSsat.c -o $(ObjDir)$@
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
