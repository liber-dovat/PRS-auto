CC      = gcc
FLAGS   = -Wall -Werror -Wextra -ansi -pedantic -O2
FLAGS2  = -lnetcdf -lm
Obj     = lib_PRS_R.o
SrcDir  = ./
ObjDir  = ./
BIN     = PRS_auto_R PRS_proc_R

All: $(BIN)

PRS_auto_R: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_auto_R.c
	@echo -n "Making PRS_auto_R"
	@$(CC) -o $@ $@.c $(ObjDir)$(Obj) $(FLAGS2)
	@echo "                                                       [ DONE ]"

PRS_proc_R: $(ObjDir)lib_PRS_R.o $(SrcDir)PRS_proc_R.c
	@echo -n "Making PRS_proc_R"
	@$(CC) -o $@ $@.c $(ObjDir)$(Obj) $(FLAGS2)
	@echo "                                                       [ DONE ]"

lib_PRS_R.o: $(SrcDir)lib_PRS_R.c $(SrcDir)lib_PRS_R.h
	@echo -n "Making lib_PRS_R "
	@$(CC) $(FLAGS2) -c $(SrcDir)lib_PRS_R.c -o $(ObjDir)$@
	@echo "                                                       [ DONE ]"

clean:
	@echo -n "Cleaning        "
	@rm -rf $(ObjDir)*.o
	@rm -rf $(BIN)
	@echo "                                                       [ DONE ]"
