import java.util.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class MerkleTree {
    private List<String> transactions;
    private String hashAlgorithm;
    private MerkleNode root;

    public MerkleTree(List<String> transactions, String hashAlgorithm) {
        this.transactions = transactions;
        this.hashAlgorithm = hashAlgorithm;
        this.root = buildTree(transactions);
    }

    private MerkleNode buildTree(List<String> levelData) {
        List<MerkleNode> nodes = new ArrayList<>();
        for (String tx : levelData) {
            nodes.add(new MerkleNode(hash(tx)));
        }

        while (nodes.size() > 1) {
            List<MerkleNode> newLevel = new ArrayList<>();
            for (int i = 0; i < nodes.size(); i += 2) {
                MerkleNode left = nodes.get(i);
                MerkleNode right = (i + 1 < nodes.size()) ? nodes.get(i + 1) : new MerkleNode("");
                String combinedHash = hash(left.hash + right.hash);
                newLevel.add(new MerkleNode(left, right, combinedHash));
            }
            nodes = newLevel;
        }

        return nodes.get(0);
    }

    private String hash(String input) {
        try {
            MessageDigest digest = MessageDigest.getInstance(hashAlgorithm);
            byte[] hashBytes = digest.digest(input.getBytes());
            StringBuilder hex = new StringBuilder();
            for (byte b : hashBytes) {
                String h = Integer.toHexString(0xff & b);
                if (h.length() == 1) hex.append('0');
                hex.append(h);
            }
            return hex.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Invalid algorithm: " + hashAlgorithm);
        }
    }

    public String getRoot() {
        return root.hash;
    }

    public void printTree() {
        printNode(root, 0);
    }

    private void printNode(MerkleNode node, int level) {
        if (node == null) return;
        printNode(node.right, level + 1);
        System.out.println("  ".repeat(level) + node.hash);
        printNode(node.left, level + 1);
    }
}
