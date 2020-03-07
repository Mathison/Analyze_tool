#!/usr/bin/env python
#coding=utf-8
# Function: translate the results from BTM
# Input:
#    mat/pw_z.k20

import sys

# return:    {wid:w, ...}
def read_voca(pt):
    voca = {}
    for index,l in enumerate(open(pt)):
        try:
            w = str(l.replace('\n',''))
            voca[int(index)] = w
        except Exception as e:
            print(e) 
    return voca

def read_pz(pt):
    return [float(p) for p in open(pt).readline().split()]
    
# voca = {wid:w,...}
def dispTopics(pt, voca, pz):
    k = 0
    topics = []
    for l in open(pt):
        vs = [float(v) for v in l.split()]
        wvs = zip(range(len(vs)), vs)
        wvs = sorted(wvs, key=lambda d:d[1], reverse=True)
        #tmps = ' '.join(['%s' % voca[w] for w,v in wvs[:10]])
        tmps = ' '.join(['%s:%f' % (voca[w],v) for w,v in wvs[:30]])
        topics.append((pz[k], tmps))
        k += 1
        
    print('p(z)\t\tTop words')
    for pz, s in topics:
        print('%f\t%s' % (pz, s))

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python %s <model_dir> <K> <voca_pt>' % sys.argv[0])
        print('\tmodel_dir    the output dir of BTM')
        print('\tK    the number of topics')
        print('\tvoca_pt    the vocabulary file')
        exit(1)
        
    model_dir = sys.argv[1]
    K = int(sys.argv[2])
    voca_pt = sys.argv[3]
    voca = read_voca(voca_pt)    
    W = len(voca)
    print('K:%d, n(W):%d' % (K, W))

    pz_pt = model_dir + 'k%d.pz' % K
    pz = read_pz(pz_pt)
    
    zw_pt = model_dir + 'k%d.pw_z' %  K
    dispTopics(zw_pt, voca, pz)
