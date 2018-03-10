package machineproject2;

import java.math.BigInteger;
import java.util.Scanner;
import java.util.ArrayList;

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
        
        if("LD".equalsIgnoreCase("LD"))
            op = "110111";
        else if("SD".equalsIgnoreCase("SD"))
            op = "110111";
        else if("DADDIU".equalsIgnoreCase("DADDIU"))
            op = "110111";
        else if("XORI".equalsIgnoreCase("XORI"))
            op = "110111";
        else if("DADDU".equalsIgnoreCase("DADDU"))
            op = "110111";
        else if("SLT".equalsIgnoreCase("SLT"))
            op = "110111";
        else if("BGTZC".equalsIgnoreCase("BGTZC"))
            op = "110111";
        else if("J".equalsIgnoreCase("J"))
            op = "110111";
        else
            System.out.println("Instruction not supported.");
        
        return op;
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
    
    /** This method checks whether the instruction is a valid instruction.
     * 
     * @param instrc is the instruction
     * @return a boolean expression if it passes the error checking criteria
     */
    public static Boolean errorCheck(String instrc) {
    	String[] parts = instrc.split(" ");
    	System.out.println(parts[0]);
    	if(parts[0].equalsIgnoreCase("LD")) {
    		/* perform reg expression check for LD */
    	}
    	if(parts[0].equalsIgnoreCase("SD")) {
    		/* perform reg expression check for SD */
    	}
    	if(parts[0].equalsIgnoreCase("DADDIU")) {
    		/* perform reg expression check for DADDIU */
    	}
    	if(parts[0].equalsIgnoreCase("XORI")) {
    		/* perform reg expression check for XORI */
    	}
    	if(parts[0].equalsIgnoreCase("DADDU")) {
    		/* perform reg expression check for DADDU */
    	}
    	if(parts[0].equalsIgnoreCase("SLT")) {
    		/* perform reg expression check for SLT */
    	}
    	if(parts[0].equalsIgnoreCase("BGTZC")) {
    		/* perform reg expression check for BGTZC */
    	}
    	if(parts[0].equalsIgnoreCase("J")) {
    		/* perform reg expression check for J */
    	}
    	else {
    		System.out.println("Instruction error !!!");
    		return false;
    	}
    	return true;
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
               base = null,
               offset = null;
        	   
        MachineProject2 m = new MachineProject2();
        Scanner sc = new Scanner (System.in);
        ArrayList<String> reg = new ArrayList<>();   // Registers
        ArrayList<String> freg = new ArrayList<>();  // Floating point Register
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
                	freg.add("0000000000000000");
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
                    /* Scenario 1: DADDIU or XOR */
                    if(in != null && rs != null && rt != null && imm != null) {
                        m.Scenario1(in, rs, rt, imm);
                    /* Scenario 2: LD or SD */
                    } else if(in != null && rs != null && rt != null && imm != null) {
                        m.Scenario2(in, base, rt, offset);
                    } else
                        System.out.println("Invalid.\n");
                    
                    
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
