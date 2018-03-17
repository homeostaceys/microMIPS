from django.shortcuts import render, redirect
from django.http import HttpResponse
import binascii

from .models import *

import re
# Create your views here.
def load(request):
    return render(request, 'mips/load.html')
def index(request):

    return render(request,'mips/index.html')

def inputcode(request):
    if (request.method == "POST"):
        codearea = request.POST["codearea"]
        request.session['codearea'] = codearea
        list = codearea.split("\r\n")
        print(list)
    return HttpResponse('Success')

def check(request):
    codearea = request.session['codearea']
    list = codearea.split("\r\n")
    print(list)
    #not yet done need to do line per line check and label check else prompt an error
    return render(request, 'mips/load.html')

def errorCheck(instr):
    regex = r"^((\w+:( )?)?((LD|SD) R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( ([0-9A-F]){4})(\(R([0-9]|1[0-9]|2[0-9]|3[0-1])\)))$|^((\w+:( )?)?(DADDIU|XORI)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9A-F])){4}))$|^((\w+:( )?)?(DADDU|SLT)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( R([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\w+:( )?)?(BGTZC R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( \w+))$|^((\w+:( )?)?(J \w+))$"

    if re.search(regex, instr): # need to add checking of labels
        return True

    return False

#def opcode(instr):
    
# di pa 'to tapos lol
def opcode(instrc, instrc_num):
    if ":" in instrc:
        label = instrc.split(":")[0]
        instrc = instrc.split(":")[1] #DADDIU R1, R2, R4
    parts = instrc.split(" ")
    cmd = parts[0]
    # parse and load for LD or SD
    if cmd == "LD" or cmd == "SD":
        base = parts[2].split("()")[1].replace(")","")
        rt = parts[1].replace(",", "")
        offset = parts[2].split("(")[0]
        
        if cmd == "LD":
            inop = "110111"
        else:
            inop = "111111"
        
        baseop = '{0:05b}'.format(base)                 # Integer to binary
        rtop = '{0:05b}'.format(rt)                     # Integer to binary
        offsetop = binary(binascii.hexlify(offset))     # hex to binary
        
        opc = inop
        opc = opc + baseop
        opc = opc + rtop
        opc = opc + offsetop
        
        opc = binascii.hexlify(opc)
        
        return opc
        
    # parse and load for DADDIU or XORI
    elif cmd == "DADDIU" or cmd == "XORI":
        if "0x" in parts[3]:
            parts[3] = parts[3].replace("0x","")
        else:
            parts[3] = parts[3].replace("#","")
            
        rs = parts[2].replace(",", "")
        rt = parts[1].replace(",", "")
        imm = parts[3]
        
        if cmd == "DADDIU":
            inop = "011001"
        else:
            inop = "001110"
            
        rsop = '{0:05b}'.format(rs)                     # Integer to binary
        rtop = '{0:05b}'.format(rt)                     # Integer to binary
        immop = binary(binascii.hexlify(imm))           # hex to binary
        
        opc = inop
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + immop
        
        opc = binascii.hexlify(opc)
        
        return opc
        
    # parse and load for DADDU or SLT
    elif cmd == "DADDU" or cmd == "SLT":
        rs = parts[2].replace(",","")
        rt = parts[3]
        rd = parts[1].replace(",","")
	# parse and load for BGTZC
    elif cmd == "BGTZC":
        rt = parts[1].replace(",","")
        offset = parts[2]
	# parse and load for J
    else:
        a = "a"
         #opcode[instrc_num][1] = Scenario5(cmd, instrc_num)