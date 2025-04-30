import java.util.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class Block {
    String timestamp;
    List<String> transactions;
    String merkleRoot;
    String previousHash;
    String hash;
    MerkleTree merkleTree;

    public Block(List<String> transactions, String previousHash, String hashAlgorithm) {
        this.timestamp = new Date().toString();
        this.transactions = new ArrayList<>(transactions);
        this.previousHash = previousHash;
        this.merkleTree = new MerkleTree(transactions, hashAlgorithm);
        this.merkleRoot = merkleTree.getRoot();
        this.hash = calculateHash();
    }

    public String calculateHash() {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            String input = timestamp + merkleRoot + previousHash;
            byte[] hashBytes = digest.digest(input.getBytes());
            StringBuilder hex = new StringBuilder();
            for (byte b : hashBytes) {
                String h = Integer.toHexString(0xff & b);
                if (h.length() == 1) hex.append('0');
                hex.append(h);
            }
            return hex.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException(e);
        }
    }

    public void addTransaction(String tx, String hashAlgo) {
        transactions.add(tx);
        this.merkleTree = new MerkleTree(transactions, hashAlgo);
        this.merkleRoot = merkleTree.getRoot();
        this.hash = calculateHash(); 
    }

    public boolean validate() {
        String currentRoot = new MerkleTree(transactions, "SHA-256").getRoot();
        return this.merkleRoot.equals(currentRoot) && this.hash.equals(calculateHash());
    }
}
