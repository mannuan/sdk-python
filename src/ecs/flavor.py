# -*- coding:utf-8 -*-

class Flavor(object):

    '''
    flavorName : str
    cpu : int
    menory : int
    '''
    def __init__(self, flavorName, cpu, memory):
        self.flavorName = [flavorName]
        self.cpu = [cpu]
        self.memory = [memory]

    #name : str
    def getFlavor(self, name):
        flavor = list()
        try:
            index = self.flavorName.index(name)
            flavor.append(name)
            flavor.append(self.cpu[index])
            flavor.append(self.memory[index])
        except Exception:
            print 'This flavor is not in flavor list.'
            flavor.append(name + "is not in flavor list")
        return flavor

    #flavorName : str
    #cpu : int
    #memory : int
    def setFlavor(self, flavorName, cpu, memory):
        try:
            self.flavorName.index(flavorName)
        except Exception:
            self.flavorName.append(flavorName)
            self.cpu.append(cpu)
            self.memory.append(memory)
