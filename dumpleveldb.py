#!/usr/bin/env python

import argparse
import plyvel
import os
import gzip


class LevelDbDump(object):
    def __init__(self):
        self.path0 = os.getcwd()
        self.path = os.path.split(os.path.realpath(__file__))[0] + "/"
        self.undecodelist = ""

        parser = argparse.ArgumentParser(description=os.path.basename(__file__) + " - dumps a leveldb from ./leveldb or from the path you set with '-d' - latest source: https://github.com/cleanworld123/leveldb_read_write_python3")
        parser.add_argument('-d', '--db-path', dest='level_db_path', help='Path to database directory')
        self.args = parser.parse_args()

        if self.args.level_db_path:
            self.dbpath = self.args.level_db_path
        else:
            self.dbpath = self.path + "leveldb"

        self.str4bytesfile = self.path + os.path.basename(__file__) + '_str4bytesCookieContent.dat'
        self.decodedfile = self.path + os.path.basename(__file__) + '_decodedCookieContent.dat'
        self.undecodedfile = self.path + os.path.basename(__file__) + '_undecodedCookieContent.dat'

        self.msg_begin = "===================== BEGIN ===================="
        self.msg_end = "====================== END ====================="

        self.it = ""

        # get leveldb object
        try:
            self.db = plyvel.DB(self.dbpath)
        except:
            print("wrong database path '" + self.dbpath + "' or missing access rights? put it to ./leveldb or set the path with '-d'. use 'dumpleveldb --help' for more help")
            exit(1)

    def run(self):
        # get iterator
        self.it = self.db.iterator()
        # read key,value (type is bytes); decode by utf-8 ; write into file
        self._writedecodedkv()
        self.it.close()

        self.it = self.db.iterator()
        # read key,value (type is bytes); force convert to str ; write into file
        self._writeforcestrkv()
        self.it.close()

        # write fail decoded key,value pair into file. (a lot of hex ,eg. x08xa1xe3...)
        self._writefaildecodedkv()
        self.db.close()

    # write force str(key,value)
    def _writeforcestrkv(self):
        with open(self.str4bytesfile, mode='w', encoding='utf-8') as f:
            print(self.msg_begin)
            f.write(self.msg_begin + '\n')
            i = 1
            for key, value in self.it:
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
                        self.undecodelist.append((key, value))

                    except Exception as e:
                        print(str(i) + ', key:' + key.decode('utf-8') + ', insert into list wrong.  ' + str(e))
                        # continue

                i += 1
            print(self.msg_end)
            f.write(self.msg_end + '\n')

    # write faildecoded key,value
    def _writefaildecodedkv(self):
        j = 1
        print('Begin print undecoded record, total:{num} \n'.format(num=len(self.undecodelist)))

        with open(self.undecodedfile, mode='w') as f:
            try:
                for record in self.undecodelist:
                    print('record{j}:\n'.format(j=j))
                    key = record[0]
                    value = record[1]
                    print(key, ':', value, '\n')

                    keystr = key.decode('utf-8')
                    valuestr = value.decode('utf-8')
                    # valuestr = value.decode('ASCII')

                    f.write('Begin write undecoded record:\n', encoding='utf-8')
                    f.write('Record' + str(j) + ':\n', encoding='utf-8')
                    f.write(keystr + ':::' + valuestr)
                    j += 1
                print('End print undecoded record.')

            except Exception as e:
                estr = str(j) + ', key:' + key.decode('utf-8') + ', write into file wrong.  ' + str(e)
                print(estr)

    # write decoded key,value
    def _writedecodedkv(self):
        self.undecodelist = []  # fail decoded list
        with open(self.decodedfile, mode='w') as f:
            print(self.msg_begin)
            f.write(self.msg_begin + '\n')
            i = 1
            for key, value in self.it:
                num = 'Record ' + str(i) + '\n'
                f.write(num)
                try:
                    keystr = key.decode('utf-8')
                    valuestr = value.decode('utf-8')

                    print(i)
                    # if (keystr.find('whatsapp') > -1):
                    recordline = 'key: ' + keystr + '\n' + 'value:' + valuestr + '\n'
                    print(recordline)
                    f.write(recordline)

                except Exception as e:
                    estr = str(i) + ', key: ' + keystr + '\n' + 'value:' + str(value) + '\n' ', decode wrong.  ' + str(e)
                    print(estr)
                    f.writelines(estr)

                    try:
                        self.undecodelist.append((key, value))

                    except Exception as e:
                        print(str(i) + ', key:' + key.decode('utf-8') + ', insert into list wrong.  ' + str(e))
                        # continue
                i += 1
            print(self.msg_end)
            f.write(self.msg_end + '\n')
        return self.undecodelist

    # write decoded whatsapp key,value
    def _writedecodedwhatsappkv(self):
        self.undecodelist = []  # fail decoded list
        with open(self.decodedfile, mode='w', encoding='utf-8') as f:
            print(self.msg_begin)
            f.write(self.msg_begin + '\n')
            i = 1
            for key, value in self.it:
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
                        self.undecodelist.append((key, value))

                    except Exception as e:
                        print(str(i) + ', key:' + key.decode('utf-8') + ', insert into list wrong.  ' + str(e))
                        # continue
                i += 1
            print(self.msg_end)
            f.write(self.msg_end + '\n')
        return self.undecodelist

if __name__ == '__main__':
    leveldbdump = LevelDbDump()
    leveldbdump.run()
