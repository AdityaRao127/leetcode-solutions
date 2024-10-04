class Solution {
    public int superPow(int a, int[] b) {
        int mod = 1337;
        a = a % mod; // Reduce a modulo 1337 initially
        int result = 1;

        // Loop through the array b to calculate the final result
        for (int num : b) {
            // First, handle the result raised to the power of 10 modulo 1337
            result = powMod(result, 10, mod);

            // Then, multiply by a^num % mod
            result = (result * powMod(a, num, mod)) % mod;
        }

        return result;
    }

    // Helper to calculate (base^exp) % mod
    private int powMod(int base, int exp, int mod) {
        int res = 1;
        base = base % mod; // Reduce base modulo mod to avoid overflow

        for (int i = 0; i < exp; i++) {
            res = (res * base) % mod;
        }

        return res;
    }
}

