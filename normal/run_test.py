# -*- coding: utf-8 -*-

import unittest

import sys
import os
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    #准备测试环境
    from django.core.management import setup_environ
    import wolfox.foxit.other_settings.settings_sqlite_test as settings
    setup_environ(settings)

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.run import run_main

import logging
logger = logging.getLogger('wolfox.fengine.normal.run_test')

class ModuleTest(unittest.TestCase):    #保持run的有效性
    def setUp(self):
        from StringIO import StringIO
        self.tmp = sys.stdout
        sys.stdout = StringIO()  #将标准I/O流重定向到buff对象，抑制输出

    def tearDown(self):
        sout = sys.stdout.getvalue()
        logger.debug(u'demo测试控制台输出:%s',sout)
        sys.stdout = self.tmp        #恢复标准I/O流
        #print sout
    
    def test_run(self):
        begin,end = 20010101,20060101
        dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000'],[ref_code])
        run_main(dates,sdata,idata,catalogs,begin,end)        
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

