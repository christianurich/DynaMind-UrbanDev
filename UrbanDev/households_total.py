"""
@file
@author  Chrisitan Urich <christian.urich@gmail.com>
@version 1.0
@section LICENSE

This file is part of DynaMind
Copyright (C) 2013  Christian Urich

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


class households_total(Module):
     def __init__(self):
         Module.__init__(self)

         self.createParameter("scenario", INT, "Select a scenario")
         self.scenario = 1
         self.vcity = View("CITY", FACE, READ)
         self.vcity.getAttribute("total_households")
         self.vcity.addAttribute("unplaced_total_households")
                  
         datastream = []
         datastream.append(self.vcity)
         
         self.addData("city", datastream)
         
         self.total_household_inital = 0
         self.counter = 0
         
         self.senarios_years = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030]
         
         self.growth = [1.0,1.008980364,1.017985367,1.027015111,1.036069697,1.045149229,1.054461599,1.063803382,1.073174718,1.082575748,1.092006612,1.101248676,1.110516476,1.119810118,1.129129712,1.138475366,1.147541158,1.156627519,1.165734518,1.174862226,1.184010713]         
         self.competition = [1.0,1.006176528,1.012370003,1.018580493,1.02480807,1.031052804,1.037519217,1.044006054,1.050513412,1.057041389,1.063590083,1.069947034,1.076321687,1.082714115,1.089124393,1.095552597,1.101704992,1.107871347,1.114051707,1.120246121,1.126454637]       
         self.security = [1.0,1.002571596,1.005150248,1.007735985,1.010328835,1.012928829,1.015736154,1.018552346,1.021377447,1.024211499,1.027054545,1.029702066,1.032356958,1.035019254,1.037688983,1.040366178,1.042772779,1.045184839,1.047602378,1.050025415,1.052453967]
         self.risk = [1.0,1.0017705,1.003545858,1.005326094,1.007111228,1.008901279,1.010895473,1.012895966,1.014902788,1.016915968,1.018935537,1.020758739,1.022587018,1.024420396,1.026258892,1.02810253,1.029676731,1.031254504,1.032835861,1.034420813,1.036009374]
         
         
     def run (self):

         household_growth = []
         if self.scenario == 1:
             household_growth = self.growth
         if self.scenario == 2:
             household_growth = self.competition
         if self.scenario == 3:
             household_growth = self.security
         if self.scenario == 4:
             household_growth = self.risk             
         
         self.counter += 1
         city = self.getData("city")
         uuids = city.getUUIDs(self.vcity)
         
         for uuid in uuids:
             c = city.getFace(uuid)
         
         if self.counter == 1:
             self.total_household_inital = c.getAttribute("total_households").getDouble()
             
         growth_rate = household_growth[self.counter]
         print self.total_household_inital
         new_total_households = self.total_household_inital * growth_rate
        
         unplaced_households = new_total_households - c.getAttribute("total_households").getDouble()
        
         c.addAttribute("unplaced_total_households", unplaced_households)
         
         c.addAttribute("total_households", new_total_households)
         
         print unplaced_households


         
         