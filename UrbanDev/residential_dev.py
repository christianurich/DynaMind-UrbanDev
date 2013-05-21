"""
@file
@author  Chrisitan Urich <christian.urich@gmail.com>
@version 1.0
@section LICENSE

This file is part of DynaMind
Copyright (C) 2012  Christian Urich

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from pydynamind import * 
import operator   


class residential_dev(Module):
     def __init__(self):
         Module.__init__(self)
         self.superblocks = View("CITY", FACE, READ)
         self.superblocks.getAttribute("unplaced_total_households")
         self.superblocks.getAttribute("year")
         self.parcels = View("PARCEL", FACE, READ)
         self.parcels.getAttribute("attractiveness")
         self.parcels.getAttribute("possible_ress")
         self.parcels.modifyAttribute("released")
                  
         datastream = []
         datastream.append(self.superblocks)
         datastream.append(self.parcels)
         
         self.addData("city", datastream)


         
     def run (self):
         city = self.getData("city")
         uuids = city.getUUIDs(self.superblocks)
         population=0
         year=0
         for uuid in uuids:
             sp = city.getFace(uuid)
             population = sp.getAttribute("unplaced_total_households").getDouble()
             year = sp.getAttribute("year").getDouble()
      
         a_v=[]
         a_m={}
         print "Unplaced Households" + str(population)
         uuids = city.getUUIDs(self.parcels)
         for uuid in uuids:
             sp = city.getFace(uuid)
             released =  sp.getAttribute("released").getDouble()
             if released > 0:
                 continue
             attractiveness = sp.getAttribute("attractiveness").getDouble()
             a_v.append(attractiveness)
             a_m[uuid]=attractiveness

         a_v.sort()
  
         a_sort=sorted(a_m.iteritems(),key=operator.itemgetter(1))
         
         pop_to_pace = population
         avalible_units = len(a_v)
         print "Avalible Units " + str(avalible_units)
         h = 0
         while pop_to_pace > 0 and avalible_units > 0:
             id=a_sort[h][0]
             parcel=city.getFace(id)
             parcel.addAttribute("released", year)
             avalible_units = avalible_units-1
             pop_to_pace = pop_to_pace - parcel.getAttribute("possible_ress").getDouble()
             h = h+1
         print "PLACED " +str(h)
