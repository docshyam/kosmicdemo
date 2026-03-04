#!/usr/bin/python3
from  matplotlib import pyplot as plt
import csv,sys
import scipy
import pprint
from numpy import trapezoid
import numpy as np
from statistics import median,mean
import time

np.set_printoptions(suppress=True)
sys.path.append('/home/shyam/KOSMICDEMO/python-bindings')
import kosmic

fig, ax = plt.subplots(2,2, figsize=(10,10))
plts = (fig, ax)
print(plts)
plt.subplots_adjust(wspace=0.4, hspace=0.4)
 
f=open(sys.argv[1])
c=csv.reader(f)
freq_max=float(sys.argv[2])
cumfreq_max=float(sys.argv[3])

x=[]
for d in c:
  if(len(d)>0):
    try:
      float_number = float(d[0])
      x=x+[float_number]
    except ValueError as e:
      pass

hist_result=plts[1][0,0].hist(x,bins=np.linspace(min(x),max(x),num=201),histtype='step')
plts[1][0,0].set_xlabel("Albumin Concentration (g/dL)")
plts[1][0,0].set_ylabel("Frequency (Number of Samples)")

hist_result_cum=plts[1][1,0].hist(x,bins=np.linspace(min(x),max(x),num=201),histtype='step',cumulative=True)
plts[1][1,0].set_xlabel("Albumin Concentration (g/dL)")
plts[1][1,0].set_ylabel("Cumulative Frequency (Number of Samples)")
 
h_mu=mean(hist_result[0])

result = kosmic.kosmic(x, decimals=1)
result = {k: round(v, 3) if isinstance(v, float) else v for k, v in result.items()}
lr=round(kosmic.percentile(result, 0.025), 2)
middle=round(kosmic.percentile(result, 0.50), 2)
ur=round(kosmic.percentile(result, 0.975), 2)

plts[1][0,0].plot([ur,ur],[0,freq_max])
plts[1][0,0].plot([lr,lr],[0,freq_max])

plts[1][1,1].plot([ur,ur],[0,0.5])
plts[1][1,1].plot([lr,lr],[0,0.5])

plts[1][1,0].plot([ur,ur],[0,cumfreq_max])
plts[1][1,0].plot([lr,lr],[0,cumfreq_max])

mu    = result["mu"]
sigma = result["sigma"]
plts[1][0,1].axis('off')

pprint.pprint(hist_result)
pprint.pprint(result)

t1=plts[1][0,1].table(
  [
    ['Parameter','Value'],
    ['μ',result["mu"]],
    ['σ',result["sigma"]],
    ['t1(low cut-off)',result["t1"]],
    ['t2(low cut-off)',result["t2"]],
    ['λ',result["lambda"]],
    ['ks',result["ks"]],
    ['Reference Interval (2.5%-97.5%)','{}-{}'.format(lr,ur)],
    ['mean (50%)',middle]
  ],loc="center")

t1.auto_set_font_size(False)
t1.set_fontsize(12)
  
basic_x=np.linspace(0,1,101)
basic_y=[]
for i in basic_x:
    basic_y=basic_y+[kosmic.percentile(result, i)]

plts[1][1,1].plot(basic_y,basic_x)
plts[1][1,1].set_xlabel("Albumin Concentration (g/dL)")
plts[1][1,1].set_ylabel("Cumulative Frequency (Fraction of Total Samples)")

plt.tight_layout()
plt.show()
plt.close()

'''
{'bootstrap': [],
 'ks': 0.0022613108952529936,
 'lambda': 0.07,
 'mu': 3.1508196560827586,
 'sigma': 0.7163059461821749,
 't1': 11.5,
 't2': 46.8}

'''
