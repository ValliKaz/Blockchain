import java.util.*;

public class Blockchain {
    List<Block> chain;
    String hashAlgorithm;

    public Blockchain(String hashAlgorithm) {
        this.chain = new ArrayList<>();
        this.hashAlgorithm = hashAlgorithm;
    }

    public void addBlock(List<String> transactions) {
        String prevHash = (chain.isEmpty()) ? "0" : chain.get(chain.size() - 1).hash;
        Block newBlock = new Block(transactions, prevHash, hashAlgorithm);
        chain.add(newBlock);
    }

    public boolean validateChain() {
        for (int i = 1; i < chain.size(); i++) {
            Block current = chain.get(i);
            Block previous = chain.get(i - 1);

            if (!current.previousHash.equals(previous.hash) || !current.validate()) {
                return false;
            }
        }
        return true;
    }

    public void tamperBlock(int index, String newTransaction) {
        chain.get(index).transactions.set(0, newTransaction);
        chain.get(index).merkleTree = new MerkleTree(chain.get(index).transactions, hashAlgorithm);
        chain.get(index).merkleRoot = chain.get(index).merkleTree.getRoot();
        chain.get(index).hash = chain.get(index).calculateHash();
    }

    public void printBlockchain() {
        for (int i = 0; i < chain.size(); i++) {
            Block b = chain.get(i);
            System.out.println("\nBlock " + i + ":");
            System.out.println("Timestamp: " + b.timestamp);
            System.out.println("Merkle Root: " + b.merkleRoot);
            System.out.println("Hash: " + b.hash);
            System.out.println("Previous Hash: " + b.previousHash);
            System.out.println("Transactions: " + b.transactions);
        }
    }
}
