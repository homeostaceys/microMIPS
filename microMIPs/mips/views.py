from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from operator import xor

from django.http import Http404
import re,copy
# Create your views here.

def error_404(request):
        print("hi")
        return render(request,'mips/404.html')
def e404():
    print("hello")
    return redirect('/')
def error_500(request):
        data = {}
        return render(request,'mips/500.html', data)
    
def load(request):
    print("LOAD")
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
    ilist = Codes.objects.all()
    ilist.delete()
    olist = Opcodetable.objects.all()
    olist.delete()
    plist = Piplnsrcdest.objects.all()
    plist.delete()

def resetindex(request):
  
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
        editcont = Memory.objects.get(address=memadd)
        editcont.memval = memvalue.upper()
        editcont.save()
    return HttpResponse('Success')
def editreg(request):
    if (request.method == "POST"):
        regnum = request.POST['regnum']
        regval = request.POST['regval']
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

            if "SD" in instr or "LD" in instr:

                if (int(instr.split(" ")[-1].split("(")[0],16) > 8184 or int(instr.split(" ")[-1].split("(")[0],16)%8 != 0):
                    memerror = True
                    line = i + 1
                    context = {
                        'memerror': memerror,
                        'line': line,
                    }
                    return render(request, 'mips/index.html', context)

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
                context = {
                    'errorlabel': errorlabel,
                    'line': line,
                }
                return render(request, 'mips/index.html', context)
            if len(lbl) == 0:
                
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
            
            context = {
                'errorlabel': errorlabel,
                'line': line,
            }
            return render(request, 'mips/index.html', context)


    codes_obj = Codes.objects.all()
    for i,e in enumerate(codes_obj):
        opcode(i,e)
        
    piplineparse()
    executemips(request)
    return redirect('/load/')
    


def errorCheck(instr):
    regex = r"^(\w+:( )?)$|((\w+:( )?)?((LD|SD) R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( ([0-9A-F]){4})(\(R([0-9]|1[0-9]|2[0-9]|3[0-1])\)))$|^((\w+:( )?)?(DADDIU|XORI)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9A-F])){4}))$|^((\w+:( )?)?(DADDU|SLT)( R([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( R([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\w+:( )?)?(BGTZC R([0-9]|1[0-9]|2[0-9]|3[0-1]),)( \w+))$|^((\w+:( )?)?(J \w+))$"
    if re.search(regex, instr): # need to add checking of labels
        return True

    return False

  
def opcode(instrnum, codes_obj):
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

        
        opco = Opcodetable.objects.create(instrnum = instrnum, instrc=instrc,opcode=opc.upper(),rs=baseop,rt=rtop,imm=offsetop)
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
        
        opco = Opcodetable.objects.create(instrnum = instrnum, instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=immop)
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

        
        opco = Opcodetable.objects.create(instrnum = instrnum, instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=(rdop+saop+funcop))
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

        
        opco = Opcodetable.objects.create(instrnum = instrnum, instrc=instrc,opcode=opc.upper(),rs=rsop,rt=rtop,imm=offset)
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

        
        opco = Opcodetable.objects.create(instrnum = instrnum, instrc=instrc,opcode=opc.upper(),rs=lbl[:5],rt=lbl[5:10],imm=lbl[10:])
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
        previnstr = get_object_or_404(Piplnsrcdest, instrnum=counter - 1).instrc
        #previnstr = Piplnsrcdest.objects.filter(instrnum=counter - 1).get().instrc
        if "BGTZC" in previnstr or "J" in previnstr:
            poslabel = Piplnsrcdest.objects.filter(label=previnstr.split(" ")[-1]).get().instrnum

            if "J" in previnstr:
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
            elif "BGTZC" in previnstr and Piplnsrcdest.objects.filter(instrnum=counter - 1).get().stat == 1:
                branch = 1
                
                if poslabel == counter:
                    for obj in arrpln[-1]:
                        if obj == " " or obj == "IF":
                            lstoappend.append(" ")
                        if obj == "ID":
                            lstoappend.append("IF")
                        if obj == "*" or obj == "/":
                            lstoappend.append("/")
                        if obj == "EX" or obj == "MEM":
                            lstoappend.append("*")
                        if obj == "WB":
                            lstoappend.append("ID")
                            lstoappend.append("EX")
                            lstoappend.append("MEM")
                            lstoappend.append("WB")
                else: 
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
                        arrpln.append([""])
                    lstoappend = []
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
                #print("NOT TAKEN")
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
            
        elif (amij == 1):

            if (counter < poslabel):
                lstoappend.append("")
                skipcount -= 1
            else:
                complain = 0
                amij = 0
                prevobj = Piplnsrcdest.objects.filter(instrnum=counter - 1).get()
                currobj = Piplnsrcdest.objects.filter(instrnum=counter).get()
                if prevobj.dest == currobj.src1 or prevobj.dest == currobj.src2:
                    complain = 1
                for obj in arrpln[skipcount]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "ID":
                        lstoappend.append("IF")
                    if obj == "EX":
                        if complain == 1:
                            lstoappend.append("*")
                        else:
                            lstoappend.append("ID")
                    if obj == "MEM":
                        if complain == 1:
                            lstoappend.append("*")
                        else:
                            lstoappend.append("EX")
                    if obj == "WB":
                        if complain == 1:
                            lstoappend.append("ID")
                            lstoappend.append("EX")
                            lstoappend.append("MEM")
                            lstoappend.append("WB")

                        else:
                            lstoappend.append("MEM")
                            lstoappend.append("WB")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")
                skipcount = -1
        else:
            #print("DOING ELSE")
            if (amij > 1):
                amij -= 1
            prevobj = Piplnsrcdest.objects.filter(instrnum=counter - 1).get()
            currobj = Piplnsrcdest.objects.filter(instrnum=counter).get()
            if currobj.instrc == "":
                for i in range (0, len(arrpln[-1])):
                    lstoappend.append(" ")
                arrpln.append(lstoappend)
            else:
                if prevobj.dest == currobj.src1 or prevobj.dest == currobj.src2:
                    complain = 1
                for obj in arrpln[-1]:
                    if obj == " " or obj == "IF":
                        lstoappend.append(" ")
                    if obj == "ID":
                        lstoappend.append("IF")
                    if obj == "EX":
                        if complain == 1:
                            lstoappend.append("*")
                        else:
                            lstoappend.append("ID")
                    if obj == "MEM":
                        if complain == 1:
                            lstoappend.append("*")
                        else:
                            lstoappend.append("EX")
                    if obj == "WB":
                        if complain == 1:
                            lstoappend.append("ID")
                            lstoappend.append("EX")
                            lstoappend.append("MEM")
                            lstoappend.append("WB")

                        else:
                            lstoappend.append("MEM")
                            lstoappend.append("WB")
                    if obj == "*" or obj == "/":
                        lstoappend.append("/")

        if branch == 0:
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
            #print(cycle, "cycle")

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
def IF(instrnum, thepc):
    theif=[]
    
    op = Opcodetable.objects.filter(instrnum=instrnum).get()
    
    ir = op.opcode                                #if/id.ir
    pc = format(thepc, '02x').zfill(16).upper()   #if/id.pc
    npc = pc                                      #if/id.npc
    
    return ir.upper(), npc.upper(), pc.upper()
#    theif.append(ir.upper())
#    theif.append(npc.upper())
#    theif.append(pc.upper())
#    
#    return theif

def ID(instrnum, theif):
    theid=[]
    op = Opcodetable.objects.filter(instrnum=instrnum).get()
    a = None
    b = None
    imm = None
    
#    print(Register.objects.filter(regnum=hex(int(op.rt, 2))[2:]).get().regval.upper(), "rt", hex(int(op.rt, 2))[2:])
#    print(Register.objects.filter(regnum=hex(int(op.rs, 2))[2:]).get().regval.upper(), "rs", hex(int(op.rs, 2))[2:])
#    
    a = Register.objects.filter(regnum=hex(int(op.rs, 2))[2:]).get().regval.upper()
    b = Register.objects.filter(regnum=hex(int(op.rt, 2))[2:]).get().regval.upper()
    
    imm = hex(int(op.imm, 2))[2:].upper().zfill(16)             # id/ex.imm
    
    npc = theif[1]                   # id/ex.npc
    ir = theif[0]                    # id/ex.ir
    
    return a.upper(), b.upper(), imm.upper(), ir.upper(), npc.upper()
    
#    theid.append(a.upper())
#    theid.append(b.upper())
#    theid.append(imm.upper())
#    theid.append(ir.upper())
#    theid.append(npc.upper())
#    
#    
#    return theid

def EX(instr, theid):
    theex=[]
    
    b = theid[1]
    ir = theid[3]
    
    if("J" in instr):                                      # Jump instruction
        print(theid[2], "theid")
        aluo = hex(int(theid[2],16) << 2)[2:].zfill(16).upper()
        cond = "1"
    elif("LD" in instr or "SD" in instr):                 # Load/Store instruction
        aluo = hex(int(theid[0],16) + int(ir,16))[2:].zfill(16).upper()
        cond = "0"
    elif("BGTZC" in instr):                                # Branch instruction
        aluo = hex(int(ir,16) + (int(theid[2],16) << 2))[2:].zfill(16).upper()
        cond = Codes.objects.filter(instruction=instrc).get().status
    else:                                                   # ALU instruction
        if("DADDIU" in instr):
            tmp = sign_extend(hex(int(theid[0],16) + int(sign_extend(theid[2]),16))[2:].zfill(16))
            print(theid[0], theid[2], tmp, "hello")
            aluo = tmp
            print("TMP!!!", tmp)
        elif("SLT" in instr):
            if(theid[0] < b):
                aluo = "0000000000000001"
            else:
                aluo = "0000000000000000"
        elif("DADDU" in instr):
            tmp = hex(int(theid[0],16) + int(b,16))[2:].zfill(16).upper()
            aluo = tmp
            print(tmp, "TMPPPP")
        elif("XORI" in instr):
            rs = int(sign_extend(theid[0]),16)
            rt = int(theid[2].zfill(16),16)
            
            aluo = format(rs^rt,'x').zfill(16).upper()
        else:
            aluo = "ERROR!! WHAT HAPPENED?? :<"
            
        cond = "0"
        
    return aluo.upper(), cond.upper(), ir.upper(), b.upper()
#    theex.append(aluo.upper())
#    theex.append(cond.upper())
#    theex.append(ir.upper())
#    theex.append(b.upper())
#    
#    return theex

def MEM(instrc, theex):
    themem=[]
    lmd = "N/A"
    aluo = "N/A"
    
    ir = theex[2]                               #mem/wb.ir
    
    if("LD" in instrc):                         #load instruction
        end = theex[0][-4:]
        start = '0x{:02x}'.format(int(end,16) + 7)[2:].upper().zfill(4)
        print("start", start)
        lmd = Memory.objects.filter(address=start).get().memval
        
        n = 6
        while n >= 0:
            start = '0x{:02x}'.format(int(end,16) + n)[2:].upper().zfill(4)
            print("start again", start)
            lmd = lmd + Memory.objects.filter(address=start).get().memval
            n-=1
       
    elif("SD" in instrc):                       #store instruction
        print(theex[0], theex[1], theex[2], theex[3], "theex")
        ir = theex[2]
        b = theex[3]
        print (b)
        src2 = (((instrc.split(" "))[2]).split("(")[1]).replace(")","").replace("R","")
        print(src2)
        
        smem = ((instrc.split(" "))[2]).split("(")[0]
        print (smem)
        
        endmem = format(int(Register.objects.filter(regnum=src2).get().regval, 16) +  int('7', 16) + int(smem, 16), 'x').zfill(4).upper()
        print(endmem)
        
        n = 2
        memtoget = endmem

        for i in range(0, len(b), n):
            print(b[i:i+n])
            mem = Memory.objects.filter(address=memtoget).get()
            
            mem.memval = b[i:i+n]
            mem.save()    
            
            print("MEM VALUE",mem.memval, "MEMORY NUM", mem.address)
            memtoget = format(int(memtoget, 16) - int('1', 16), 'x').zfill(4).upper()
        
        aluo = theex[0]
    else:
        aluo = theex[0]
    
    return lmd.upper(), ir.upper(), aluo.upper()
    
#    themem.append(lmd.upper())
#    themem.append(ir.upper())
#    themem.append(aluo.upper())
#    
#    return themem

def WB(instrc, instrnum, src2, themem):
    op = Opcodetable.objects.filter(instrnum=instrnum).get()
    
    thewb=[]
    if("LD" in instrc):                                                           #load
        r = Register.objects.filter(regnum=int(op.rt, 2)).get()         #mem/wb.ir 16..20
        r.regval = themem[0]
        r.save()
        reg = "R" + str(int(op.rt,2))
        wb = reg + " = " + r.regval
    elif("SD" in instrc or "BGTZC" in instrc or "J" in instrc):
        wb = "N/A"
    elif("R" in src2 and "LD" not in instrc):                                     #reg-reg
        kwa = op.imm[:5]
        r = Register.objects.filter(regnum=int(kwa, 2)).get()
        r.regval = themem[2]
        r.save()
        reg = "R" + str(int(    kwa, 2))
        wb = reg + " = " + r.regval
    else:                                                                         #reg-imm
        r = Register.objects.filter(regnum=int(op.rt, 2)).get()         #mem/wb.ir 16..20
        r.regval = themem[2]
        r.save()
        reg = "R" + str(int(op.rt, 2))
        wb = reg + " = " + r.regval
        
    return wb.upper()
        
#    thewb.append(wb.upper())
    
#    return thewb
def pipeline(request):
    internal = []
    pc = 0                                      # pc/npc
    arrpln = pipelnmap()                        # pipeline map
    maxsize = len(arrpln[-1])                   # number of instructions
    
    for a in arrpln:                            # fills in spaces for pipeline
        if len(a) < maxsize:
            for i in range(0,maxsize-len(a)):
                a.append(" ")
    
    cycles = []                                 # get per cycle
    cycle = []   
    for v in range(0, maxsize):
        for a in arrpln:
            cycle.append(a[v])
        cycles.append(cycle)
        cycle = []
    
    icyc=[]
    anif = []
    anid = []
    anex = []
    amem = []
    awb = []
                                                # initialize table
    for a in cycles:
        internal.append([" ", " ", " "," "," "," "," "," "," "," "," "," "," "," "," "," "])
#        icyc.append([" ", " ", " "])            # if
#        icyc.append([" ", " ", " ", " ", " "])  # id
#        icyc.append([" ", " ", " ", " "])       # ex
#        icyc.append([" ", " ", " "])            # mem
#        icyc.append([" "])                      # wb
#        internal.append(icyc)
#        icyc=[]

#    internal[0][0] = "dog"
#    internal[0][1] = "aa"
#    internal[1] = ["apple", " ", " "," "," "," "," "," "," "," "," "," "," "," "," "," "]

    ccnt = 0
    for a in cycles:
        for i, obj in enumerate(a):
            if obj == "WB":
                internal[ccnt][15] = WB(Piplnsrcdest.objects.filter(instrnum=i).get().instrc, i, Piplnsrcdest.objects.filter(instrnum=i).get().src2, amem)
#                internal[ccnt][4] = awb
            elif obj == "MEM":
                internal[ccnt][12],internal[ccnt][13],internal[ccnt][14] = MEM(Piplnsrcdest.objects.filter(instrnum=i).get().instrc, anex)
#                internal[ccnt][3] = amem
                amem.append(internal[ccnt][12])
                amem.append(internal[ccnt][13])
                amem.append(internal[ccnt][14])
            elif obj == "EX":
                internal[ccnt][8],internal[ccnt][9],internal[ccnt][10],internal[ccnt][11] = EX(Piplnsrcdest.objects.filter(instrnum=i).get().instrc, anid)
                anex.append(internal[ccnt][8])
                anex.append(internal[ccnt][9])
                anex.append(internal[ccnt][10])
                anex.append(internal[ccnt][11])
#                internal[ccnt][2] = anex
            elif obj == "ID":
                internal[ccnt][3],internal[ccnt][4],internal[ccnt][5],internal[ccnt][6],internal[ccnt][7] = ID(i, anif)
#                internal[ccnt][1] = anid
                anid.append(internal[ccnt][3])
                anid.append(internal[ccnt][4])
                anid.append(internal[ccnt][5])
                anid.append(internal[ccnt][6])
                anid.append(internal[ccnt][7])
            elif obj == "IF":
                pc += 4
                internal[ccnt][0],internal[ccnt][1],internal[ccnt][2] = IF(i, pc)
                anif.append(internal[ccnt][0])
                anif.append(internal[ccnt][1])
                anif.append(internal[ccnt][2])
#                internal[ccnt][0] = anif
        ccnt+=1
    
                                                # add values to table
#    ccnt = 0
#    for a in cycles:
#        for i, obj in enumerate(a):
#            if obj == "WB":
#                awb = WB(Piplnsrcdest.objects.filter(instrnum=i).get().instrc, i, Piplnsrcdest.objects.filter(instrnum=i).get().src2, amem)
#                internal[ccnt][4] = awb
#            elif obj == "MEM":
#                amem = MEM(Piplnsrcdest.objects.filter(instrnum=i).get().instrc, anex)
#                internal[ccnt][3] = amem
#            elif obj == "EX":
#                anex = EX(Piplnsrcdest.objects.filter(instrnum=i).get().instrc, anid)
#                internal[ccnt][2] = anex
#            elif obj == "ID":
#                anid = ID(i, anif)
#                internal[ccnt][1] = anid
#            elif obj == "IF":
#                pc += 4
#                anif = IF(i, pc)
#                internal[ccnt][0] = anif
#            elif obj == "*":
##                if "EX" in a:
##                    print("EX")
##                    internal[ccnt][1] = ["*", "*", "*", "*", "*"]
##                else:
##                    print("MEM")
##                    internal[ccnt][2] = ["*", "*", "*", "*"]
#                print("ASTERISK",a)
#
#        ccnt+=1
        
    #print(cycles, "CYCLE")
    print(internal, "INTERNAL")
    
    lists = ['IF/ID.IR = ','IF/ID.PC = ','IF/ID.NPC = ',"ID/EX.A = ","ID/EX.B = ","ID/EX.IMM = ","ID/EX.IR = ","ID/EX.NPC = ","EX/MEM.ALUoutput = ","EX/MEM.COND = ","EX/MEM.IR = ","EX/MEM.B = ","MEM/WB.LMD = ", "MEM/WB.IR = ","MEM/WB.ALUoutput = ","Rn = "]
    
    context={
        'internal':internal,
        'lists':lists,
    }
    return render(request, 'mips/pipln.html', context)


def executemips(request):
    pipelist = Piplnsrcdest.objects.all()
    reglist = Register.objects.all()
    memlist = Memory.objects.all()
    
    
    counter = 0
    jump = 0
    
    tempreglist = []
    tempmemlist = []
    
    for reg in reglist:
        tempreglist.append(reg.regval)

    for mem in memlist:
        tempmemlist.append(mem.memval)
        
    while counter < len(pipelist):

        print(pipelist[counter].instrc)
        pip = pipelist[counter].instrc
        pipinst = pip.split(" ")
        if ": " in pip:
            pipinst = pip.split(": ")[1]
        elif ":" in pip:
            pipinst = pip.split(":")[1]
        else:
            pipinst = pip

        
        if "DADDU" in pipinst:
            
            src1 = pipelist[counter].src1           # R3
            src2 = pipelist[counter].src2           # R4

            dest = pipelist[counter].dest
            rs = tempreglist[int(src1.split("R")[1])]
            rt = tempreglist[int(src2.split("R")[1])]
            
            de = int(dest.split("R")[1])
            des = format( int(rs,16) + int(rt,16),'x').upper()
            tempreglist[de] = des

            
        if "DADDIU" in pipinst:
            src1 = pipelist[counter].src1
            dest = pipelist[counter].dest
            de = int(dest.split("R")[1])
            rs = tempreglist[int(src1.split("R")[1])]
            
            rt = (pipelist[counter].instrc).split("#")[1]

            des = sign_extend(format( int(rs,16) + int(sign_extend(rt),16),'x').upper())
            tempreglist[de] = des
            print("REG",de," is",tempreglist[de])
           
        if "XORI" in pipinst:
            src1 = pipelist[counter].src1
            dest = pipelist[counter].dest
            
            s1 = src1.split("R")[1]
            s2 = (pipelist[counter].instrc).split("#")[1]
            de = dest.split("R")[1]

            rs = tempreglist[int(s1)]
            rs = int(sign_extend(rs),16)
            rt = int(s2.zfill(16),16)

            tempreglist[int(de)] = format(rs^rt,'x').zfill(16).upper()
            print("REG", de, " is", tempreglist[int(de)])
        
        if "SLT" in pipinst:
            src1 = pipelist[counter].src1
            src2 = pipelist[counter].src2
            dest = pipelist[counter].dest
            s1 = src1.split("R")
            s2 = src2.split("R")
            de = dest.split("R")[1]
            print(s1,s2,de)
            
            rs = tempreglist[int(s1[1])]
            rt = tempreglist[int(s2[1])]

            if s16(int(rs,16)) < s16(int(rt,16)):
                tempreglist[int(de)] = "1".zfill(16)
            else:
                tempreglist[int(de)] = "0".zfill(16)
            

            print("REG", de, " is", tempreglist[int(de)])
        if "LD" in pipinst:
            src1 = pipelist[counter].src1
            dest = pipelist[counter].dest
            
            s1 = src1.split("R")[1]
            s2 = ((pipelist[counter].instrc).split(" ")[-1]).split("(")[0]
            de = dest.split("R")[1]

            #startmem = format(int(s2,16)  + int(tempreglist[int(s1)],16),'x').zfill(4).upper()
            endmem = format(int(s2,16) + int('7',16) + int(tempreglist[int(s1)],16),'x').zfill(4).upper()
            # print("START",startmem)
            print("LD END mem",endmem)
            maxctr = 8
            memtoget = endmem
            strregval = ""
            while maxctr != 0:
                print(memtoget, "who?")
                mem = Memory.objects.filter(address=memtoget).get().memval
                strregval += mem
                memtoget = format(int(memtoget, 16) - int('1', 16), 'x').zfill(4).upper()
                maxctr-=1


            tempreglist[int(de)] = strregval
            print("REG", de, " is", tempreglist[int(de)])

        if "SD" in pipinst:
            src1 = pipelist[counter].src1 #register
            src2 = pipelist[counter].src2 #memory
            
            s1 = src1.split("R")[1]
            s2 = src2.split("R")[1]
            smem = ((pipelist[counter].instrc).split(" ")[-1]).split("(")[0]
            regval = tempreglist[int(s1)]
            print("HAHAHAHAHA",tempreglist[int(s2)])

            #startmem = format(int(tempreglist[int(s2)], 16) + int(smem, 16), 'x').zfill(4).upper()
            endmem = format(int(tempreglist[int(s2)], 16) + int('7', 16) + int(smem, 16), 'x').zfill(4).upper()
            #print("START",startmem)
            print("END",endmem)
            print(regval,"REGVAL")
            n = 2
            memtoget = endmem

            for i in range(0, len(regval), n):
                print(regval[i:i+n])
                print(memtoget)
#                mem = Memory.objects.filter(address=memtoget).get()
#                print(int(memtoget, 16), "tempmem")
                tempmemlist[int(memtoget, 16)] = regval[i:i+n]
                print("TEMP MEM VALUE", tempmemlist[int(memtoget, 16)], "MEMORY NUM", memtoget)
                memtoget = format(int(memtoget, 16) - int('1', 16), 'x').zfill(4).upper()
      
        if "BGTZC" in pipinst:
            src1 = tempreglist[int((pipelist[counter].src1).split("R")[1])]
            if int(src1,16) > 0:
                origc = counter - 1
                label = (pipelist[counter].instrc).split(" ")[-1]
                print("labellll ",label)
                intnum = Piplnsrcdest.objects.filter(label=label).get().instrnum
                branch= Piplnsrcdest.objects.filter(instrnum=counter).get()
                branch.stat = 1
                branch.save()
                counter = intnum-1  
                
                print(origc, counter+1, "YOO")
                if origc >= counter + 1:
                    raise Http404
    
        if jump == 1:
            origc = counter - 1
            label = (pipelist[counter-1].instrc).split(" ")[-1]
            intnum = Piplnsrcdest.objects.filter(label=label).get().instrnum
            counter = intnum-1
            jump = 0
            print("JUMP")
            print(origc, counter + 1, "yo")
            if origc > counter + 1:
                raise Http404
   
        if "J" in pipinst:
            print("ENTER J")
            jump = 1
            
            if counter == len(pipelist)-1:
                raise Http404
  
        counter+=1
        

def sign_extend(value):
     
    if len(str(value)) < 16:

        if "{0:16b}".format(int(value,16))[:1] == "1":
            ext = ""
            for i in range(0, 64-(len(str(value))*4)):
                ext += "1"
            return format(int(ext + "{0:16b}".format(int(value,16)),2),'x').upper() 
        else:
            return str(value).zfill(16).upper()
    elif len(str(value)) > 16:
        return value[1:]
    else:
        return value
def s16(value):
    return -(value & 0x8000) | (value & 0x7fff)