class dmt:

    import struct
    import binascii
    import os

    def __init__(self,data=None):
        self.load(data)

    def load(self,data):
        self.whole_dmt = data
        self.unpack()

    def dump(self):
        print(self.whole_dmt)

    def unpack(self):
        if self.whole_dmt:
            l=len(self.whole_dmt) # Or `self.total_msg_len` might work. Should check that.
        self.len = l
        # Decode header
        self.header = self.whole_dmt[6:10]
        self.body = self.whole_dmt[10:]

        self.stn_name = self.header[0][25:51].rstrip()
        self.stn_country = self.header[1][25:50].rstrip()
        self.stn_lat = self.header[0][61:].rstrip()
        self.stn_lon = self.header[1][61:].rstrip()

        self.stn_jasl = self.header[2][25:46].rstrip()
        self.stn_timemeridian = self.header[2][61:].rstrip().split('(')
        #print(self.stn_timemeridian)
        if self.stn_timemeridian[0] == 'GMT':
            self.stn_timezone = 'GMT'
        else:
            self.stn_timezone = self.header[2][61:].rstrip().split('(')[1][:-1].replace(" ", "").replace("hr","")


        
        #self.stn_gloss = self.header[3][25:34].rstrip()
        
        if "TOGA" in self.header[3]:
            #print("T")
            self.stn_gloss = self.header[3][25:34].strip()
            self.stn_originatornum = 'none'
            self.stn_toga = self.header[3][42:53].strip()
            self.stn_nodc = self.header[3][61:].strip()
        elif "WOCE" in self.header[3]:
            #print("T")
            self.stn_gloss = self.header[3][25:34].strip()
            self.stn_originatornum = 'none'
            self.stn_toga = self.header[3][42:53].strip()
            self.stn_nodc = self.header[3][61:].strip()

        elif "riginator" in self.header[3]:
            #print("O")
            self.stn_gloss = self.header[3][25:29].strip()
            self.stn_originatornum = self.header[3][28:53].split(':')[1].strip()
            self.stn_toga = 'none'
            self.stn_nodc = self.header[3][61:].strip()
        
        self.sources = self.body[0:30]
        #cidx = [idx for idx, s in enumerate(self.sources) if 'Originator   :' in s][0]
        cidx = [idx for idx, s in enumerate(self.sources) if 'Origi' in s][0]

        #print(cidx)
        oidx = [idx for idx, s in enumerate(self.sources[cidx:]) if 'Original Data:' in s][0]
        
        self.contributor = [s[28:].strip() for s in self.sources[0:cidx]]
        self.originator = [s[28:].strip() for s in self.sources[cidx:cidx+oidx]]
        # insert body decoding here
    


def module_unit_test():
    try:
        with open("./test2.dmt") as f:
            foo = f.readlines()
            M = dmt(foo)
            M.unpack()
            #print(foo)
    except EnvironmentError:
        print('error')

    #M = dmt(foo)
    #print(M.len)
    #print ("Loading dmt")
    print(M.contributor)
    print(M.originator)
    #print(M.stn_nodc)
    
    #M.unpack()
    #print(M.len)



if __name__ == '__main__':
    #import os
    #print(os.getcwd())
    module_unit_test()
