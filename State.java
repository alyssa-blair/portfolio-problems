import java.util.Scanner;

public class State {

    public static char CHAR_A = 'a';
    public static char CHAR_B = 'b';

    /* 
     * This program simulates a DFA. The program will output a message to the terminal 
     * whether or not the string is accepted by this DFA.
     */
    public static void main(String[] args) {
        String str = prompt();
        boolean result = state_0(str);

        if (result == true) {
            System.out.println("This string is accepted by the DFA");
        } else {
            System.out.println("This string is not accepted by the DFA");
        }
    }

    public static String prompt() {
        // prompts the user to enter a string comprised of a's and b's
        try (Scanner scan = new Scanner(System.in)) {
            System.out.println("Enter a string made up of only a's and b's: ");
            String scanned = scan.nextLine();
            return scanned;
        }
    }

    public static boolean state_0(String str) {
        // state q0
        if (str.length() == 0) {
            // reject as string ends on non-accept state
            return false;
        }
        
        char curChar = str.charAt(0);
        // checks first character of string to see next state
        if (curChar == CHAR_A) {
            return state_2(str = str.substring(1,str.length()));
        } else if (curChar == CHAR_B) {
            return state_3(str = str.substring(1, str.length()));
        } else {
            return false;
        }
    }

    public static boolean state_1(String str) {
        // state q1
        if (str.length() == 0) {
            // accept as string ends on accept state
            return true;
        }
        
        char curChar = str.charAt(0);
        // checks first character of string to see next state
        if (curChar == CHAR_A) {
            return state_0(str = str.substring(1, str.length()));
        } else if (curChar == CHAR_B) {
            return state_1(str = str.substring(1, str.length()));
        } else {
            return false;
        }
    }

    public static boolean state_2(String str) {
        // state q2
        if (str.length() == 0) {
            // reject as string ends on non-accept state
            return false;
        }

        char curChar = str.charAt(0);
        // checks first character of string to see next state
        if (curChar == CHAR_A) {
            return state_0(str = str.substring(1, str.length()));
        } else if (curChar == CHAR_B) {
            return state_1(str = str.substring(1, str.length()));
        } else {
            return false;
        }
    }

    public static boolean state_3(String str) {
        // state q3
        if (str.length() == 0) {
            // reject as string ends on non-accept state
            return false;
        }

        char curChar = str.charAt(0);
        // checks first character of string to see next state
        if (curChar == CHAR_A) {
            return state_2(str = str.substring(1, str.length()));
        } else if (curChar == CHAR_B) {
            return state_3(str = str.substring(1, str.length()));
        } else {
            return false;
        }
    }
}
