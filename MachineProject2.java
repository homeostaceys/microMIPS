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
        System.out.println("[2] - Reset Tables");
        System.out.println("[3] - Load Tables");
        System.out.println("[4] - Start!");
        System.out.println("[5] - Exit\n");
        System.out.print (">> ");
    }
    
    /** This method converts Integer to Binary.
     * @param x is an integer number
     * @return Binary String of x
     */
    public String convToBin(int x) {
        return(Integer.toBinaryString(x));
    }
    
    /** This method converts Hexadecimal to Binary.
     * 
     * @param x is a hexadecimal number
     * @return Binary String of x
     */
    public String convHexToBin(String x) {
        return new BigInteger(x, 16).toString(2);
    }
    
    /** This method converts Binary to Hexadecimal.
     * 
     * @param x is binary
     * @return x in hexadecimal format
     */
    public String convBinToHex(String x) {
        int decimal = Integer.parseInt(x,2);
        return(Integer.toString(decimal,16));
    }
    
    /** This method performs sign extension.
     * 
     * @param x is binary
     * @return x with sign extension
     */
    public String signExtend(String x) {
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
    public String signExtendIndex(String x) {
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
    public String signExtendImm(String x) {
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
    public String getInstOp(String inst) {
        String op = null;
        
        if(inst.equals("LD".equalsIgnoreCase("LD")))
            op = "110111";
        else if(inst.equals("SD".equalsIgnoreCase("SD")))
            op = "110111";
        else if(inst.equals("DADDIU".equalsIgnoreCase("DADDIU")))
            op = "110111";
        else if(inst.equals("XORI".equalsIgnoreCase("XORI")))
            op = "110111";
        else if(inst.equals("DADDU".equalsIgnoreCase("DADDU")))
            op = "110111";
        else if(inst.equals("SLT".equalsIgnoreCase("SLT")))
            op = "110111";
        else if(inst.equals("BGTZC".equalsIgnoreCase("BGTZC")))
            op = "110111";
        else if(inst.equals("J".equalsIgnoreCase("J")))
            op = "110111";
        else
            System.out.println("Instruction not supported.");
        
        return op;
    }
    
    public String getFuncOp(String inst) {
        String func = null;
        
        if(inst.equals("DADDU".equalsIgnoreCase("DADDU")))
            func = "101101";
        else if(inst.equals("SLT".equalsIgnoreCase("SLT")))
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
    public String getRegOp(String reg) {
        reg = reg.replaceAll("\\D+","");
        return convToBin(Integer.parseInt(reg));
    }
    
    /** This method gets opcode for immediate.
     * 
     * @param imm is immediate
     * @return Binary String of imm
     */
    public String getImmOp(String imm) {
        return convHexToBin(imm);
    }
    
    public String getOffsetOp(String offset) {
        return "B";
    }
    
    /** This method prints the opcode for DADDIU or XORI
     * 
     * @param in is the instruction
     * @param rs is the rs value
     * @param rt is the rt value
     * @param imm is the immediate value
     */
    public void Scenario1(String in, String rs, String rt, String imm) {
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
                        
        //print in hex
        System.out.println(convBinToHex(opc) + "\n");
    }
    
    /** This method prints the opcode for SD or LD
     * 
     * @param in is the instruction
     * @param base is the base value
     * @param rt is the rt value 
     * @param offset is the offset value
     */
    public void Scenario2(String in, String base, String rt, String offset) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String baseopp = getRegOp(base);
        String rtopp = getRegOp(rt);
        String offsetopp = getOffsetOp(offset);

        //sign extend
        baseopp = signExtend(baseopp);
        rtopp = signExtend(rtopp);
        offsetopp = signExtendImm(offsetopp);

        //concatenate
        opc = inopp;
        opc += baseopp;
        opc += rtopp;
        opc += offsetopp;
                        
        //print in hex
        System.out.println(convBinToHex(opc) + "\n");
    }
    
    /** This method prints the opcode for the DADDU and SLT instructions.
     * 
     * @param in is the instruction
     * @param rs is the rs value
     * @param rt is the rt value
     * @param rd is the rd value
     * @param sa is the sa value
     * @param func is the func value
     */
    public void Scenario3(String in, String rs, String rt, String rd) {
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
                        
        //print in hex
        System.out.println(convBinToHex(opc) + "\n");
    }
    
    /** This method prints the opcode for BGTZC instruction
     * 
     * @param in is the instruction
     * @param rt is the rt value
     * @param offset is the offset
     */
    public void Scenario4(String in, String rt, String offset) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String baseopp = "00000";
        String rtopp = getRegOp(rt);
        String offsetopp = getOffsetOp(offset);

        //sign extend
        rtopp = signExtend(rtopp);
        offsetopp = signExtendImm(offsetopp);

        //concatenate
        opc = inopp;
        opc += baseopp;
        opc += rtopp;
        opc += offsetopp;
                        
        //print in hex
        System.out.println(convBinToHex(opc) + "\n");
    }
    
    /** This methods prints the opcode for J instruction
     * 
     * @param in is the instruction
     * @param pos as position
     */
    public void Scenario5(String in, int pos) {
        String opc = null;
        //get binary
        String inopp = getInstOp(in);
        String indexopp = Integer.toString(pos);

        //sign extend
        indexopp = signExtendIndex(indexopp);

        //concatenate
        opc = inopp;
        opc += indexopp;
                        
        //print in hex
        System.out.println(convBinToHex(opc) + "\n");
    }
    
    /** This method checks whether the instruction is a valid instruction.
     * 
     * @param instrc is the instruction
     * @return a boolean expression if it passes the error checking criteria
     */
    public static Boolean errorCheck(String instrc) {
    	String pattern="^((\\w+:)?(LD|ld)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),)( (\\w+))(\\((r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])\\)))$|^((\\w+:)?(SD|sd)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),)( (\\w+)|([0-9A-Fa-f]{4}))(\\((r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])\\)))$|^((\\w+:)?(DADDIU|daddiu)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9a-fA-f])){4}))$|^((\\w+:)?(XORI|xori)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( ((0x)|#)(([0-9a-fA-f])){4}))$|^((\\w+:)?(DADDU|daddu)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\\w+:)?(SLT|slt)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1])))$|^((\\w+:)?(BGTZC|bgtzc)( (r|R)([0-9]|1[0-9]|2[0-9]|3[0-1]),){2}( \\w+))$|^(END|end)$";
    	Pattern r= Pattern.compile(pattern);
    	Matcher m = r.matcher(instrc);
    	if (m.find()) {
    		return true;
    	}
    	else {
    		System.out.println("Instruction error !!!");
    		return false;
    	}
    }
    
    /** This method gets parses the instruction then loads into memory.
     * 
     * @param instrc is the instruction
     *
     */
    public static void parseLoad(String instrc) {
    	String[] parts = instrc.split(" ");
    	System.out.println(parts[0]);
    	if(parts[0].equalsIgnoreCase("LD")) {
    		/* parse and load for LD */
    	}
    	if(parts[0].equalsIgnoreCase("SD")) {
    		/* parse and load for SD */
    	}
    	if(parts[0].equalsIgnoreCase("DADDIU")) {
    		/* parse and load for DADDIU */
    	}
    	if(parts[0].equalsIgnoreCase("XORI")) {
    		/* parse and load for XORI */
    	}
    	if(parts[0].equalsIgnoreCase("DADDU")) {
    		/* parse and load for DADDU */
    	}
    	if(parts[0].equalsIgnoreCase("SLT")) {
    		/* parse and load for SLT */
    	}
    	if(parts[0].equalsIgnoreCase("BGTZC")) {
    		/* parse and load for BGTZC */
    	}
    	else {
    		/* parse and load for J */
    	}
    }
    
    public static void main(String[] args) {
       
        boolean exitMain = false;
        int opt, ctr;
        String in = null, 
               rs = null, 
               rt = null,
               imm = null,
               rd = null,
               sa = null;
        	   
        MachineProject2 m = new MachineProject2();
        Scanner sc = new Scanner (System.in);
        ArrayList<String> reg = new ArrayList<>();   // Registers
        ArrayList<String> instr = new ArrayList<>(); // the instruction per line
        String[][] memory = new String[0][0];
        
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
                    instr = new ArrayList<>();
                    ctr = 0;
                    System.out.print("Add an instruction: ");
                    instr.add(sc.nextLine());  
                    while(errorCheck(instr.get(ctr))&&((instr.get(ctr).compareToIgnoreCase("END")) != 0)) {
                        instr.add(sc.nextLine());
                        ctr++;
                    }
                    
                    break;
                case 2: /* Reset all register and memory values */
                    memory = new String[65536][2];
                    for(int i = 1; i <= 31; i++) {
                        reg.add("0000000000000000");
                    }
                    for(int i = 0; i < 65535; i++) {
                	memory[i][0] = Integer.toHexString(i);
                	memory[i][1] = "00";
                    }
                	
                    break;
                case 3: /* Load values to tables */
                    for(int i = 0; i < instr.size(); i++) {
                	parseLoad(instr.get(i));
                    }
                	
                    break;
                case 4: /* Start! */
                    System.out.println("Opcode of MIPS Program:");
                    
                    for(int i = 0; i < instr.size(); i++) {
                        parseLoad(instr.get(i));
                        
                        /* Scenario 1: DADDIU or XOR */
                        if(in != null && rs != null && rt != null && imm != null)
                            m.Scenario1(in, rs, rt, imm);
                        /* Scenario 2: LD or SD */
//                        else if(in != null && base != null && rt != null && offset != null)
//                            m.Scenario2(in, base, rt, offset);
                        /* Scenario 3: DADDU or SLT */
                        else if(in != null && rs != null && rt != null && rd != null)
                            m.Scenario3(in, rs, rt, rd);
                        /* Scenario 4: BGTZC */
//                        else if(in != null && rt != null && offset != null)
//                            m.Scenario4(in, rt, offset);
//                        /* Scenario 5: J */
                        else if(in != null)
                            m.Scenario5(in, i);
                        else
                            System.out.println("Invalid.\n");
                        
                    }
                    break;
                case 5: /* Exit */
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
