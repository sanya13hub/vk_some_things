#coding=utf-8
import sys, math,requests, re, datetime,time, os, csv, asyncio
from aiohttp import ClientSession

try:
    import xlwt
except:
    #print('xlwt обосрамс')
    pass

startime = time.time()


def progress(lenli, i):
    sys.stdout.write('\r')
    part = float(i) / (lenli - 1)
    symbols_num = int(60 * part)
    sys.stdout.write("          [%-60s] %3.2f%%" % ('=' * symbols_num, part * 100))
    sys.stdout.flush()


def getUsersFromPub(_idg, offse=0):
    rq = requests.get(
        'https://api.vk.com/method/groups.getById?&group_id={0}'.format(_idg)).json()
    filename = str(rq['response'][0]['gid']) + '_[' + re.sub('\W','-',rq['response'][0]['name']) + ']_' + \
               str(datetime.datetime.now().date()) + '.txt'
    if not os.path.isfile(filename) or offse>0:

        ra = requests.get(
            'https://api.vk.com/method/groups.getMembers?&group_id=' + _idg + "&offset=" + str(offse) + "&sort=d_desc").json()
        r = ra['response']['users']
        cntr = ra['response']['count']
        if offse==0:
            print('\nfollowers: '+str(cntr)+'\n')
        progress(math.trunc(cntr / 1000) * 1000,offse)


        i = 0
        f = open(filename, 'a')
        for item in r:
            i += 1
            if r[0] == item:
                f.write('##########'+str(offse) + '\n')

            f.write('@'+str(item)+':0'+'\n')

        f.close()
        offse += 1000

        if (offse < cntr):
            getUsersFromPub(_idg, offse)
    return filename


def GetPubs(_id):

    ra = requests.get('https://api.vk.com/method/users.getSubscriptions?&user_id=' + _id).json()
    r = ra['response']['groups']['items']
    i=0
    shitstring=''
    for item in r:
        i=i+1

        shitstring = shitstring+ str(item)+'\n'
    return shitstring


def ifIdinFile(path,uid):
    f = open(path)
    buf = f.read()
    buf1 = buf.split('\n')

    if uid in buf:
        print('EZ FINDED')

    for line in buf1:
        if  line == uid :
            print(line)
            line1=line+':1'
            buf=re.sub(line,line1,buf)

    f.close()

    path2=re.sub("\.",'-new.',path,1)
    f = open(path2,'w')
    f.write(buf)
    f.close()

def crosspubs(*ids):
    path = {}
    pips={}
    first=0
    iterate=0
    buf=''

    for i in ids:
        path[i]=getUsersFromPub(i)
        ra = requests.get(
            'https://api.vk.com/method/groups.getMembers?&group_id=' + i).json()
        pips[i] = ra['response']['count']
        print('\n'+path[i].split('[')[1].split(']')[0]+ " : "+ str(pips[i]) +" users")
    l = lambda x: x[1]
    pipss = sorted(pips.items(), key=l)

    for i in pipss:
        i=i[0]
        if first==0:
            print('\nпроверка {0} записей из >> {1} << :'.format(str(pips[i]),path[i].split('[')[1].split(']')[0]))
            var = pips[i]
            progresslen=len(ids)*var
            f = open(path[i])
            buf = f.read()
            f.close()
            f = open('out.txt', 'w')
            f.close()
            first += 1
        elif first !=0:

            f = open(path[i])
            buf2 = f.read()
            #buf2 = buf2.split('\n')
            for line in buf.split('\n'):
                iterate += 1

                #progress(progresslen, iterate + first * var)

                if '#' not in line and line !='':
                    if first <= 1 or ':0' not in line:
                        if line.split(':')[0] in buf2:
                            idg=re.sub('@','',str(line.split(':')[0]))

                            line1 = '@'+idg+':'+str( int(line.split(':')[1]) + 1  )
                            if line != '' and '#' not in line:
                                #print(str(iterate) + line)
                                buf = re.sub(line, line1, buf)

            f.close()
            first+=1


    print('\n')
    i = 0
    for winner in buf.split('\n'):
        f = open('out.txt', 'a')

        if ':'+str(len(ids)-1) in winner:
            i+=1
            winner=re.sub('@','',winner)
            winner=winner.split(':')[0]
            link='http://vk.com/id{}'.format(winner)
            f.write(link+"\n")
            print(link)
    print('{} целей'.format(i))

def get_stats(*paths):
    longstring=''
    counter=0
    f = open('stats.txt', 'w')
    for pat in paths:
        if pat != 'xl':
            f.write(pat+ ' ')
            ff=open(getUsersFromPub(pat),'r')
            buf = ff.read()
            buf1 = buf.split('\n')
            for id in buf1:
                id = re.sub('@','',id).split(':')[0]
                if '#' not in id and counter ==0:
                    #print(id)
                    longstring=GetPubs(id)
                    #print(longstring+ "  loNG")
                    counter+=1
                if '#' not in id and id !='' and counter !=0:
                    #print(id)
                    string=GetPubs(id)
                    for pub in string.split('\n'):
                        if pub in longstring:
                            print(pub +'#############################')
                            pub1=pub+'$'
                            re.sub(pub,pub1,longstring)
                        else:
                            longstring+='\n'+pub


            ff.close()

    f.write(longstring)
    print(longstring)
    f.close()


def stats_pub_csv(*paths):
    longdict = {}
    counter=0
    filename = "{0}-stats-{1}.csv".format(paths[0],datetime.datetime.now().date())
    with open(filename, 'w',newline='') as f:
        w = csv.writer(f)
        for pat in paths:
            if pat != 'xl':
                ff = open(getUsersFromPub(pat),'r')
                buf = ff.read()
                buf1 = buf.split('\n')
                for id in buf1:
                    id = re.sub('@','',id).split(':')[0]
                    if '#' not in id and counter ==0:
                        longdict[id] = 1
                        counter += 1
                    if '#' not in id and id != '' and counter != 0:
                        string=GetPubs(id)

                        ### execute!!

                        progress(len(buf1),counter)
                        for pub in string.split('\n'):
                            if pub in longdict:
                                longdict[pub] += 1
                            else:
                                longdict[pub] = 1
                        counter += 1
        l = lambda x: x[1]
        longdict = sorted(longdict.items(), key=l, reverse=True)
        for key in longdict:
            if key[0] != '':

                print(str(key[0]) + ' ' + str(key[1]))

                w.writerows([key])


async def get(url, out, typo='pubs'):
    async with ClientSession() as session:
        async with session.get(url) as response:
            outPUT = await response.json()
            #print(outPUT)
            try:
                if typo == 'pubs':
                    out += outPUT['response']['groups']['items']
            except KeyError:
                print("ERR  "+str(outPUT))


def fast_get_pubs(*ids):
    loop = asyncio.get_event_loop()
    tasks = []
    bigout = []
    for i in ids[0]:
        task = asyncio.ensure_future(get('https://api.vk.com/method/users.getSubscriptions?&user_id={}'.format(str(i)), bigout))
        tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))
    return bigout

def fast_stats_pub_csv(*paths):
    longdict = {}
    ids = []
    filename = "{0}-stats-{1}-fast.csv".format(paths[0],datetime.datetime.now().date())

    for pat in paths:
        ff = open(getUsersFromPub(pat),'r')
        buf = ff.read()
        buf1 = buf.split('\n')
        PIPids = []
        for id in buf1:
            id = re.sub('@', '', id).split(':')[0]

            if '#' not in id and id !='':
                PIPids.append(str(id))

        templ = []
        appendc=0
        if len(PIPids) > 200:
            print('\n'+'{}'.format(len(PIPids)))

            for id1 in range(len(PIPids)):
                templ.append(str(PIPids[id1]))

                if id1 % 350 == 0 and id1 != 0:
                    ids.append(fast_get_pubs(templ))
                    appendc+=1
                    templ.clear()
                    progress( len(PIPids),id1)

            if len(templ) != 0:
                ids.append(fast_get_pubs(templ))
                appendc += 1

        else:
            ids.append(fast_get_pubs(PIPids))
            appendc += 1

        for app in range(appendc):
            for pub in ids[app]:

                if pub in longdict:
                    longdict[pub] += 1
                else:
                    longdict[pub] = 1


    l = lambda x: x[1]
    longdict = sorted(longdict.items(), key=l, reverse=True)
    print("\t\t\t\t\t{} разных подписок".format(len(longdict)))
    with open(filename, 'w',newline='') as f:
        w = csv.writer(f)

        for key in longdict:
            #print(key)
            w.writerows([key])

fast_stats_pub_csv('santa_muerte')


"""streng=['ass','1','jopa','bang']
with open('1.csv', 'w',newline='') as f1:
    w = csv.writer(f1)

    for i in streng:

        w.writerow(streng)"""

#fast_stats_pub_csv('dipshiet')


# fast_stats_pub_csv('santa_muerte') [11809] 344 secs(200) 296 sec(300) 253 sec(350) 354 sec)(400)

#  fast_stats_pub_csv('dipshiet') 11.453 secs
#  stats_pub_csv('dipshiet') 232.1335 secs w/o file
#  stats_pub_csv('112819170') 534.9552700519562 secs


print('\n'+'Time:'+str(time.time() - startime)+'\t'+"{0:.5f}".format((time.time() - startime)/200))

