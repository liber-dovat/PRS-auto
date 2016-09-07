# Funciones copiadas de:
# http://stackoverflow.com/questions/620305/convert-year-month-day-to-day-of-year-in-python

import calendar
from datetime import date, datetime

def doy(Y,M,D):
  """ given year, month, day return day of year
      Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """
  if calendar.isleap(Y):
      K = 1
  else:
      K = 2
  N = int((275 * M) / 9.0) - K * int((M + 9) / 12.0) + D - 30
  return N

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------

def ymd(Y,N):
  """ given year = Y and day of year = N, return year, month, day
      Astronomical Algorithms, Jean Meeus, 2d ed, 1998, chap 7 """    
  if calendar.isleap(Y):
      K = 1
  else:
      K = 2
  M = int((9 * (K + N)) / 275.0 + 0.98)
  if N < 32:
      M = 1
  D = N - int((275 * M) / 9.0) + K * int((M + 9) / 12.0) + 30
  return Y, M, D

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# http://stackoverflow.com/questions/5734438/how-to-create-a-month-iterator
# Iterador de meses

def months(start_month, start_year, end_month, end_year):
  month, year = start_month, start_year
  while True:
    yield month, year
    if (month, year) == (end_month, end_year):
        return  
    month += 1
    if (month > 12):
        month = 1
        year += 1

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
# http://stackoverflow.com/questions/153584/how-to-iterate-over-a-timespan-after-days-hours-weeks-and-months-in-python

def datespan(startDate, endDate, delta):
  
  # C = currentDate
  C = startDate
  while C <= endDate:
    yield C.year, C.month, doy(C.year, C.month, C.day), C.hour, C.minute, C.second 
    C += delta
