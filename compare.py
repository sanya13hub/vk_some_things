filename = "letmepaint-stats-2016-12-09.csv"
filename2 = "letmepaint-stats-2016-12-09-fast.csv"
with open(filename, 'r') as f:
    with open(filename2, 'r') as f2:
        buf = f.read()
        buf1 = buf.split('\n')
        buf2 = f2.read()
        buf3 = buf2.split('\n')
        mem=[]
        for id in buf1:
            #print('{}-{}'.format(buf1.index(id),buf3.index(id)))
            if id not in mem:
                mem.append(id)
            else:
                print(id)
            if id not in buf3:
                print(id)
