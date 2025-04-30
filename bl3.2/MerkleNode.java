public class MerkleNode {
    String hash;
    MerkleNode left;
    MerkleNode right;

    MerkleNode(String hash) {
        this.hash = hash;
    }

    MerkleNode(MerkleNode left, MerkleNode right, String hash) {
        this.left = left;
        this.right = right;
        this.hash = hash;
    }
}
