from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *

import re
# Create your views here.
def load(request):
    mem1list = []
    mem2list = []
    reglist = Register.objects.all()
    memlist = Memory.objects.all()
    instrlist = Codes.objects.all()
    executemips()
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
    # i = 0
    # j = 2574
    ilist = Codes.objects.all()
    ilist.delete()
    olist = Opcodetable.objects.all()
    olist.delete()
    plist = Piplnsrcdest.objects.all()
    plist.delete()
    # rlist = Register.objects.all()
    # mlist = Memory.objects.all()
    # for r in rlist:
    #     if r.regval != "0000000000000000":
    #         r.regval = "0000000000000000"
    #         r.save()
    # for m in mlist:
    #     if m.memval != "00":
    #         m.memval = "00"
    #         m.save()
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
            pip = Piplnsrcdest.objects.create(instrnum=i,instrc=c.instruction,dest="",src1=spl[1],src2=dest[1].replace(")",""),label=c.label,stat=0)
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
            print("LABEL ", lbl)
            if len(lbl) > 1:
                errorlabel = True
                line = Codes.objects.filter(label=label)[:1].get().id + 1
                context = {
                    'errorlabel': errorlabel,
                    'line': line,
                }
                return render(request, 'mips/index.html', context)
            if len(lbl) == 0:
                print("EMPTY")
                errorlabel = True
                line = l.id + 1
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

        offsetop = offsetop.zfill(16)                        # zero extend

        opc = inop
        opc = opc + baseop
        opc = opc + rtop
        opc = opc + offsetop
        
        temp = int(opc,2)                                  # binary to hex
        opc = hex(temp)[2:]

        opc = opc.zfill(8)                            # zero extend

        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=baseop,rt=rtop,imm=offsetop)
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save()
        
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

        immop = immop.zfill(16)                          # zero extend

        
        opc = str(inop)
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + immop
        
        temp = int(opc,2)                                 # binary to hex
        opc = hex(temp)[2:]

        opc = opc.zfill(8)                              # zero extend
        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=immop)
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save()
        
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

        opc = opc.zfill(8)                              # zero extend

        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=(rdop+saop+funcop))
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save()
        
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

        offset = offset.zfill(16)        # zero extend

        
        opc = inop
        opc = opc + rsop
        opc = opc + rtop
        opc = opc + offset
        
        temp = int(opc,2)                                 # binary to hex
        opc = hex(temp)[2:]

        opc = opc.zfill(8)                               # zero extend

        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=offset)
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save()
        
    elif cmd == "J":                                      # J
        opc = "000010"                                    # opcode(6)
        jlbl = parts[1].replace(",","")                   # label/instruction index
        
        label = Codes.objects.filter(label=jlbl).get()
        
        lbl = label.address                              # get label/instruction index address
        lbl = int(lbl,16)                                # hex to binary
        lbl = str(int(lbl)/4)                            # address / 4
        lbl = lbl.split(".")[0]                          # remove decimal point
        
        lbl = "{0:b}".format(int(lbl))

        lbl = lbl.zfill(26)                             # zero extend

        
        opc = opc + lbl
        
        temp = int(opc,2)                               # binary to hex
        opc = hex(temp)[2:]

        opc = opc.zfill(8)                           # zero extend

        
        opco = Opcodetable.objects.create(instrc=instrc,opcode=opc.upper(),rs=lbl[:5],rt=lbl[5:10],imm=lbl[10:])
        opco.save()
        
        codes_obj.rep = opc.upper()
        codes_obj.save()
def pipelnmap():
    arrpln = []
    plist = Piplnsrcdest.objects.all()
    arrpln.append(["IF", "ID", "EX", "MEM", "WB"])
    counter = 1
    poslabel = 0
    amij = 0
    skipcount = -1

    while counter != len(plist):
        branch = 0
        complain = 0
        lstoappend = []
        previnstr = Piplnsrcdest.objects.filter(instrnum=counter - 1).get().instrc
        print(previnstr, "previnstr")

        if "BGTZC" in previnstr or "J" in previnstr:
            poslabel = Piplnsrcdest.objects.filter(label=previnstr.split(" ")[-1]).get().instrnum

            if "J" in previnstr:
                ###NEED TO CHECK EXECUTE 3 LINES THEN IF MORE THAN 3 LINES APPEND [] UNTIL POSITIONOFLABEL
                amij = 3
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
            #need to fix status to become == 1
            elif "BGTZC" in previnstr and Piplnsrcdest.objects.filter(instrnum=counter - 1).get().stat == 1:
                branch = 1
                for obj in arrpln[-1]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "ID":
                        lstoappend.append("IF")
                    if obj == "EX" or obj == "MEM":
                        lstoappend.append("*")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")
                arrpln.append(lstoappend)
                for i in range(0, poslabel - counter - 1):
                    arrpln.append(["SKIP"])
                lstoappend = []
                print(arrpln[-(poslabel - counter)], "BEF")
                for obj in arrpln[-(poslabel - counter)]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")
                lstoappend.append("IF")
                lstoappend.append("ID")
                lstoappend.append("EX")
                lstoappend.append("MEM")
                lstoappend.append("WB")
                arrpln.append(lstoappend)
                counter = poslabel + 1

            else:  # BRANCH NOT TAKEN

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
            print("DO FREEZE")
        elif (amij == 1):
            if (counter < poslabel):
                lstoappend.append("SKIP")
                skipcount -= 1
            else:
                amij = 0
                print("skip " + str(skipcount))
                print(arrpln[skipcount])
                for obj in arrpln[skipcount]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "ID":
                        lstoappend.append("IF")
                    if obj == "EX":
                        lstoappend.append("ID")
                    if obj == "MEM":
                        lstoappend.append("EX")
                    if obj == "WB":
                        lstoappend.append("MEM")
                        lstoappend.append("WB")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")
                skipcount = -1
        else:
            if (amij > 1):
                amij -= 1
            prevobj = Piplnsrcdest.objects.filter(instrnum=counter - 1).get()
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

        if branch == 0:
            print("NON")
            arrpln.append(lstoappend)
            counter += 1
    return arrpln
def pipelinemap(request):
    arrpln = pipelnmap()
    maxsize = len(arrpln[-1])
    for a in arrpln:
        if len(a) < maxsize :
            for i in range(0,maxsize-len(a)):
                a.append(" ")

    plist = Codes.objects.all()
    if request.method == 'GET':
        cycle = []
        data = request.GET.get('singleexec')
        fulldata = request.GET.get('fullexec')
        if data != None and int(data) <= maxsize:
            for a in arrpln:
                cycle.append(a[int(data)-1])

            context = {
                'cycle': cycle,
            }
            return JsonResponse(context)
        if fulldata != None:

            context = {
                'arrpln': arrpln,
            }

            return JsonResponse(context)

    context={
        'plist':plist,
        'maxsize': maxsize,
    }
    return render(request, 'mips/pipeline.html', context)

# CODE FOR INTERNAL MIPS64 REGISTERS PIPELINE
def IF(instrc, pc):
    theif=[]
    
    op = Opcodetable.objects.filter(instrc=instrc).get()
    
    ir = op.opcode              #if/id.ir
    pc = pc                     #if/id.pc
    npc = pc                    #if/id.npc
    
    theif.append(ir)
    theif.append(npc)
    theif.append(pc)
    
    return theif

def ID(instrc, theif):
    theid=[]
    
    op = Opcodetable.objects.filter(instrc=instrc).get()
    a = Register.objects.filter(regnum = op.rs.replace("R","")).get().regval.zfill(16)
    #a = op.rs                        # id/ex.a
    #b = op.rt                        # id/ex.b
    b = Register.objects.filter(regnum = op.rt.replace("R","")).get().regval.zfill(16)
    imm = op.imm.zfill(16)           # id/ex.imm
    npc = theif[1]                   # id/ex.npc
    ir = theif[0]                    # id/ex.ir
    
    theid.append(op)
    theid.append(a)
    theid.append(b)
    theid.append(imm)
    theid.append(npc)
    theid.append(ir)
    
    return theid

def EX(instrc, theid):
    theex=[]
    
    b = theid[2]
    ir = theid[5]
    
    parts = instrc.split(" ")
    instrc = parts[0]
    
    if("J" in instrc):                                      # Jump instruction
        aluo = bin(theid[3] << 2)
        cond = 1
    elif("LD" in instrc or "SD" in instrc):                 # Load/Store instruction
        aluo = theid[1] + theid[3]
        cond = 0
    elif("BGTZC" in instrc):                                # Branch instruction
        pass
        aluo = theid[4] + bin(theid[3] << 2)
        # cond = a op 0 (do operation)
    else:                                                   # ALU instruction
        #if():
            #aluo = theid[1] func theid[2] (do function)
        #else:
            #aluo = theid[1] op theid[3] (do operation)
        cond = 0
        
    theex.append(aluo)
    theex.append(b)
    theex.append(ir)
    theex.append(cond)
    
    return theex

def MEM(instrc, theex):
    themem=[]
        
    parts = instrc.split(" ")
    instrc = parts[0]
    
    ir = theex[2]                               #mem/wb.ir
    
    if("LD" in instrc):                         #load instruction
        #lmd = theex[0] # supposedly mem of aluoutput
        lmd = Memory.objects.filter(address=theex[0]).get().memval
        themem.append(lmd)
    elif("SD" in instrc):                       #store instruction
        # mem of aluoutput = theex[1]
        memval = Memory.objects.filter(address=theex).get()  # ano dapat si theex???
        memval.memval = theex[1]
        memval.save()
        themem.append(memalu)
    else:
        aluo = theex[0]
        themem.append(aluo)
        
    themem.append(ir)
    
    return themem

def WB(instrc, src2, themem):
    
    parts = instrc.split(" ")
    instrc = parts[0]
    
    thewb=[]
    if("R" in src2 and "LD" not in instrc):                                       #reg-reg
        pass
        # reg[mem/wb.ir 11..15] = themem[1] #aluoutput
    elif("#" in src2 and "LD" not in instrc):                                     #reg-imm
        pass
        # reg[mem/wb.ir 16..20] = themem[1] #aluoutput
    elif("LD" in instrc):                                                          #load
        pass
        # reg[mem/wb.ir 16..20] = themem[1] # lmd
        
    thewb.append(reg)
    
    return thewb

def pipeline(request):
    plist = Piplnsrcdest.objects.all()
    #oplist = Opcodetable.objects.all()
    pc = "0000000000000000"
    cycles = []
    
    # write algo here
    # call the functions if, id, ex, mem, wb when needed
    # all cycles will be placed in cycles list
    
    context={'cycles':cycles}
    return render(request, 'mips/pipln.html', context)

def executemips():
    pipelist = Piplnsrcdest.objects.all()
    reglist = Register.objects.all()
    memlist = Memory.objects.all()
    
    
    counter = 0
    jump = 0
    
    tempreglist = []
    tempmemlist = []
    instruclist = []
    
    for reg in reglist:
        tempreglist.append(reg.regval)
        
    for mem in memlist:
        tempmemlist.append(mem.memval)
        
    while counter < len(pipelist):
        print(pipelist[counter].instrc)
        print("SOURCE1", pipelist[counter].src1)
        print("SOURCE2", pipelist[counter].src2)
        print("DEST", pipelist[counter].dest)
        print("LABEL", pipelist[counter].label)
        print(counter)
        pip = pipelist[counter].instrc
        pipinst = pip.split(" ")
        print(pipinst[0])
#        print(counter)
    
        if jump == 1:
            pips = pipelist[counter-1].instrc
            label = (pipelist[counter-1].instrc).split(" ")[1]
            print("LABEL ",label)
            print("PIPS", pips)
            intnum = Piplnsrcdest.objects.filter(label=label).get().instrnum
            counter = intnum
            jump = 0
            print("JUMP", intnum)
            print("COUNTER", counter, pips)
            
            #get the label where jump is going to execute
            #go to the label
            #current counter will go to the label
    
        if "DADDU" in pipinst[0]:
            src1 = pipelist[counter].src1
            src2 = pipelist[counter].src2
            dest = pipelist[counter].dest
            s1 = src1.split("R")
            s2 = src2.split("R")
            de = dest.split("R")
            print (s1, s2, de)
            rs = tempreglist[int(s1[1])]
            rs = int(rs, 16)
            print(rs)
            rt = tempreglist[int(s2[1])]
            rt = int(rt, 16)
            print(rt)
            des = rs + rt
            print(des)
            tempreglist[counter] = format(des, 'x').zfill(16)
            print(tempreglist[counter])
            
        if "DADDIU" in pipinst[0]:
            src1 = pipelist[counter].src1
            src2 = pipelist[counter].src2
            dest = pipelist[counter].dest
            s1 = src1.split("R")
            s2 = (pipelist[counter].instrc).split("#")
            s2 = s2[1]
            de = dest.split("R")
            print (s1, s2, de)
            rs = tempreglist[int(s1[1])]
            rs = int(rs,16)
            rt = int(s2, 16)
            print(rt)
            des = rs + rt 
            print("DES",des)
            tempreglist[counter] = format(des, 'x').zfill(16).upper()
            print ("DITO ME CIZT" + '\n',tempreglist[counter])
        if "XORI" in pipinst[0]:
            src1 = pipelist[counter].src1
            src2 = pipelist[counter].src2
            dest = pipelist[counter].dest
            
            s1 = src1.split("R")
            s2 = (pipelist[counter].instrc).split("#")
            s2 = s2[1]
            de = dest.split("R")
            print(s1,s2,de)
            
            rs = tempreglist[int(s1[1])]
            rs = int(rs,16)
            rt = int(s2,16)
            des = bool(rs) ^ bool(rt)
            print("DES",des)
            tempreglist[counter] = format(des, 'x').zfill(16).upper()
            print ("DITO ME CIZTT" + '\n',tempreglist[counter])
        
        if "SLT" in pipinst[0]:
            src1 = pipelist[counter].src1
            src2 = pipelist[counter].src2
            dest = pipelist[counter].dest
            s1 = src1.split("R")
            s2 = src2.split("R")
            de = dest.split("R")
            print(s1,s2,de)
            
            rs = tempreglist[int(s1[1])]
            rt = tempreglist[int(s2[1])]
            
            if rs < rt:
                des = 1
            else:
                des = 0
            
            tempreglist[counter] = format(des,'x').zfill(16).upper()
            
        if "J" in pipinst[0]:
            jump = 1
            
        if "LD" in pipinst[0]:
            src1 = pipelist[counter].src1
            dest = pipelist[counter].dest
            
            s1 = src1.split("R")
            s2 = ((pipelist[counter].instrc).split(" ")[2]).split("(")[0]
            de = dest.split("R")
            print(s1,s2,de)
            maxctr = 8
            
            rs = tempreglist[int(s1[1])]
            rt = int(s2) + maxctr
            print ("RS", rs)
            print ("RT", rt)
            rt = str(rt)
            print (rt)
            membox = []
            mem = Memory.objects.filter(address=rt).get().memval
            print (mem)
            c = 0
            while maxctr != 0:
                rt = int(rt) - 1
                rt = str(rt)
                mem = Memory.objects.filter(address=rt).get().memval
                membox.append(mem)
                maxctr-=1
                c+=1
                print ("MAXCTR" , maxctr)
            
            print (''.join(membox))
            

            
            
        
        if "SD" in pipinst[0]:
            pass
            
            
        
            
        
        counter+=1
#        
#    while counter != len(pipelist):
#        if "DADDIU" in currins:
#            pass
#        counter+=1