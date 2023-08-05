#!/usr/bin/env python
from os.path import isfile
import tensorflow as tf
import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
import json as js


def init_bonds(p_):
    spec,bonds,offd,angs,torp,hbs = [],[],[],[],[],[]
    for key in p_:
        # key = key.encode('raw_unicode_escape')
        # print(key)
        k = key.split('_')
        if k[0]=='bo1':
           bonds.append(k[1])
        elif k[0]=='rosi':
           kk = k[1].split('-')
           # print(kk)
           if len(kk)==2:
              offd.append(k[1])
           elif len(kk)==1:
              spec.append(k[1])
        elif k[0]=='theta0':
           angs.append(k[1])
        elif k[0]=='tor1':
           torp.append(k[1])
        elif k[0]=='rohb':
           hbs.append(k[1])
    return spec,bonds,offd,angs,torp,hbs


def get_p(ffield):
    if ffield.endswith('.json'):
       lf = open(ffield,'r')
       j = js.load(lf)
       p  = j['p']
       m       = j['m']
       spec,bonds,offd,angs,torp,hbs= init_bonds(p)
    else:
       p,zpe_,spec,bonds,offd,Angs,torp,Hbs=read_lib(libfile=ffield,zpe=False)
       m = None
    return p,m,bonds

def f_nn(x,m=None,pre=None,bd=None,layer=[4,1]):
    wi  = np.array(m[pre+'wi_'+bd]) 
    bi  = np.array(m[pre+'bi_'+bd] ) 
    w   = np.array(m[pre+'w_'+bd] ) 
    b   = np.array(m[pre+'b_'+bd] ) 
    wo  = np.array(m[pre+'wo_'+bd] ) 
    bo  = np.array(m[pre+'bo_'+bd] ) 
    #x  = np.expand_dims(x,axis=1)
    o   = []
    o.append(sigmoid(np.matmul(x,wi)+bi))  
                                                                  # input layer
    for l in range(layer[1]):                                     # hidden layer      
        o.append(sigmoid(np.matmul(o[-1],w[l])+b[l]))
   
    out  = sigmoid(np.matmul(o[-1],wo) + bo) 
    # out = np.squeeze(o_)                                        # output layer
    return out

    
def sigmoid(x):
    s = 1.0/(1.0+np.exp(-x))
    return s


class Linear(tf.keras.Model):
    def __init__(self,J=None,nnlayer=[4,1]):
        super().__init__()
        self.hl       = nnlayer[1]
        self.wh       = []
        self.bh       = []
        self.wbf      = 'vdwtaper.json' if J is None else J
        if J is None or not isfile(self.wbf):
           self.wi  = tf.Variable(tf.random.normal([1,nnlayer[0]],stddev=0.2),name='wi')
           self.bi  = tf.Variable(tf.random.normal([nnlayer[0]],stddev=0.2),name='bi')
           
           for i in range(nnlayer[1]):
               self.wh.append(tf.Variable(tf.random.normal([nnlayer[0],nnlayer[0]],
                                stddev=0.2),name='wh_%d' %i))
               self.bh.append(tf.Variable(tf.random.normal([nnlayer[0]],
                                stddev=0.2),name='bh_%d' %i))

           self.wo  = tf.Variable(tf.random.normal([nnlayer[0],1],stddev=0.2),name='wo')
           self.bo  = tf.Variable(tf.random.normal([1],stddev=0.2),name='bo')
        else:
           with open(J,'r') as lf:
                j = js.load(lf)
           hl_ = len(j['wh'])
           self.wi  = tf.Variable(j['wi'],name='wi')
           self.bi  = tf.Variable(j['bi'],name='bi')

           for i in range(self.hl):
               if i <=hl_-1:
                  self.wh.append(tf.Variable(j['wh'][i],name='wh_%d' %i))
                  self.bh.append(tf.Variable(j['bh'][i],name='bh_%d' %i))
               else:
                  self.wh.append(tf.Variable(tf.random.normal([nnlayer[0],nnlayer[0]],
                                 stddev=0.2),name='wh_%d' %i))
                  self.bh.append(tf.Variable(tf.random.normal([nnlayer[0]],
                                 stddev=0.2),name='bh_%d' %i))

           self.wo  = tf.Variable(j['wo'],name='wo')
           self.bo  = tf.Variable(j['bo'],name='bo')

    def call(self, r):
        o  = []
        o.append(tf.sigmoid(tf.matmul(r,self.wi)+self.bi))
        for i in range(self.hl):
            o.append(tf.sigmoid(tf.matmul(o[-1],self.wh[i])+self.bh[i]))
        output   = tf.sigmoid(tf.matmul(o[-1],self.wo)+self.bo)
        return tf.squeeze(output)

    def save(self):
        with open(self.wbf,'w') as fj:
             j = {}
             wh = []
             bh = []
             for i in range(self.hl):
                 wh.append(self.wh[i].numpy().tolist())
                 bh.append(self.bh[i].numpy().tolist())
             j['wi'] = self.wi.numpy().tolist()
             j['bi'] = self.bi.numpy().tolist()
             j['wh'] = wh
             j['bh'] = bh
             j['wo'] = self.wo.numpy().tolist()
             j['bo'] = self.bo.numpy().tolist()
             js.dump(j,fj,sort_keys=True,indent=2)
        return j


def fitbo(step=2000,old=True):
    with open('ffield.json','r') as lf:
         j = js.load(lf)
         p  = j['p']
         m_ = j['m']
    spec,bonds,offd,angs,torp,hbs= init_bonds(p)
    model = Linear(J='bo.json',nnlayer=[4,2])

    x_  = np.linspace(0.0001,2.6,100,dtype=np.float32)
    x   = np.expand_dims(x_,axis=1)

    for bd in bonds:
        for pre in ['si','pi','pp']:
            y   = fbo(x,m=m_,p=p,pre=pre,bd=bd,old=old)
            b_  = get_bo(x_,bd=bd,m=m_,p=p,pre=pre)
            # print(y.shape,b_.shape)
            # neural network layers
            optimizer = tf.keras.optimizers.Adam(learning_rate=0.01)
            # plt.ion()   # something about plotting
            plt.figure()
            for s in range(step):
                # train and net output
                with tf.GradientTape() as tape:
                     y_pred = model(b_)     
                     loss = tf.reduce_mean(tf.square(y_pred - y))
                grads = tape.gradient(loss, model.variables) # 使用 model.variables 这一属性直接获得模型中的所有变量
                optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))
                
                if s % 100 == 0:
                   # plt.text(0.5, 0, 'Step: %d Loss=%.4f' %(step,loss), fontdict={'size': 20, 'color': 'red'})
                   # plt.pause(0.1)
                   print('Step: %d Loss=%.4f' %(s,loss))
                if loss<0.0001:
                   print('Convergeced!')
                   break
            # print(x.shape,y.shape)
            plt.scatter(x,y)
            plt.plot(x,y_pred, 'r-', lw=3)
            plt.savefig('Fitbo%s%s.pdf' %(pre,bd))
            plt.close()
            m = model.save()

            wi_ = 'f' + pre +'wi'+ '_' +bd
            j['m'][wi_] = m['wi']
            bi_ = 'f' + pre +'bi'+ '_' +bd
            j['m'][bi_] = m['bi']

            wo_ = 'f' + pre +'wo'+ '_' +bd
            j['m'][wo_] = m['wo']
            bo_ = 'f' + pre +'bo'+ '_' +bd
            j['m'][bo_] = m['bo']

            w_ = 'f' + pre +'w'+ '_' +bd
            j['m'][w_] = m['wh']
            b_ = 'f' + pre +'b'+ '_' +bd
            j['m'][b_] = m['bh']

    with open('ffieldFitted.json','w') as fj:
         js.dump(j,fj,sort_keys=True,indent=2)


def fbo(x,bd='C-C',m=None,p=None,pre='si',old=True):
    # p,m,bonds = get_p('ffield.json')
    x_   = np.squeeze(x)
    bo   = get_bo(x_,bd=bd,m=m,p=p,pre=pre)
    fbo_ = f_nn(bo,m=m,pre='f'+pre,bd=bd)
    if old:
       bo_ = np.squeeze(fbo_*bo)
    else:
       bo_ = fbo_
    return bo_


def get_bo(r,bd='C-C',m=None,p=None,pre='si'):
    b = bd.split('-')
    bdn = b[0] if b[0]==b[1] else bd 
    if pre=='si':
       ro_ = 'rosi_'
       bo1_= 'bo1_'
       bo2_= 'bo2_'
    elif pre=='pi':
       ro_ = 'ropi_'
       bo1_= 'bo3_'
       bo2_= 'bo4_'
    elif pre=='pp':
       ro_ = 'ropp_'
       bo1_= 'bo5_'
       bo2_= 'bo6_'

    rosi=p[ro_+bdn]
    bo1=p[bo1_+bd]
    bo2=p[bo2_+bd]
    bo   = np.exp(bo1*(r/rosi)**bo2)
    bo_  = np.expand_dims(bo,axis=1)
    return bo_


def func(x):
    s = sigmoid(x)
    return (s*s - 0.5)**2


def resolve():
    res = minimize_scalar(func,method='brent')
    print(res.x)
  
    t = sigmoid(0.8813735870089523)
    print(t*t)


if __name__ == '__main__':
   ''' use commond like ./bp.py <t> to run it
       z:   optimize zpe 
       t:   train the whole net
   '''
   # plotMorse()
   fitbo()


   