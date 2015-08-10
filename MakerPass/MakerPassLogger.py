#!/usr/bin/python

import logging

logging.basicConfig(filename='/home/pi/makerpass/MakerPass/logs/makerpass.log',
format='%(levelname)s:%(asctime)s:%(name)s:%(message)s', datefmt='%m-%d-%Y %H:%M:%S', level=logging.DEBUG)

#logger = logging.getLogger('makerpass')
main_logger = logging.getLogger('main')
Machine_logger = logging.getLogger('Machine')
MachinePlug_logger = logging.getLogger('MachinePlug')
MachinePlugCreator_logger = logging.getLogger('MachinePlugCreator')
MachinePlug_PowerMonitored_logger = logging.getLogger('MachinePlug_PowerMonitored')
MachinePlug_2State_logger = logging.getLogger('MachinePlug_2State')
MachinePlug_WemoInsight_logger = logging.getLogger('MachinePlug_WemoInsight')
MachinePlug_GPIO_logger = logging.getLogger('MachinePlug_GPIO')
MachinePlug_TestBrand_logger = logging.getLogger('MachinePlug_TestBrand')
MakerPassDatabase_logger = logging.getLogger('MakerPassDatabase')
PLNU_IDCardSwipe_logger = logging.getLogger('PLNU_IDCardSwipe')
PipeSwipe_logger = logging.getLogger('PipeSwipe')
SmartPlugTestBrand_logger = logging.getLogger('SmartPlugTestBrand')
SmartPlugWemoInsight_logger = logging.getLogger('SmartPlugWemoInsight')
RegisterScan_logger = logging.getLogger('RegisterScan')





