import plyvel
import  os
import gzip



# write force str(key,value)
def _writeforcestrkv(str4bytesfile, it):
    with open(str4bytesfile, mode='w', encoding='utf-8') as f:
        print('=====================Begin====================')
        f.write('=====================Begin====================\n')
        i = 1
        for key, value in it:
            num = 'Record ' + str(i) + '\n'
            f.write(num)
            try:
                recordline = 'key: ' + str(key) + '\r\n' + 'value:' + str(value) + '\r\n'

                print(i)
                print(recordline)
                f.writelines(recordline)

            except Exception as e:
                estr = 'Record ' + str(i) + ', key:' + key.decode('utf-8') + ', decode wrong.  ' + str(e)
                print(estr)
                f.writelines(estr)
                try:
                    undecodelist.append((key, value))

                except Exception as e:
                    print(str(i) + ', key:' + key.decode('utf-8') + ', insert into list wrong.  ' + str(e))
                    # continue

            i += 1
        f.write('=====================end====================')
        print('=====================end====================')

# write faildecoded key,value
def _writefaildecodedkv(undecodedfile, undecodelist):
    j = 1
    print('Begin print undecoded record, total:{num} \n'.format(num=len(undecodelist)))

    with open(undecodedfile, mode='w') as f:
        try:
            for record in undecodelist:
                print('record{j}:\n'.format(j=j))
                key = record[0]
                value = record[1]
                print(key, ':', value, '\n')

                keystr = key.decode('utf-8')
                valuestr = value.decode('utf-8')
                #valuestr = value.decode('ASCII')

                f.write('Begin write undecoded record:\n', encoding='utf-8')
                f.write('Record' + str(j) + ':\n', encoding='utf-8')
                f.write(keystr + ':::' + valuestr)
                j += 1
            print('End print undecoded record.')

        except Exception as e:
            estr = str(j) + ', key:' + key.decode('utf-8') + ', write into file wrong.  ' + str(e)
            print(estr)

# write decoded key,value
def _writedecodedkv(decodedfile, it):
    undecodelist = []  # fail decoded list
    with open(decodedfile, mode='w') as f:
        print('=====================Begin====================')
        f.write('=====================Begin====================')
        i = 1
        for key, value in it:
            num = 'Record ' + str(i) + '\n'
            f.write(num)
            try:
                keystr = key.decode('utf-8')
                valuestr = value.decode('utf-8')


                print(i)
                #if (keystr.find('whatsapp') > -1):
                recordline = 'key: ' + keystr + '\n' + 'value:' + valuestr + '\n'
                print(recordline)
                f.write(recordline)

            except Exception as e:
                estr = str(i) + ', key: ' + keystr + '\n' + 'value:' + str(value) + '\n' ', decode wrong.  ' + str(e)
                print(estr)
                f.writelines(estr)

                try:
                    undecodelist.append((key, value))

                except Exception as e:
                    print(str(i) + ', key:' + key.decode('utf-8') + ', insert into list wrong.  ' + str(e))
                    # continue
            i += 1
        f.write('=====================end====================')
        print('=====================end====================')
    return undecodelist

# write decoded whatsapp key,value
def _writedecodedwhatsappkv(it):
    undecodelist = []  # fail decoded list
    with open(decodedfile, mode='w', encoding='utf-8') as f:
        print('=====================Begin====================')
        f.write('=====================Begin====================')
        i = 1
        for key, value in it:
            num = 'Record ' + str(i) + '\n'
            f.write(num)
            try:
                # keystr = key.decode('utf-8')
                # truevalue = value.split(b'\x01')[0]
                # valuestr = truevalue.decode('utf-8')
                keystr = bytes.decode(key, encoding='utf-8')
                print(i)
                print('key: ' + str(key) + '\r\n' + 'value:' + str(value) + '\r\n')

                if (keystr.find('whatsapp') > -1):
                    valuestr = bytes.decode(value, encoding='utf-8')
                    recordline = 'key: ' + keystr + '\n' + 'value:' + valuestr + '\n'
                    f.writelines(recordline)

            except Exception as e:
                estr = str(i) + ', key:' + key.decode('utf-8') + ', decode wrong.  ' + str(e)
                print(estr)
                f.writelines(estr)
                try:
                    undecodelist.append((key, value))

                except Exception as e:
                    print(str(i) + ', key:' + key.decode('utf-8') + ', insert into list wrong.  ' + str(e))
                    # continue
            i += 1
        f.write('=====================end====================')
        print('=====================end====================')
    return undecodelist


if __name__ == '__main__':
    path0 = os.getcwd()  # get current path
    path = os.path.split(os.path.realpath(__file__))[0]
    dbpath = path + "/Local Storage/leveldb";
    str4bytesfile = path + '/str4bytesCookieContent.dat'
    decodedfile = path + '/decodedCookieContent.dat'
    undecodedfile = path + '/undecodedCookieContent.dat'

    #get leveldb object
    db = plyvel.DB(dbpath)

    #get iterator
    it = db.iterator()
    #read key,value (type is bytes); decode by utf-8 ; write into file
    undecodelist = _writedecodedkv(decodedfile, it)
    it.close()


    it = db.iterator()
    # read key,value (type is bytes); force convert to str ; write into file
    _writeforcestrkv(str4bytesfile, it)
    it.close()

    db.close()

    # write fail decoded key,value pair into file. (a lot of hex ,eg. x08xa1xe3...)
    _writefaildecodedkv(undecodedfile, undecodelist)

