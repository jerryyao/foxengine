# -*- coding: utf-8 -*-

import numpy as np

def tmatch(signal,length=5,interval=1):
    ''' 正确设置超时平仓点    
        平仓参数：信号，持股时长，间隔. signal>0为有信号
        其中，若时长之内有新的买入，则时长从0计算
        间隔为信号后的清场间隔，因为买入信号第二天(假设信号当天买入)才能卖出，所以一般为1
        length=5为一周内完成
    '''
    
    rev = np.zeros_like(signal)
    total = length > interval and length or interval  #如果持股一天,interval=1,则是第三天卖出(2,1,0)
    cur = -1
    for i in xrange(len(signal)):
        cur = total if signal[i] > 0 else cur-1
        rev[i] = 1 if cur == 0 else 0
    return rev
    
def matchshift(target,follow):  
    ''' follow中信号只有在target中有未匹配信号时才后移1位，否则抛弃
        可用于卖出信号对买入信号的匹配跟踪上，避免当日买卖的情形
    '''
    assert len(target) == len(follow)
    if(len(follow) == 0):
        return  np.array([])
    rev = np.zeros_like(target)
    sstate = 0 #信号状态
    for i in xrange(len(target)-1):
        ct,cf = target[i],follow[i]
        if(ct != 0 and cf == 0):
            sstate = 1
        elif(cf != 0 and (ct != 0 or sstate == 1)):
            sstate = 0
            rev[i+1] = cf
    return rev

def makematch(target,follow):
    ''' 根据target中的信号，对target中信号发出日后的第一个follow信号次日置位，其它的都置0. 这样就不需要roll(1)了
        特殊情况：如果target信号当日有follow信号，则follow当日信号仍然存在，并添加次日信号
        非0为有信号
        Note:对于买入信号前一日发出的卖出信号(因此体现在买入日),不消除，但也不添加，只是单纯保持。由trade去搞定
        最后一个follow信号的处理:
            因为循环只到length-1,所以最后一个follow信号没有被处理
            有两种情况，一种，如果最后一个target无信号，则最后一个follow信号不论怎么处理都不会影响trade(即便要生效，也要次日才能执行trade)
                另一种，如果当日有target信号，则如果follow信号不置位，则会影响target信号是否被实施
            统一起见，与中间的情况保持一致
            最后一个如果有target信号，则follow置位，否则不管
    '''
    assert len(target) == len(follow)
    if(len(follow) == 0):
        return  np.array([])
    if(len(follow) == 1):
        return np.array([0])  #必然是0，即使follow[0]=1，因为只能次日发出，所以也为[0]
    rev = np.zeros_like(target)
    sstate = 1  #信号状态. 第一个无买入卖出也视作有信号。这样，可以用于买卖抵消
    for i in xrange(len(target)-1):
        ct,cf = target[i],follow[i]
        if(ct != 0 and cf != 0): #当日信号保留，还添加次日信号
            rev[i+1] = rev[i] = cf
            sstate = 0
        elif(ct != 0):   #follow[i] == 0
            sstate = 1
            #rev[i] = 0  #取消因为昨日之卖出信号而发出的信号
        elif(cf != 0 and sstate == 1):    #target[i] == 0
            #print i,sstate
            rev[i+1] = cf
            sstate = 0
    #都不用，则自然正确表示最后一个卖出信号推移出序列的情形
    rev[-1] = 1 if target[-1] and follow[-1] else rev[-1]  #如果最后一个target和follow都有信号，则设置follow以利抵消，否则保留之前设置的(最后一次循环设置)或者预置的0
    return rev

