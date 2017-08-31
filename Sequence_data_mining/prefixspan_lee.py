
import gc
import shlex
import time
MinimumSupport = 0.03
start = time.time()

def SupportCount(newdata):
    tmpsub = {}
    for x in newdata:
        repeat = []
        for y in x:
            for z in y:
                if z not in repeat:
                    if z in tmpsub:
                        tmpsub[z] += 1
                    else:
                        tmpsub[z] = 1
                    repeat.append(z)
    s = []
    for x in tmpsub.keys():
        if tmpsub[x] >= MinimumSupport * len(newdata):
            s.append(x)
    # print(s)
    gc.collect()
    return s

def PrefixSpan(data,subseq,ans,pre):
    for i in subseq:
        newpre = []
        if len(pre) != 0:
            for p in pre:
                newpre.append(p)
        newpre.append(i)
        ans.append(newpre)
        newdata = []
        newsubseq = []
        for j in data:
            newrow = []
            found = False
            for k in j:
                newpat = []
                if found == False:
                    if i in k:
                        if len(k) != 1:
                            desh = False
                            for l in range(k.index(i)+1,len(k)):
                                if desh == False:
                                    newpat.append((-1)*k[l])
                                    desh = True
                                else:
                                    newpat.append(k[l])
                            if k.index(i)+1 != len(k):
                                newrow.append(newpat)
                        found = True
                else:
                    newrow.append(k)
            if len(newrow) != 0:
                newdata.append(newrow)
        newsubseq = SupportCount(newdata)
        newsubseq.sort()
        if len(newsubseq) != 0:
            ans = PrefixSpan(newdata,newsubseq,ans,newpre)
    return ans

input1 = open("Dataset/test.ascii","r")
data = []
tmpsup = {}
first = -1
firstnow = -1
second = -1
for i in input1.readlines():
    i = shlex.split(i)
    for j in range(0,3):
        i[j] = int(i[j])
    if i[0] - 1 != first:
        data.append([])
        first = i[0] - 1
        firstnow += 1
        secondnow = -1
    if i[1] - 1 != second:
        data[firstnow].append([])
        second += 1
        secondnow += 1
    data[firstnow][secondnow].append(i[2])
    if i[2] in tmpsup:
        tmpsup[i[2]] += 1
    else:
        tmpsup[i[2]] = 1
subseq = []
for i in tmpsup.keys():
    if tmpsup[i] >= MinimumSupport * 50000:
    #if tmpsup[i] >= MinimumSupport:
        subseq.append(i)
subseq.sort()

# for i in data:
#     print(i)

ans = []

ans = PrefixSpan(data,subseq,ans,[])
end = time.time()
elapsed = end - start
print "Time taken: ", elapsed, "seconds."
print(ans)
print(len(ans))
