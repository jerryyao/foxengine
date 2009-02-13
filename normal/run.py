# -*- coding: utf-8 -*-

#完整的演示脚本

from wolfox.fengine.core.shortcut import *
from wolfox.fengine.normal.funcs import *

import logging
logger = logging.getLogger('wolfox.fengine.normal.run')    

def run_body(sdata,dates,begin,end):
    from time import time
    tbegin = time()

    pman = AdvancedATRPositionManager()
    dman = DateManager(begin,end)
    myMediator=mediator_factory(trade_strategy=B1S1,pricer = oo_pricer)
    seller = atr_seller_factory(3000)
    #seller = csc_func
    #pman = AdvancedPositionManager()

    config = fcustom(BaseObject,seller=seller,pman=pman,dman=dman)
    configs = []
    #configs.append(config(buyer=fcustom(ma3,fast=4,mid=45,slow=88)))
    #configs.append(config(buyer=fcustom(ma3,fast=8,mid=45,slow=70)))

    #configs.append(config(buyer=fcustom(svama2,fast=53,slow=108)))
    #configs.append(config(buyer=fcustom(svama2,fast=16,slow=61)))
    #configs.append(config(buyer=fcustom(svama2,fast=7,slow=62)))
    #configs.append(config(buyer=fcustom(svama2,fast=14,slow=126)))    
    #configs.append(config(buyer=fcustom(svama2,fast=5,slow=98)))
    #configs.append(config(buyer=fcustom(svama2,fast=14,slow=88)))
    #configs.append(config(buyer=fcustom(svama2,fast=8,slow=71)))
    
    #configs.append(config(buyer=fcustom(svama2s,fast=53,slow=108)))
    #configs.append(config(buyer=fcustom(svama2s,fast=16,slow=61)))
    #configs.append(config(buyer=fcustom(svama2s,fast=7,slow=62)))
    #configs.append(config(buyer=fcustom(svama2s,fast=14,slow=126)))    
    #configs.append(config(buyer=fcustom(svama2s,fast=5,slow=98)))
    #configs.append(config(buyer=fcustom(svama2s,fast=14,slow=88)))
    #configs.append(config(buyer=fcustom(svama2s,fast=8,slow=71)))
    #configs.append(config(buyer=fcustom(svama3,fast=12,mid=55,slow=119)))
    #configs.append(config(buyer=fcustom(svama3,fast=23,mid=64,slow=120)))
    #configs.append(config(buyer=fcustom(svama3,fast=31,mid=57,slow=30)))
    
    configs.append(config(buyer=fcustom(vama3,fast=12,mid=59,slow=116)))
    configs.append(config(buyer=fcustom(vama3,fast=20,mid=64,slow=119)))    
    configs.append(config(buyer=fcustom(vama3,fast=29,mid=55,slow=100)))    
    configs.append(config(buyer=fcustom(vama3,fast=12,mid=45,slow=100)))
    configs.append(config(buyer=fcustom(vama3,fast=25,mid=53,slow=124)))
    configs.append(config(buyer=fcustom(vama3,fast=8,mid=43,slow=102)))
    
    configs.append(config(buyer=fcustom(vama2,fast=2,slow=113)))
    configs.append(config(buyer=fcustom(vama2,fast=26,slow=123)))
    configs.append(config(buyer=fcustom(vama2,fast=3,slow=22)))
    configs.append(config(buyer=fcustom(vama2,fast=3,slow=58)))    
    
    configs.append(config(buyer=fcustom(svama2,fast=1,slow=3)))
    configs.append(config(buyer=fcustom(svama2,fast=1,slow=5)))    
    configs.append(config(buyer=fcustom(svama2,fast=47,slow=94)))    
    configs.append(config(buyer=fcustom(svama2,fast=5,slow=68)))    
    configs.append(config(buyer=fcustom(svama3,fast=12,mid=42,slow=127)))    
    configs.append(config(buyer=fcustom(svama3,fast=20,mid=64,slow=119)))
    configs.append(config(buyer=fcustom(svama3,fast=12,mid=59,slow=116)))
    configs.append(config(buyer=fcustom(svama3,fast=17,mid=57,slow=92)))    
    configs.append(config(buyer=fcustom(vama3,fast=18,mid=52,slow=22)))    
    


    
    #configs = [config1,config2,config3]
    #configs = [config3]
    #configs = [config1,config2]
    batch(configs,sdata,dates,begin,cmediator=myMediator)

    tend = time()
    print u'耗时: %s' % (tend-tbegin)
    logger.debug(u'耗时: %s' % (tend-tbegin))    

    save_configs('atr_ev.txt',configs)

def run_main(dates,sdata,idata,catalogs,begin,end):
    d_posort('g5',sdata.values(),distance=5)        
    d_posort('g20',sdata.values(),distance=20)    
    d_posort('g120',sdata.values(),distance=120)     
    d_posort('g250',sdata.values(),distance=250)     
    run_body(sdata,dates,begin,end)


if __name__ == '__main__':
    logging.basicConfig(filename="run.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    begin,end = 20010701,20050701
    from time import time
    tbegin = time()
    dates,sdata,idata,catalogs = prepare_all(begin,end,[],[ref_code])
    #dates,sdata,idata,catalogs = prepare_all(begin,end,['SH600000','SZ002258'],[ref_code])    
    tend = time()
    print u'数据准备耗时: %s' % (tend-tbegin)    
    run_main(dates,sdata,idata,catalogs,begin,end)
