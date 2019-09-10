#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

class LocType:
  def __init__(self, valor, msk, cnt, ite):
    self.valor = valor
    self.msk   = msk
    self.cnt   = cnt
    self.ite   = ite

  def __lt__(self, other):
    return self.ite < other.ite

#########################################

class DateType:
  def __init__(self, year, doy, hh, mm, ss, ite):
    self.year = year
    self.doy  = doy
    self.hh   = hh
    self.mm   = mm
    self.ss   = ss
    self.ite  = ite

  def __lt__(self, other):
    return self.ite < other.ite
