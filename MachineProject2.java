package machineproject2;

import java.math.BigInteger;
import java.util.Scanner;
import java.util.ArrayList;

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
        System.out.println("[1] - Input MIPS program");
        System.out.println("[2] - Input value for registers R1 to R31");
        System.out.println("[3] - Input value for memory");
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
        switch(inst) {
            case "LD":
                op = "110111";
                break;
            case "SD":
                op = "111111";
                break;
            case "DADDIU":
                op = "011001";
                break;
            case "XORI":
                op = "001110";
                break;
            case "DADDU":
                op = "000000";
                break;
            case "SLT":
                op = "000000";
                break;
            case "BGTZC":
                op = "010111";
                break;
            case "J":
                op = "000010";
            default:
                System.out.println("Invalid");
        }
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
    
    public static void main(String[] args) {
        // TODO code application logic here
        boolean exitMain = false;
        int opt;
        String in = null, 
               rs = null, 
               rt = null,
               imm = null,
               opc = null;
        MachineProject2 m = new MachineProject2();
        Scanner sc = new Scanner (System.in);
        ArrayList<String> reg = new ArrayList<>();
        
        /* initialize regs */
        for(int i = 1; i <= 31; i++)
            reg.add("0000000000000000");
        
        do {
            m.mainMenu();
            opt = sc.nextInt();
            sc.nextLine();
            switch(opt) {
                case 1: /* Input MIPS program */
                    
                    //sample inputs for scenario 1
                    in = "XORI";
                    rs = "R5";
                    rt = "R20";
                    imm = "FFFF";
                    break;
                case 2: /* Input value for registers R1 to R31 */
                    break;
                case 3: /* Input value for memory */
                    break;
                case 4: /* Start! */
                    
                    /* Scenario 1: DADDIU or XOR */
                    if(in != null && rs != null && rt != null && imm != null) {
                        System.out.println("MIPS Program:");
                        System.out.println(in + " " + rs + "," + rt + "," + imm + "\n");
                        System.out.println("Opcode of MIPS Program:");

                        //get binary
                        String inopp = m.getInstOp(in);
                        String rsopp = m.getRegOp(rs);
                        String rtopp = m.getRegOp(rt);
                        String immopp = m.getImmOp(imm);

                        //sign extend
                        rsopp = m.signExtend(rsopp);
                        rtopp = m.signExtend(rtopp);
                        immopp = m.signExtendImm(immopp);

                        //concatenate
                        opc = inopp;
                        opc += rsopp;
                        opc += rtopp;
                        opc += immopp;
                        
                        //print in hex
                        System.out.println(m.convBinToHex(opc) + "\n");
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
