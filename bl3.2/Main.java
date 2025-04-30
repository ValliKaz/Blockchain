import java.util.*;

public class Main {
    public static void main(String[] args) {
        Blockchain chain = new Blockchain("SHA-256");
        chain.addBlock(List.of("Alice pays Bob", "Bob pays Charlie"));
        chain.addBlock(List.of("Charlie pays Dave", "Dave pays Eve"));
        chain.addBlock(List.of("Eve pays Alice"));

        chain.printBlockchain();

        System.out.println("\nChain is valid: " + chain.validateChain());
        System.out.println("\n--- TAMPERING BLOCK ---");
        chain.tamperBlock(1, "Charlie steals everything!");
        chain.printBlockchain();
        System.out.println("\nChain is valid: " + chain.validateChain());
    }
}
