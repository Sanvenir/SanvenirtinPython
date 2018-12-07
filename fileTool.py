#Sanvenirtin
#roguelike game
#programming by Sanvenir
#ver 0.0.1
#File saving tools
#Saving races, maps, hero properties, NPC;map include local maps and main maps;
#Saving file categories:
#-----1.main maps:
#-------(1)map width
#-------(2)map height
#-------(3)main map data

#-----**property reading:
#-------reading data in that order: conValue, armStrValue, legStrValue, touValue
#-----------------------------------intValue, wilValue, dexValue, senValue,
#-----------------------------------recValue, bodyHeight, bodyWeight

#-----2.races:
#-------(1)race total num
#-------(2)in order of identity:
#----------a.race name
#----------b.race starting property
#----------c.race increasing property
#----------d.race male property
#----------e.race female property

#-----**item reading:
#-------(1)name
#-------(2)weight
#-------(3)volume
#-------(4)image name
#-------(5)introduction

#-----**npc reading:
#-------reading data in that order:
#-------(0)identity
#-------(1)properties
#-------(2)hunger[0], health[0], injure[0], endure[0]
#-------(3)paralysis, dead(?)
#-------(4)sex
#-------(5)age
#-------(6)race identity
#-------(7)item total num
#-------(8)due to the number reading items

#-----3.local maps:
#
