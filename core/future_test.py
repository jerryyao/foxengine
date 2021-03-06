# -*- coding: utf-8 -*-

import unittest
import logging

import numpy as np
from wolfox.fengine.core.future import * 

logger = logging.getLogger("wolfox.fengine.core.future_test")

class ModuleTest(unittest.TestCase):
    def test_mm_ratio(self):
        shigh = np.array([200,250,200,400])
        slow = np.array([100,200,100,200])
        sclose = np.array([150,220,180,300])
        satr = atr(sclose,shigh,slow,1)
        #print satr
        amfe,amae = mm_ratio(sclose,shigh,slow,satr,2)
        self.assertEquals([700,800,0,0],amfe.tolist())
        self.assertEquals([-300,400,0,0],amae.tolist())        

    def test_mm_sum(self):
        sbuy = np.array([0,1,1,0,1,0,0])
        smfe = np.array([1,2,3,4,50,6,7])
        smae = np.array([10,20,30,40,500,60,70])
        sum_mfe,sum_mae = mm_sum(sbuy,smfe,smae)
        #print s.mfe_sum,s.mae_sum
        self.assertEquals(55,sum_mfe)
        self.assertEquals(550,sum_mae)
        
    def test_mm_sum_smooth(self):
        sbuy = np.array([0,1,1,0,1,0,0])
        smfe = np.array([1,2,3,4,50,6,7])
        smae = np.array([10,20,30,40,500,60,70])
        sum_mfe,sum_mae = mm_sum_smooth(sbuy,smfe,smae)
        #print s.mfe_sum,s.mae_sum
        self.assertEquals(23,sum_mfe)
        self.assertEquals(550,sum_mae)

    def test_mm_sum_smooth_less_than_0(self):
        sbuy = np.array([0,1,1,0,1,0,0])
        smfe = np.array([1,2,3,4,50,6,7])
        smae = np.array([10,20,-30,40,-500,60,70])
        sum_mfe,sum_mae = mm_sum_smooth(sbuy,smfe,smae)
        #print s.mfe_sum,s.mae_sum
        self.assertEquals(23,sum_mfe)
        self.assertEquals(22,sum_mae)
 
    def test_mm_sum_smooth_greaterthan_length(self):
        sbuy = np.array([0,1,1,0,1,0,0])
        smfe = np.array([1,2,3,4,50,6,7])
        smae = np.array([10,20,30,40,500,60,70])
        sum_mfe,sum_mae = mm_sum_smooth(sbuy,smfe,smae,4)
        #print s.mfe_sum,s.mae_sum
        self.assertEquals(54,sum_mfe)
        self.assertEquals(550,sum_mae)

    def test_sum_smooth_mfe(self):
        from wolfox.fengine.core.future import _sum_smooth_mfe
        self.assertEquals(13,_sum_smooth_mfe(np.array([1,2,3,4,5])))
        self.assertEquals(12,_sum_smooth_mfe(np.array([1,2,3,4,5]),2))
        self.assertEquals(15,_sum_smooth_mfe(np.array([1,2,3,4,5]),8))

    def test_sum_smooth_mae(self):
        from wolfox.fengine.core.future import _sum_smooth_mae
        self.assertEquals(15,_sum_smooth_mae(np.array([1,2,3,4,5])))
        self.assertEquals(13,_sum_smooth_mae(np.array([1,2,-3,4,5])))
        self.assertEquals(9,_sum_smooth_mae(np.array([1,2,-3,0,5])))

    def test_decline(self):
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,930,915,990,1020,990])
        self.assertEquals((107,4),decline(sclose))
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,930,891,990,1020,990])
        self.assertEquals((116,8),decline(sclose))
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,1030,1050,990,970,930,935,915,990,1040,1080])
        self.assertEquals((135,5),decline(sclose))
        mr,mp = decline(sclose)
        self.assertEquals(type(1),type(mr))
        self.assertEquals(type(1),type(mp))

    def test_decline_ranges(self):
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,930,915,990,1020,990])
        self.assertEquals([107,45],decline_ranges(sclose,1).tolist())
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,930,891,990,1020,990])
        self.assertEquals([107,69],decline_ranges(sclose,1).tolist())
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,1030,1050,990,970,930,935,915,990,1040,1080])
        self.assertEquals([107,120,20],decline_ranges(sclose,1).tolist())
        self.assertEquals([107,135],decline_ranges(sclose,2).tolist())  #过滤掉点935的小突起

    def test_decline_periods(self):
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,930,915,990,1020,990])
        self.assertEquals([4,2],decline_periods(sclose,1).tolist())
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,930,910,899,990,1020,990])
        self.assertEquals([4,3],decline_periods(sclose,1).tolist())
        sclose = np.array([1000,1005,1007,990,940,920,900,910,960,1030,1050,990,970,930,935,915,990,1040,1080])
        self.assertEquals([4,3,1],decline_periods(sclose,1).tolist())
        self.assertEquals([4,5],decline_periods(sclose,2).tolist())

    def test_xmax_points(self):
        self.assertEquals([],xmax_points(np.array([]),5).tolist())
        self.assertEquals([0,0,0],xmax_points(np.array([1,3,2]),2).tolist())
        self.assertEquals([0,1,0],xmax_points(np.array([1,3,2]),1).tolist())
        self.assertEquals([0,0,0],xmax_points(np.array([5,3,4]),1).tolist())   #第一位无法确认为最高点
        self.assertEquals([0,0,0],xmax_points(np.array([1,3,4]),1).tolist())   #最后一位无法确认为最高点
        self.assertEquals([0,0,0,1,0,0],xmax_points(np.array([1,3,5,6,2,1]),2).tolist())
        self.assertEquals([0,1,0,1,0,0],xmax_points(np.array([1,7,5,6,2,8]),1).tolist())
        #测试重复情形
        self.assertEquals([0,0,0,1,0,0],xmax_points(np.array([7,7,5,6,2,8]),1).tolist())
        self.assertEquals([0,1,0,1,0,0],xmax_points(np.array([1,7,6,6,2,8]),1).tolist())   #虽然和[3]和[2]都是6，但因为rev[2]!=1，所以[3]还是可以计入高点
        self.assertEquals([0,1,0,1,0,0],xmax_points(np.array([1,7,6,6,6,4]),1).tolist())   #rev[4]被[3]derepeat,不能计入

    def test_xmin_points(self):
        self.assertEquals([],xmin_points(np.array([]),5).tolist())
        self.assertEquals([0,0,0],xmin_points(np.array([1,3,2]),2).tolist())
        self.assertEquals([0,1,0],xmin_points(np.array([1,0,2]),1).tolist())
        self.assertEquals([0,0,0],xmin_points(np.array([0,3,4]),1).tolist())   #第一位无法确认为最低点
        self.assertEquals([0,0,0],xmin_points(np.array([1,3,0]),1).tolist())   #最后一位无法确认为最低点
        self.assertEquals([0,0,0,1,0,0],xmin_points(np.array([1,3,5,0,2,1]),2).tolist())
        self.assertEquals([0,1,0,1,0,0],xmin_points(np.array([1,0,5,0,2,1]),1).tolist())
        #测试重复情形
        self.assertEquals([0,0,0,1,0,0],xmin_points(np.array([0,0,5,0,2,1]),1).tolist())
        self.assertEquals([0,1,0,1,0,0],xmin_points(np.array([2,0,1,1,2,1]),1).tolist())
        self.assertEquals([0,1,0,1,0,0],xmin_points(np.array([1,0,5,1,1,1]),1).tolist())

    def test_xpeak_points(self):
        self.assertEquals([],xpeak_points(np.array([]),5).tolist())
        self.assertEquals([0,0,0],xpeak_points(np.array([1,3,2]),2).tolist())
        self.assertEquals([0,-1,0],xpeak_points(np.array([1,0,2]),1).tolist())
        self.assertEquals([0,0,0],xpeak_points(np.array([0,3,4]),1).tolist())   #第一位无法确认为最低点
        self.assertEquals([0,1,0],xpeak_points(np.array([1,3,0]),1).tolist())   #最后一位无法确认为最低点
        self.assertEquals([0,0,0,1,0,0],xpeak_points(np.array([1,3,5,6,2,1]),2).tolist())
        self.assertEquals([0,1,-1,1,-1,0],xpeak_points(np.array([1,7,5,6,2,8]),1).tolist())
        #测试重复情形
        self.assertEquals([0,0,-1,1,-1,0],xpeak_points(np.array([7,7,5,6,2,8]),1).tolist())
        self.assertEquals([0,1,-1,1,-1,0],xpeak_points(np.array([1,7,6,6,2,8]),1).tolist())  #[2]的6被计为底点
        self.assertEquals([0,1,-1,1,0,0],xpeak_points(np.array([1,7,6,6,6,4]),1).tolist())   #rev[4]被6被derepeat,不能计入
        self.assertEquals([0,0,1,0,0,1,0,0],xpeak_points(np.array([0,1,5,3,4,7,6,4]),2).tolist())

    def test_xpeak_points_2(self):  #只测试通过性和特殊情形
        self.assertEquals([],xpeak_points_2(np.array([]),np.array([]),5).tolist())
        self.assertEquals([0,0,0],xpeak_points_2(np.array([1,3,2]),np.array([1,2,3]),2).tolist())
        #高底点同时出现,直接抵消.较长extend时这个不可能出现
        self.assertEquals([0,0,0],xpeak_points_2(np.array([1,3,2]),np.array([1,0,3]),1).tolist())
        #只出现底点的情形，作为参照
        self.assertEquals([0,-1,0],xpeak_points_2(np.array([1,2,3]),np.array([1,0,3]),1).tolist())
        #连续的同向顶点
        #print 'consecutive'
        self.assertEquals([0,0,1,0,0,1,0,0],xpeak_points_2(np.array([0,1,5,3,4,7,6,4]),np.array([0,1,5,3,4,7,6,4]),2).tolist())

if __name__ == "__main__":
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    unittest.main()

