
class Granularity(object):
    INSTRUCTION = 1
    METHOD = 2
    CLASS = 4
    GRANULARITIES = {
        "instruction": INSTRUCTION,
        "method": METHOD, 
        "class": CLASS
    }
    default = "instruction"
    
    def __init__(self, granularity="instruction"):
        self.granularity = Granularity.GRANULARITIES[granularity]
    
    @staticmethod
    def granularities():
        return Granularity.GRANULARITIES.keys()

    @staticmethod
    def is_class(granularity):
        return granularity <= Granularity.CLASS

    @staticmethod
    def is_method(granularity):
        return granularity <= Granularity.METHOD
    
    @staticmethod
    def is_instruction(granularity):
        return granularity == Granularity.INSTRUCTION

    @staticmethod
    def get(granularity_key):
        for granularity_method, granularity_num in Granularity.GRANULARITIES.items():
            if granularity_key == granularity_num:
                return granularity_method
        raise WrongGranularityValueException
    
class WrongGranularityValueException(Exception):
    pass