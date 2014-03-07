# database of FPGA boards

class Device:
    def __init__(self, family, name, package, speed):
        self.family = family
        self.name = name
        self.package = package
        self.speed = speed

    def coregen_options(self):
        return {
            'devicefamily': self.family,
            'device': self.name,
            'package': self.package,
            'speedgrade': self.speed
        }

    def xst_part(self):
        return self.name+str(self.speed)+'-'+self.package

susibo = Device('virtex5', 'xc5vlx30t', 'ff665', -2)
syscore3 = Device('spartan6', 'xc6slx150t', 'fgg900', -3)

