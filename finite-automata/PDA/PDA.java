import java.util.*;

public class PDA {
    public static char CHAR_A = 'a';
    public static char CHAR_B = 'b';
    public static char BASE = '$';

    /* 
     * Simulates a PDA which only accepts strings in alphabet {a,b} that
     * are of the form { (a^n)(b^n) | n >= 0 }
     */

    public static void main(String[] args) {
        
        String str = prompt();
        Stack<Character> stack = new Stack<Character>();
        boolean result = state_0(str, stack);

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


    public static boolean state_0(String str, Stack<Character> stack) {
        // state q0
        if (str.length() == 0) {
            // accept as string ends on accept state
            return true;
        }

        // push the base onto the stack and go to state 1
        stack.push(BASE);
        return state_1(str, stack);
    }

    public static boolean state_1(String str, Stack<Character> stack) {
        // state q1
        if (str.length() == 0) {
            // reject as string ends on non-accept state
            return false;
        }

        char curChar = str.charAt(0);
        while (curChar == CHAR_A) {
            // push all consecutive a's onto the stack
            stack.push(curChar);
            str = str.substring(1, str.length());
            if (str.length() == 0) {
                return false;
            }
            curChar = str.charAt(0);
        }

        char popped;
        if (curChar == CHAR_B) {
            // if the current character is a b, pop an a from the stack and go to state 2
            popped = stack.pop();
            if (popped == BASE) {
                // if there are more b's than a's, reject
                return false;
            }
            str = str.substring(1, str.length());
            return state_2(str, stack);
        } else {
            // if the current character is not a b, reject
            return false;
        }
    }

    public static boolean state_2(String str, Stack<Character> stack) {
        // state q2
        if (str.length() == 0) {
            // reject as string ends on non-accept state
            return false;
        }

        char popped;
        char curChar = str.charAt(0);
        while (curChar == CHAR_B) {
            // for each consecutive b, pop an a from the stack
            popped = stack.pop();
            if (popped == BASE) {
                return false;
            }

            str = str.substring(1, str.length());
            if (str.length() == 0) {
                break;
            }
            curChar = str.charAt(0);
        }

        if (str.length() == 0) {
            // state 3
            popped = stack.pop();
            if (popped != BASE) {
                // there are more a's than b's, so reject
                return false;
            } else {
                // there are an equal number of a's and b's in the correct order
                return true;
            }
        } else {
            // reject as the string ends in a character that is not b
            return false;
        }
    }

}
