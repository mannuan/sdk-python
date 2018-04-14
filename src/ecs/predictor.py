from flavor import Flavor
from common import Common

def predict_vm(ecsContent, inputContent):
    # Do your work from here#
    result = []
    if ecsContent is None:
        print 'ecs information is none'
        return result
    if inputContent is None:
        print 'input file information is none'
        return result
    flavorList = Flavor()
    input = Common.parseInput(inputContent, flavorList)


    return result
