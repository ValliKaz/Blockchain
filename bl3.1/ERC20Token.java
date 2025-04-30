import java.util.HashMap;
import java.util.Map;

public class ERC20Token {
    private String name;
    private String symbol;
    private int decimals;
    private Map<String, Integer> balances;
    private Map<String, Map<String, Integer>> allowances;
    private double transferFeePercent;
    private int totalFees;

    public ERC20Token(String name, String symbol, int decimals) {
        this.name = name;
        this.symbol = symbol;
        this.decimals = decimals;
        this.balances = new HashMap<>();
        this.allowances = new HashMap<>();
        this.transferFeePercent = 1.0;
        this.totalFees = 0;
    }

    public String transfer(String from, String to, int amount) {
        if (!balances.containsKey(from)) {
            return "Error: Sender account does not exist";
        }
        if (!balances.containsKey(to)) {
            return "Error: Recipient account does not exist";
        }

        if (amount <= 0) {
            return "Error: Transfer amount must be positive";
        }

        int balance = balances.get(from);
        if (balance < amount) {
            return "Error: Insufficient balance";
        }

        int fee = (int) (amount * transferFeePercent / 100);
        int amountAfterFee = amount - fee;
        totalFees += fee;

        balances.put(from, balance - amount);
        balances.put(to, balances.get(to) + amountAfterFee);

        logTransfer(from, to, amount, fee);
        return "Transfer successful: " + from + " sent " + amount + " to " + to + " (fee: " + fee + ")";
    }

    public String transferFrom(String spender, String from, String to, int amount) {
        if (!balances.containsKey(from) || !balances.containsKey(to) || !balances.containsKey(spender)) {
            return "Error: One or more accounts do not exist";
        }

        int allowance = allowance(from, spender);
        if (allowance < amount) {
            return "Error: Insufficient allowance";
        }

        int balance = balances.get(from);
        if (balance < amount) {
            return "Error: Insufficient balance";
        }

        int fee = (int) (amount * transferFeePercent / 100);
        int amountAfterFee = amount - fee;
        totalFees += fee;

        balances.put(from, balance - amount);
        balances.put(to, balances.get(to) + amountAfterFee);
        
        allowances.get(from).put(spender, allowance - amount);

        logTransfer(from, to, amount, fee);
        return "TransferFrom successful: " + spender + " transferred " + amount + " from " + from + " to " + to + " (fee: " + fee + ")";
    }

    public String approve(String owner, String spender, int amount) {
        if (!balances.containsKey(owner) || !balances.containsKey(spender)) {
            return "Error: One or more accounts do not exist";
        }

        if (amount < 0) {
            return "Error: Approval amount must be non-negative";
        }

        allowances.computeIfAbsent(owner, k -> new HashMap<>()).put(spender, amount);
        logApproval(owner, spender, amount);
        return "Approval successful: " + owner + " approved " + spender + " to spend " + amount;
    }

    public int allowance(String owner, String spender) {
        if (!allowances.containsKey(owner) || !allowances.get(owner).containsKey(spender)) {
            return 0;
        }
        return allowances.get(owner).get(spender);
    }

    private void logTransfer(String from, String to, int amount, int fee) {
        System.out.println("Transfer Event: " + from + " -> " + to + " Amount: " + amount + " Fee: " + fee);
    }

    private void logApproval(String owner, String spender, int amount) {
        System.out.println("Approval Event: " + owner + " approved " + spender + " to spend " + amount);
    }

    public int balanceOf(String address) {
        return balances.getOrDefault(address, 0);
    }

    public String getName() {
        return name;
    }

    public String getSymbol() {
        return symbol;
    }

    public int getDecimals() {
        return decimals;
    }

    public int getTotalFees() {
        return totalFees;
    }

    public static void main(String[] args) {
        ERC20Token token = new ERC20Token("MyToken", "MTK", 18);

        System.out.println("Token name: " + token.getName());
        System.out.println("Token symbol: " + token.getSymbol());
        System.out.println("Token decimals: " + token.getDecimals());

        token.balances.put("Alice", 1000);
        token.balances.put("Bob", 500);
        token.balances.put("Charlie", 200);

        System.out.println("\nTesting valid transfers:");
        System.out.println(token.transfer("Alice", "Bob", 200));
        System.out.println(token.transfer("Charlie", "Alice", 100));

        System.out.println("\nTesting invalid transfers:");
        System.out.println(token.transfer("Alice", "Bob", -50));
        System.out.println(token.transfer("Alice", "Bob", 2000)); 
        System.out.println(token.transfer("David", "Alice", 100)); 

        System.out.println("\nTesting approve and allowance:");
        System.out.println(token.approve("Alice", "Bob", 100));
        System.out.println("Allowance: " + token.allowance("Alice", "Bob"));

        System.out.println("\nTesting transferFrom:");
        System.out.println(token.transferFrom("Bob", "Alice", "Charlie", 70));
        System.out.println("New allowance: " + token.allowance("Alice", "Bob"));

        System.out.println("\nFinal balances:");
        System.out.println("Alice balance: " + token.balanceOf("Alice"));
        System.out.println("Bob balance: " + token.balanceOf("Bob"));
        System.out.println("Charlie balance: " + token.balanceOf("Charlie"));
        System.out.println("Total fees collected: " + token.getTotalFees());
    }
}