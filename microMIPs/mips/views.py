from django.shortcuts import render, redirect
from django.http import HttpResponse
import binascii

from .models import *

import re
# Create your views here.
def load(request):
    reglist = Register.objects.all()
    memlist = Memory.objects.all()
    instrlist = Codes.objects.all()
    context={
        'reglist':reglist,
        'memlist':memlist,
        'instrclist':instrlist,

    }
    return render(request, 'mips/load.html', context)
def reset(request):
    i = 0
    j = 2574
    rlist = Register.objects.all()
    mlist = Memory.objects.all()
    for r in rlist:
        if r.regval != "0000000000000000":
            r.regval = "0000000000000000"
            r.save()
    for m in mlist:
        if m.memval != "00":
            m.memval = "00"
            m.save()

    return redirect('/load/')
def index(request):

    return render(request,'mips/index.html')

def inputcode(request):
    if (request.method == "POST"):
        codearea = request.POST["codearea"]
        request.session['codearea'] = codearea
        list = codearea.split("\r\n")
    return HttpResponse('Success')

def check(request):
    error = None
    line = None
    c = Codes.objects.all()
    c.delete()
    codearea = request.session['codearea']
    codearea = codearea.upper()
    list = codearea.split("\r\n")
    i = 0
    while i < len(list):
        instr = ""
        label = ""
        status = 0
        if errorCheck(list[i]) == True:
            if ":" in list[i]:
                label = list[i].split(":")[0]
                instr = list[i].split(":")[1]
            elif ": " in list[i]:
                label = list[i].split(": ")[0]
                instr = list[i].split(": ")[1]
            else:
                instr = list[i]

            if "J" in instr or "BGTZC" in instr:
                status = 1
            code = Codes.objects.create(id=i,address=format(i * 4, 'x').zfill(4), rep="", label=label, instruction=instr,
                                        status=status)
            code.save()
        else:
            error = True
            line = i + 1
            context = {
                'error': error,
                'line': line,
            }
            return render(request, 'mips/index.html', context)
        i += 1

    branchjumplist = Codes.objects.filter(status=1)
    for l in branchjumplist:

        try:
            lbl = Codes.objects.filter(label=str(l).split(" ")[-1])
            lbl[0]
        except IndexError:
            errorlabel = True
            line = l.id + 1
            print("False")
            context = {
                'errorlabel': errorlabel,
                'line': line,
            }
            return render(request, 'mips/index.html', context)

    return render(request, 'mips/load.html')

def errorCheck(instr):
    regex = r"^((\w+:( )?)?((LD|SD) R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( ([0-9A-F]){4})(\(R([0-9]|1[0-9]|2[0-9]|3[0-1])\)))$|^((\w+:( )?)?(DADDIU|XORI)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9A-F])){4}))$|^((\w+:( )?)?(DADDU|SLT)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( R([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\w+:( )?)?(BGTZC R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( \w+))$|^((\w+:( )?)?(J \w+))$"
    if re.search(regex, instr): # need to add checking of labels
        return True

    return False

def checkRData(regval):
    regex = r"^(([0-9A-Fa-f]{4}){4})$"
    if re.search(regex, regval): # need to add checking of labels
        return True

    return False

def checkMData(memval):
    regex = r"^([0-9A-Fa-f]{2})$"
    if ((int(memval,16) > 0 and int(memval,16) < 4096) and re.search(regex, memval)): # need to add checking of labels
        return True

    return False
  
# di pa 'to tapos lol
def opcode(instrc, instrc_num):
    if ":" in instrc:
        Codes.label = instrc.split(":")[0]              # store label
        instrc = instrc.split(":")[1]
    parts = instrc.split(" ")
    cmd = parts[0]
    
    if cmd == "LD" or cmd == "SD":                      # parse and load for LD or SD
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
        
    elif cmd == "DADDIU" or cmd == "XORI":               # parse and load for DADDIU or XORI
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
        
    elif cmd == "DADDU" or cmd == "SLT":                # parse and load for DADDU or SLT
        rs = parts[2].replace(",","")
        rt = parts[3]
        rd = parts[1].replace(",","")
        
        inop = "000000"
        
        rsop = '{0:05b}'.format(rs)                     # Integer to binary
        rtop = '{0:05b}'.format(rt)                     # Integer to binary
        rdop = '{0:05b}'.format(rd)                     # Integer to binary
        
        saop = "00000"
        
        if cmd == "DADDU":
            funcop = "101101"
        else:
            funcop = "101010"
            
        opc = inop
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + rdop
        opc = opc + saop
        opc = opc + funcop
        
        opc = binascii.hexlify(opc)
        
        return opc
        
    elif cmd == "BGTZC":                                # parse and load for BGTZC
        rt = parts[1].replace(",","")
        offset = parts[2]
        
        inopp = "010111"
        baseopp = "00000"
        rtop = '{0:05b}'.format(rt)                     # Integer to binary
        offsetop = binary(binascii.hexlify(offset))     # hex to binary
        
        opc = inop
        opc = opc + baseop
        opc = opc + rtop
        opc = opc + offsetop
        
        opc = binascii.hexlify(opc)
        
        return opc
        
    else:                                               # parse and load for J
        instrc_num.zfill(16)
        
        opc = inop;
        opc += indexop;
        
        opc = binascii.hexlify(opc)
        
        return opc