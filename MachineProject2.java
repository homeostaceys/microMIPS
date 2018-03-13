package machineproject2;

import java.math.BigInteger;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/* THINGS NEED TO DO 
 * 1. errorCheck() function - possibly use regular expression
 * 2. parseLoad() function  - parse the instruction one by one then get opcode put in a arraylist equivalent opcode
 * 3. plan how to simulate the instructions for freeze
 */

/**
 * S12 - COMPARC
 * @author CO, Kimberly Jane
 * @author PINLAC, Rastine
 * @author REYES, Stacey Kyle
 */
public class MachineProject2 {

    /**	This method displays the main menu.
     */
    public void mainMenu() {
        System.out.println("What would you like to do?\n");
        System.out.println("[1] - Input Instruction(s)");
        System.out.println("[2] - Input Registers");
        System.out.println("[3] - Input Memory");
        System.out.println("[4] - Load Tables");
        System.out.println("[5] - Start!");
        System.out.println("[6] - Exit\n");
        System.out.print (">> ");
    }
    
    /** This method converts Integer to Binary.
     * @param x is an integer number
     * @return Binary String of x
     */
    public static String convToBin(int x) {
        return(Integer.toBinaryString(x));
    }
    
    /** This method converts Decimal to Hexadecimal
     * 
     * @param x is a decimal number
     * @return Hexadecimal String of x
     */
    public static String convDecToHex(int x) {
        return Integer.toHexString(x);
    }
    
    /** This method converts Hexadecimal to Binary.
     * 
     * @param x is a hexadecimal number
     * @return Binary String of x
     */
    public static String convHexToBin(String x) {
        return new BigInteger(x, 16).toString(2);
    }
    
    /** This method converts Binary to Hexadecimal.
     * 
     * @param x is binary
     * @return x in hexadecimal format
     */
    public static String convBinToHex(String x) {
        int decimal = Integer.parseInt(x,2);
        return(Integer.toString(decimal,16));
    }
    
    /** This method performs sign extension.
     * 
     * @param x is binary
     * @return x with sign extension
     */
    public static String signExtend(String x) {
        int len = x.length();
        String msb = "0";
        String extend = "0";
        int tmp = len;
        //msb = Character.toString(x.charAt(0));
        if(len < 4) {
            while(tmp < 4) {
                extend += msb;
                tmp++;
            }
            x = extend + x;
        }
            
        return x;
    }
    
    /** This method performs sign extension for instruction index.
     * 
     * @param x is binary
     * @return x with sign extension
     */
    public static String signExtendIndex(String x) {
        int len = x.length();
        String msb = "0";
        String extend = "0";
        int tmp = len;
        //msb = Character.toString(x.charAt(0));
        if(len < 25) {
            while(tmp < 25) {
                extend += msb;
                tmp++;
            }
            x = extend + x;
        }
            
        return x;
    }
    
    /** This method performs sign extension for immediate.
     * 
     * @param x is binary
     * @return x with sign extension
     */
    public static String signExtendImm(String x) {
        int len = x.length();
        String msb = "0";
        String extend = "0";
        int tmp = len;
        //msb = Character.toString(x.charAt(0));
        if(len < 15) {
            while(tmp < 15) {
                extend += msb;
                tmp++;
            }
            x = extend + x;
        }
            
        return x;
    }
    
    /** this method gets the opcode for an instruction.
     * @param inst is the instruction
     * @return op is the opcode of the instruction
     */
    public static String getInstOp(String inst) {
        String op = null;
        
        if(inst.equalsIgnoreCase("LD"))
            op = "110111";
        else if(inst.equalsIgnoreCase("SD"))
            op = "110111";
        else if(inst.equalsIgnoreCase("DADDIU"))
            op = "110111";
        else if(inst.equalsIgnoreCase("XORI"))
            op = "110111";
        else if(inst.equalsIgnoreCase("DADDU"))
            op = "110111";
        else if(inst.equalsIgnoreCase("SLT"))
            op = "110111";
        else if(inst.equalsIgnoreCase("BGTZC"))
            op = "110111";
        else if(inst.equalsIgnoreCase("J"))
            op = "110111";
        else
            System.out.println("Instruction not supported.");
        
        return op;
    }
    
    public static String getFuncOp(String inst) {
        String func = null;
        
        if(inst.equalsIgnoreCase("DADDU"))
            func = "101101";
        else if(inst.equalsIgnoreCase("SLT"))
            func = "101010";
        else
            System.out.println("Instruction not supported.");
        
        return func;
    }
    
    /** This method gets register opcode for rs, rt, rd, and the like.
     * 
     * @param reg is the register
     * @return Binary String of reg
     */ 
    public static String getRegOp(String reg) {
        reg = reg.replaceAll("\\D+","");
        return convToBin(Integer.parseInt(reg));
    }
    
    /** This method gets opcode for immediate.
     * 
     * @param imm is immediate
     * @return Binary String of imm
     */
    public static String getImmOp(String imm) {
        return convHexToBin(imm);
    }
    
//    public String getOffsetOp(String offset) {
//        return Integer.toString(Integer.parseInt(offset)/4);
//    }
    
    /** This method gets the opcode for DADDIU or XORI
     * 
     * @param in is the instruction
     * @param rs is the rs value
     * @param rt is the rt value
     * @param imm is the immediate value
     * @return opcode in hexadecimal
     */
    public static String Scenario1(String in, String rs, String rt, String imm) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String rsopp = getRegOp(rs);
        String rtopp = getRegOp(rt);
        String immopp = getImmOp(imm);

        //sign extend
        rsopp = signExtend(rsopp);
        rtopp = signExtend(rtopp);
        immopp = signExtendImm(immopp);

        //concatenate
        opc = inopp;
        opc += rsopp;
        opc += rtopp;
        opc += immopp;
                        
        //return in hex
        return convBinToHex(opc);
    }
    
    /** This method gets the opcode for SD or LD
     * 
     * @param in is the instruction
     * @param base is the base value
     * @param rt is the rt value 
     * @param offset is the offset value
     * @return opcode in hexadecimal
     */
    public static String Scenario2(String in, String base, String rt, String offset) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String baseopp = getRegOp(base);
        String rtopp = getRegOp(rt);
//        String offsetopp = getOffsetOp(offset);
        String offsetopp = convHexToBin(offset);

        //sign extend
        baseopp = signExtend(baseopp);
        rtopp = signExtend(rtopp);
        offsetopp = signExtendImm(offsetopp);

        //concatenate
        opc = inopp;
        opc += baseopp;
        opc += rtopp;
        opc += offsetopp;
                        
        //return in hex
        return convBinToHex(opc);
    }
    
    /** This method gets the opcode for the DADDU and SLT instructions.
     * 
     * @param in is the instruction
     * @param rs is the rs value
     * @param rt is the rt value
     * @param rd is the rd value
     * @return opcode in hexadecimal
     */
    public static String Scenario3(String in, String rs, String rt, String rd) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String rsopp = getRegOp(rs);
        String rtopp = getRegOp(rt);
        String rdopp = getRegOp(rd);
        String saopp = "00000";
        String funcopp = getFuncOp(in);

        //sign extend
        rsopp = signExtend(rsopp);
        rtopp = signExtend(rtopp);
        rdopp = signExtend(rdopp);

        //concatenate
        opc = inopp;
        opc += rsopp;
        opc += rtopp;
        opc += rdopp;
        opc += saopp;
        opc += funcopp;
                        
        //return in hex
        return convBinToHex(opc);
    }
    
    /** This method gets the opcode for BGTZC instruction
     * 
     * @param in is the instruction
     * @param rt is the rt value
     * @param offset is the offset
     * @return opcode in hexadecimal
     */
    public static String Scenario4(String in, String rt, String offset) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String baseopp = "00000";
        String rtopp = getRegOp(rt);
 //        String offsetopp = getOffsetOp(offset);
        String offsetopp = convHexToBin(offset);
        
        //sign extend
        rtopp = signExtend(rtopp);
        offsetopp = signExtendImm(offsetopp);

        //concatenate
        opc = inopp;
        opc += baseopp;
        opc += rtopp;
        opc += offsetopp;
                        
        //return in hex
        return convBinToHex(opc);
    }
    
    /** This methods gets the opcode for J instruction
     * 
     * @param in is the instruction
     * @param pos as position
     * @return opcode in hexadecimal
     */
    public static String Scenario5(String in, int pos) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String indexopp = Integer.toString(pos);

        //sign extend
        indexopp = signExtendIndex(indexopp);

        //concatenate
        opc = inopp;
        opc += indexopp;
                        
        //return in hex
        return convBinToHex(opc);
    }
    
    /** This method checks whether the instruction is a valid instruction.
     * 
     * @param instrc is the instruction
     * @return a boolean expression if it passes the error checking criteria
     */
    public static Boolean errorCheck(String instrc, boolean check) {
    	String pattern="^((\\w+:)?(LD|ld)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),)( (\\w+))(\\((r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])\\)))$|^((\\w+:)?(SD|sd)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),)( (\\w+)|([0-9A-Fa-f]{4}))(\\((r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])\\)))$|^((\\w+:)?(DADDIU|daddiu)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9a-fA-f])){4}))$|^((\\w+:)?(XORI|xori)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9a-fA-f])){4}))$|^((\\w+:)?(DADDU|daddu)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\\w+:)?(SLT|slt)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\\w+:)?(BGTZC|bgtzc)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( \\w+))$|^((\\w+:)?(J|j)( \\w+))$|^(END|end)$";
    	Pattern r= Pattern.compile(pattern);
    	Matcher m = r.matcher(instrc);
    	if (m.find()) {
    		return true;
    	}
    	System.out.println("Instruction error !!!");
    	check = false;
    	return false;
    	
    }
    /** This method checks whether the value to be inputted in the register is valid or not.
     * 
     * @param regval is the register values
     * @return a boolean expression if it passes the error checking criteria
     */
    public static Boolean checkRData(String regval) {
    	String pattern = "^(([0-9A-Fa-f]{4}){4})$";
    	Pattern r= Pattern.compile(pattern);
    	Matcher m = r.matcher(regval);
    	if(m.find()) {
    		return true;
    	}
    	System.out.println("Invalid value !!! Value not changed ");
    	return false;
    }
    /** This method checks whether the value to be inputted in the memory is valid or not.
     * 
     * @param memloc is the memory location
     * @param memval is the memory value 
     * @return a boolean expression if it passes the error checking criteria
     */
    public static Boolean checkMData(String memloc, String memval) {
    	
    	String pat = "^([0-9A-Fa-f]{2})$";
    	Pattern p = Pattern.compile(pat);
    	Matcher match = p.matcher(memval);
    	
    	if((Integer.parseInt(memloc,16)> 0 && Integer.parseInt(memloc,16) < 4096) && match.find()) {
    		return true;
    	}
    	System.out.println("Invalid value !!! Value not changed ");
    	return false;
    }
    
    /** This method gets parses the instruction then loads into memory.
     * 
     * @param reg
     * @param memory
     * @param instrc is the instruction
     *
     */
    public static void parseLoad(String[][] opcode, String instrc, int instrc_num) {
        
        String cmd = null;
        
             
    	if(instrc.contains(":")) {
    		instrc = instrc.split(":")[1]; //DADDIU R1, R2, R4
    	}
        String[] parts = instrc.split(" ");
        cmd = parts[0];
    	if(cmd.equalsIgnoreCase("LD") || cmd.equalsIgnoreCase("SD")) {
    		/* parse and load for LD or SD */
                opcode[instrc_num][1] = Scenario2(cmd, parts[2].split("(")[1].replace(")",""), parts[1].replace(",", ""), parts[2].split("(")[0]);
    	}
    	if(cmd.equalsIgnoreCase("DADDIU")||cmd.equalsIgnoreCase("XORI")) {
    		/* parse and load for DADDIU or XORI */
                if(parts[3].contains("0x"))
                    parts[3].replace("0x","");
                else
                    parts[3].replace("#","");
                opcode[instrc_num][1] = Scenario1(cmd, parts[2].replace(",", ""), parts[1].replace(",", ""), parts[3]); 
    	}
    	if(cmd.equalsIgnoreCase("DADDU") || cmd.equalsIgnoreCase("SLT")) {
    		/* parse and load for DADDU or SLT */
                opcode[instrc_num][1] = Scenario3(cmd, parts[2].replace(",",""), parts[3], parts[1].replace(",","")); 
    	}
    	if(cmd.equalsIgnoreCase("BGTZC")) {
    		/* parse and load for BGTZC */
                opcode[instrc_num][1] = Scenario4(cmd, parts[1].replace(",",""), parts[2]);
    	}
    	else {
    		/* parse and load for J */
                opcode[instrc_num][1] = Scenario5(cmd, instrc_num);
    	}
    }
    
    public static void main(String[] args) {
       
        boolean exitMain = false;
        boolean check = true;
        int opt, ctr, regnum;
        String regval, memloc, memval, instr;
        String lbl = null,
               in = null, 
               rs = null, 
               rt = null,
               imm = null,
               rd = null,
               sa = null,
               base = null,
               offset = null;
                	   
        MachineProject2 m = new MachineProject2();
        Scanner sc = new Scanner (System.in);
        ArrayList<String> reg = new ArrayList<>();   // Registers
        ArrayList<String> instructions = new ArrayList<>(); // the instruction per line
        String[][] memory = new String[0][0];
        String[][] opcode;
        
        /* initialize regs */
               
        do {
            m.mainMenu();
            opt = sc.nextInt();
            sc.nextLine();
            switch(opt) {
                case 1: /* Input MIPS program */
                    
//                    //sample inputs for scenario 1
//                    in = "XORI";
//                    rs = "R5";
//                    rt = "R20";
//                    imm = "FFFF";
                    instructions = new ArrayList<>();
                    ctr = 0;
                    System.out.print("Add an instruction: \n");
                    do {
                    	instr = sc.nextLine().toUpperCase();
                    	if((!instr.equals("END"))&&(!instr.equals(""))) {
                    		if(errorCheck(instr, check))
                    			instructions.add(instr);
                    	}
                    } while((!instr.equals("END")));
                   
                     System.out.println(instructions);
                    
                    break;
                case 2: /* Input register values R1-R31*/
                    
                	for(int i = 0; i < 32; i++) {
                        reg.add("0000000000000000");
                    }
                   
                    do {
                    	
	                	System.out.println("Input register number (to exit press -1): ");
	                	regnum = sc.nextInt();
	                	sc.nextLine();
	                	System.out.println("Input register value: ");
	                	regval = sc.nextLine();
	                	if((regnum > 0 && regnum < 32) && checkRData(regval)) {
	                		reg.set(regnum, regval.toUpperCase());
	                		System.out.println("Success! Value changed");
                    	}
                    	else {
                    		System.out.println("Error!! Enter again");
                    	}
                    }while( regnum != -1 );
                    for(int i = 0; i < 32; i++) {
                       System.out.println("R"+i+"="+(reg.get(i)));
                    }
                    break;
                case 3: /* Input memory values */
                	memory = new String[8192][2];
                	 for(int i = 0; i < 8192; i++) {
                     	memory[i][0] = Integer.toHexString(i).toUpperCase();
                     	memory[i][1] = "00";
                     }
                	 do {
                     	
 	                	System.out.println("Input memory location [0000-0fff] (enter exit to abort) : ");
 	                	memloc = sc.nextLine().toUpperCase();
 	                	System.out.println("Input memory value: ");
 	                	memval = sc.nextLine().toUpperCase();
 	                	if(!memloc.equals("EXIT") &&  !memloc.equals("") ) {
	 	                	if(checkMData(memloc,memval)) {
	 	                		memory[Integer.parseInt(memloc,16)][1] = memval;
	 	                		System.out.println("Success! Value changed");
	 	                	}
	                     	else {
	                     		System.out.println("Error!! Enter again");
	                     	}
 	                	}
                     }while(!memloc.equals("EXIT") &&  !memloc.equals(""));
                    
                     for(int i = 0; i < 8192; i++) {
                      	System.out.println(memory[i][0]+"----" + memory[i][1]);
                      }
                	break;
                case 4: /* Load values to tables and Opcode */
                	  System.out.println("Opcode of MIPS Program:");
                      opcode = new String[instructions.size()][3]; /*address, rep, label*/
                      
                      for(int i = 0; i < instructions.size(); i++) {
                          opcode[i][0] = m.convDecToHex(i*4);   // address
                          parseLoad(opcode, instructions.get(i), i);
                          
                          
                      }
                    break;
                case 5: /* Start! */
                  
                        
                    
                    break;
                case 6: /* Exit */
                    System.out.println("Exiting...");
                    exitMain = true;
                    break;
                default:
                    System.out.print("System: Please enter a valid option :(\n\n>>\n ");
            }
        } while(!exitMain);
        
        sc.close();
        m = null;
        System.gc();
        
    }
    
}
