#!python
# _/_/_/ TGZ Salvage Ver.4.1 _/_/_/
# Written by Y.Hirokawa

import argparse
import subprocess

def parseArg():
    # Parse Arguments
    parser = argparse.ArgumentParser(description='TGZ Salvage Tool')
    parser.add_argument('-i','--INFILE', required=True,       help='Input File')
    parser.add_argument('-s','--SPLIT',  action="store_true", help='Only split TGZ File')
    parser.add_argument('-k','--KEEP',   action="store_true", help='Keep split TGZ File')
    args   = parser.parse_args()

    # Filename
    INFILE = args.INFILE

    # Extract split tgz file (Don't extract split tgz files)
    BSPLIT = args.SPLIT

    # Keep split tgz file
    BKEEP  = args.KEEP

    return INFILE, BSPLIT, BKEEP


def forensic(INPUT,BS,BK):
    print("[INFO] INFILE    : "+str(INPUT))
    print("[INFO] SPLIT-ONLY: "+str(BS))

    # GZIP Header Definition
    GZH0 = "0x1f"
    GZH1 = "0x8b"
    GZH2 = "0x8"
    GZH3 = "0x0"

    # FILE Open
    try:
        with open(INPUT,mode="rb") as f:
            buf = f.read()
    except BASIC_EXCEPTION as e:
        print("[ERROR] "+str(e))

    EOF = len(buf)
    sta = None 
    end = None 
    cnt = 1

    # Scan data
    for i in range(0,EOF):
        h0 = hex(buf[i])

        # Retrieve Data
        if int(i+1) <= EOF-1:
            h1 = hex(buf[i+1])
        else:
            h1 = None

        if int(i+2) <= EOF-1:
            h2 = hex(buf[i+2])
        else:
            h2 = None

        if int(i+3) <= EOF-1:
            h3 = hex(buf[i+3])
        else:
            h3 = None

        # Check GZIP Header 
        if h0 == GZH0 and h1 == GZH1:
            if h2 == GZH2 and h3 == GZH3:
                if sta == None: 
                    sta = i
                else:
                    end = i - 1 

        # Retrieve Data
        if int(i) == int(EOF-1):
            end = i

        ###print("i="+str(i)+" sta="+str(sta)+" end="+str(end)+" dat="+str(h0))

        if sta != None and end != None:
            # Output Split Data to File
            l     = len(INFILE)
            fname = "__"+str(INFILE[0:l-4])+"__"+str(cnt)+".tgz"
            if BS == True:
                print("[INFO] Write split data to "+str(fname))
            try:
                with open(fname,"wb") as f:
                    # End Value of Slice Access Requires Addition of +1
                    f.write(buf[sta:end+1])
            except BASIC_EXCEPTION as e:
                print("[ERROR] "+str(e))

            if BS == False:
                # Extract split file
                log = subprocess.run(["tar","zxvf",fname], capture_output=True, text=True)
                # Stdout of TAR contains extra line feed.  
                print("[INFO] Extract to "+str(log.stdout), end="")

                if BK == False:
                    # Remove split file
                    subprocess.run(["rm","-f",fname])

            sta  = i
            end  = None
            cnt += 1

    return


if __name__ == "__main__":
    INFILE, BS, BK = parseArg()
    forensic(INFILE, BS, BK)
