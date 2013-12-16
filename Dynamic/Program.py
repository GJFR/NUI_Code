'''
Created on 9-dec.-2013

@author: Gertjan
'''

import Calibration
import Recognition


if __name__ == '__main__':
    labels = Calibration.run(["Rechts","Links"])
    Recognition.recognize(labels)