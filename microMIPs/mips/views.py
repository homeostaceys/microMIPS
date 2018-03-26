from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

import re
# Create your views here.
def load(request):
    mem1list = []
    mem2list = []
    reglist = Register.objects.all()
    memlist = Memory.objects.all()
    instrlist = Codes.objects.all()
    for m in memlist:
        if int(m.address,16) >= 0 and int(m.address,16) < 4096:
            mem1list.append(m)
        else:
            mem2list.append(m)

    context={
        'reglist':reglist,
        'mem1list':mem1list,
        'mem2list': mem2list,
        'instrclist':instrlist,

    }
    return render(request, 'mips/load.html', context)
def reset():
    i = 0
    j = 2574
    ilist = Codes.objects.all()
    ilist.delete()
    olist = Opcodetable.objects.all()
    olist.delete()
    plist = Piplnsrcdest.objects.all()
    plist.delete()
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

def resetindex(request):
    i = 0
    j = 2574
    ilist = Codes.objects.all()
    ilist.delete()
    olist = Opcodetable.objects.all()
    olist.delete()
    plist = Piplnsrcdest.objects.all()
    plist.delete()
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
    return redirect("/")

def resetdb(request):
    i = 0
    j = 2574
    ilist = Codes.objects.all()
    ilist.delete()
    olist = Opcodetable.objects.all()
    olist.delete()
    plist = Piplnsrcdest.objects.all()
    plist.delete()
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
    olist = Opcodetable.objects.all()
    olist.delete()
    request.session['codearea'] = ""
    return redirect('/')

def pipeline(request):

    return render(request,'mips/pipeline.html')

def index(request):
    try:
        request.session['codearea']
    except:
        resetdb(request)
    
    return render(request,'mips/index.html')

def inputcode(request):
    if (request.method == "POST"):
        codearea = request.POST["codearea"]
        request.session['codearea'] = codearea
        list = codearea.split("\r\n")
    return HttpResponse('Success')
def editmem(request):
    if (request.method == "POST"):
        memadd = request.POST['memadd']
        memvalue = request.POST['memvalue']
        print(memadd,"",memvalue)
        editcont = Memory.objects.get(address=memadd)
        editcont.memval = memvalue.upper()
        editcont.save()
    return HttpResponse('Success')
def editreg(request):
    if (request.method == "POST"):
        regnum = request.POST['regnum']
        regval = request.POST['regval']
        print(regnum,"",regval)
        editcont = Register.objects.get(regnum=regnum)
        editcont.regval = regval.upper()
        editcont.save()
    return HttpResponse('Success')
def piplineparse():
    codes_obj = Codes.objects.all()
    i = 0
    for c in codes_obj:
        intrc = c.instruction
        if ": " in intrc:
            instr = intrc.split(": ")[1]
        elif ":" in intrc:
            instr = intrc.split(":")[1]
        else:
            instr = intrc
        spl = instr.replace(",","")
        spl = spl.split(" ")
        if "DADDIU" in spl[0] or "XORI" in spl[0]:
            pip = Piplnsrcdest.objects.create(instrnum=i,instrc=c.instruction,dest=spl[1],src1=spl[2],src2="",label=c.label,stat=0)
            pip.save()
        elif "LD" in spl[0]:
            src = spl[2].split("(")
            pip = Piplnsrcdest.objects.create(instrnum=i,instrc=c.instruction,dest=spl[1],src1=src[1].replace(")",""),src2="",label=c.label,stat=0)
            pip.save()
        elif  "DADDU" in spl[0] or "SLT" in spl[0]:
            pip = Piplnsrcdest.objects.create(instrnum=i,instrc=c.instruction,dest=spl[1],src1=spl[2],src2=spl[3],label=c.label,stat=0)
            pip.save()
        elif "SD" in spl[0]:
            dest = spl[2].split("(")
            pip = Piplnsrcdest.objects.create(instrnum=i,instrc=c.instruction,dest=dest[1].replace(")",""),src1=spl[1],src2="",label=c.label,stat=0)
            pip.save()
        elif "BGTZC" in spl[0]:
            pip = Piplnsrcdest.objects.create(instrnum=i,instrc=c.instruction,dest="",src1=spl[1],src2="",label=c.label,stat=0)
            pip.save()
        else: #J
            pip = Piplnsrcdest.objects.create(instrnum=i, instrc=c.instruction, dest="", src1="", src2="",label=c.label,stat=0)
            pip.save()
        i+=1
            

def check(request):
    error = None
    line = None
    reset()
    codearea = request.session['codearea']
    codearea = codearea.upper()
    list = codearea.split("\r\n")
    i = 0
    while i < len(list):
        instr = ""
        label = ""
        status = 0
        if errorCheck(list[i]) == True:
            if ": " in list[i]:
                label = list[i].split(": ")[0]
                instr = list[i].split(": ")[1]
            elif ":" in list[i]:
                label = list[i].split(":")[0]
                instr = list[i].split(":")[1]
            else:
                instr = list[i]

            if "J" in instr or "BGTZC" in instr:
                status = 1
            code = Codes.objects.create(id=i, address=format(i * 4, 'x').zfill(4), rep="", label=label,
                                        instruction=instr,
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
            if len(lbl) > 1:
                errorlabel = True
                line = Codes.objects.filter(label=label)[:1].get().id + 1
                print("False")
                context = {
                    'errorlabel': errorlabel,
                    'line': line,
                }
                return render(request, 'mips/index.html', context)
        except IndexError:
            errorlabel = True
            line = l.id + 1
            print("False")
            context = {
                'errorlabel': errorlabel,
                'line': line,
            }
            return render(request, 'mips/index.html', context)


    codes_obj = Codes.objects.all()
    for e in codes_obj:
        opcode(e)
        
    piplineparse()
    return redirect('/load/')


def errorCheck(instr):
    regex = r"^(\w+:( )?)$|((\w+:( )?)?((LD|SD) R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( ([0-9A-F]){4})(\(R([0-9]|1[0-9]|2[0-9]|3[0-1])\)))$|^((\w+:( )?)?(DADDIU|XORI)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9A-F])){4}))$|^((\w+:( )?)?(DADDU|SLT)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( R([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\w+:( )?)?(BGTZC R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( \w+))$|^((\w+:( )?)?(J \w+))$"
    if re.search(regex, instr): # need to add checking of labels
        return True

    return False

  
def opcode(codes_obj):
    instrc = codes_obj.instruction                          # get whole instruction
    parts = instrc.split(" ")                               # split
    cmd = parts[0]                                          # get instruction
    
    if cmd == "LD" or cmd == "SD":                          # LD or SD
        base = parts[2].split("(")[1].replace(")","")       # get base
        rt = parts[1].replace(",", "")                      # get rt
        offset = parts[2].split("(")[0]                     # get offset
        
        if cmd == "LD":
            inop = "110111"                                 # opcode(6)
        else:
            inop = "111111"                                 # opcode(6)
            
        base = base.replace("R", "")
        rt = rt.replace("R", "")
        
        baseop = '{0:05b}'.format(int(base))                # Integer to binary
        rtop = '{0:05b}'.format(int(rt))                    # Integer to binary
        offsetop = "{0:16b}".format(int(offset,16))         # hex to binary
        offsetop = offsetop.replace(" ", "")
        
        while len(offsetop) < 16:                           # zero extend
            offsetop = "0" + offsetop
        
        opc = inop
        opc = opc + baseop
        opc = opc + rtop
        opc = opc + offsetop
        
        temp = int(opc,2)                                  # binary to hex
        opc = hex(temp)[2:]
        
        while len(opc) < 8:                                # zero extend
            opc = "0" + opc
        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=baseop,rt=rtop,imm=offsetop)
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save(update_fields=['rep'])
        
    elif cmd == "DADDIU" or cmd == "XORI":                 # DADDIU or XORI
        if "0x" in parts[3]:
            parts[3] = parts[3].replace("0x","")
        else:
            parts[3] = parts[3].replace("#","")
            
        rs = parts[2].replace(",", "")                     # get rs
        rt = parts[1].replace(",", "")                     # get rt
        imm = parts[3]                                     # get imm
        
        if cmd == "DADDIU":
            inop = "011001"                                # opcode(6)
        else:
            inop = "001110"                                # opcode(6)  
        
        rs = rs.replace("R", "")
        rt = rt.replace("R", "")
        
        rsop = '{0:05b}'.format(int(rs))                  # Integer to binary
        rtop = '{0:05b}'.format(int(rt))                  # Integer to binary
                  
        immop = "{0:16b}".format(int(imm,16))             # hex to binary
        immop = immop.replace(" ", "")
        
        while len(immop) < 16:                            # zero extend
            immop = "0" + immop
        
        opc = str(inop)
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + immop
        
        temp = int(opc,2)                                 # binary to hex
        opc = hex(temp)[2:]   
        
        while len(opc) < 8:                               # zero extend
            opc = "0" + opc
        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=immop)
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save(update_fields=['rep'])
        
    elif cmd == "DADDU" or cmd == "SLT":                  # DADDU or SLT
        rs = parts[2].replace(",","")
        rt = parts[3]
        rd = parts[1].replace(",","")
        
        inop = "000000"                                   # opcode(6)
        
        rs = rs.replace("R", "")
        rt = rt.replace("R", "")
        rd = rd.replace("R", "")
        
        rsop = '{0:05b}'.format(int(rs))                  # Integer to binary
        rtop = '{0:05b}'.format(int(rt))                  # Integer to binary
        rdop = '{0:05b}'.format(int(rd))                  # Integer to binary
        
        saop = "00000"                                    # sa(5)
        
        if cmd == "DADDU":
            funcop = "101101"                             # func(6)
        else:
            funcop = "101010"                             # func(6)
            
        opc = inop
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + rdop
        opc = opc + saop
        opc = opc + funcop
        
        temp = int(opc,2)                                 # binary to hex
        opc = hex(temp)[2:]
        
        while len(opc) < 8:                               # zero extend
            opc = "0" + opc
        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=(rdop+saop+funcop))
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save(update_fields=['rep'])
        
    elif cmd == "BGTZC":                                  # BGTZC
        rt = parts[1].replace(",","")
        blbl = parts[2]                                   # label/offset
        inop = "010111"                                   # opcode(6)
        rsop = "00000"                                    # rs(5)
        rt = rt.replace("R", "")                          # get rt
        rtop = '{0:05b}'.format(int(rt))                  # Integer to binary
        
        label = Codes.objects.filter(label=blbl).get()    
        dest = label.address                              # get dest address
        dest = int(dest,16)                               # hex to binary
        dest = str(int(dest)/4)                           
        dest = dest.split(".")[0]                         # remove decimal point
        
        #label2 = Codes.objects.filter(instruction=instrc).get()
        #pc = label2.address
        pc = codes_obj.address                            # get pc address
        pc = int(pc,16)                                   # hex to binary
        pc = str(int((pc)/4)+1)
        pc = pc.split(".")[0]                             # remove decimal point
        
        offset = (int(dest)-int(pc))/4                    # offset = (DEST - PC) / 4
        offset = "{0:b}".format(int(offset))              # integer to binary

        while len(offset) < 16:                           # zero extend
            offset = "0" + offset
        
        opc = inop
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + offset
        
        temp = int(opc,2)                                 # binary to hex
        opc = hex(temp)[2:]
        
        while len(opc) < 8:                               # zero extend
            opc = "0" + opc
        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=offset)
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save(update_fields=['rep'])
        
    elif cmd == "J":                                      # J
        opc = "000010"                                    # opcode(6)
        jlbl = parts[1].replace(",","")                   # label/instruction index
        
        label = Codes.objects.filter(label=jlbl).get()
        
        lbl = label.address                              # get label/instruction index address
        lbl = int(lbl,16)                                # hex to binary
        lbl = str(int(lbl)/4)                            # address / 4
        lbl = lbl.split(".")[0]                          # remove decimal point
        
        lbl = "{0:b}".format(int(lbl))
        
        while len(lbl) < 26:                             # zero extend
            lbl = "0" + lbl
        
        opc = opc + lbl
        
        temp = int(opc,2)                               # binary to hex
        opc = hex(temp)[2:]
        
        while len(opc) < 8:                             # zero extend
            opc = "0" + opc
        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=lbl[:5],rt=lbl[5:10],imm=lbl[10:])
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save(update_fields=['rep'])

def pipelinemap(request):
    arrpln=[]
    lstoappend =[]
    plist = Piplnsrcdest.objects.all()
    arrpln.append(["IF","ID","EX","MEM","WB"])
    counter = 1
    count= 0
    posjump = 0
    poslabel = 0
    while counter != len(plist):
        complain = 0
        lstoappend = []
        previnstr = Piplnsrcdest.objects.filter(instrnum=counter-1).get().instrc
        print(previnstr,"previnstr")
        if "BGTZC" in previnstr or "J" in previnstr:
            posjump = counter
            poslabel = Piplnsrcdest.objects.filter(label=previnstr.split(" ")[-1]).get().instrnum
            if "J" in previnstr:
                ###NEED TO CHECK EXECUTE 3 LINES THEN IF MORE THAN 3 LINES APPEND [] UNTIL POSITIONOFLABEL
                for obj in arrpln[-1]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "ID":
                        lstoappend.append("IF")
                    if obj == "EX" or obj == "MEM":
                        lstoappend.append("*")
                    if obj == "WB":
                        lstoappend.append("ID")
                        lstoappend.append("EX")
                        lstoappend.append("MEM")
                        lstoappend.append("WB")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")
            if "BGTZC" in previnstr and Piplnsrcdest.objects.filter(label=previnstr.split(" ")[-1]).get().stat == 1:
                #DO BGTZC SINCE IT SHOULD BRANCH
                pass
            else:#BRANCH NOR JUMP NOT TAKEN
                for obj in arrpln[-1]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "ID":
                        lstoappend.append("IF")
                    if obj == "EX" or obj == "MEM":
                        lstoappend.append("*")
                    if obj == "WB":
                        lstoappend.append("ID")
                        lstoappend.append("EX")
                        lstoappend.append("MEM")
                        lstoappend.append("WB")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")
            print(lstoappend)
            print("DO FREEZE")
        else:
            prevobj = Piplnsrcdest.objects.filter(instrnum=counter-1).get()
            currobj = Piplnsrcdest.objects.filter(instrnum=counter).get()
            if prevobj.dest == currobj.src1 or prevobj.dest == currobj.src2:
                complain = 1
            for obj in arrpln[-1]:
                if obj == " " or obj == "IF":
                    lstoappend.append(" ")
                if obj == "ID":
                    lstoappend.append("IF")
                if obj == "EX":
                    lstoappend.append("ID")
                if obj == "MEM":
                    if complain == 1:
                        lstoappend.append("*")
                    else:
                        lstoappend.append("EX")
                if obj == "WB":
                    if complain == 1:
                        lstoappend.append("EX")
                        lstoappend.append("MEM")
                        lstoappend.append("WB")

                    else:
                        lstoappend.append("MEM")
                        lstoappend.append("WB")
                if obj == "*" or obj == "/":
                    lstoappend.append("/")


        arrpln.append(lstoappend)
        counter+=1

    context={'arrpln':arrpln}
    return render(request, 'mips/pipeline.html', context)