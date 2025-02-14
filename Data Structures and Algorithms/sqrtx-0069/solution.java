class Solution {
    public int mySqrt(int x) {
        int current = 0; 
        if(x<=1){
            return x; 
        }
        else{
            for(int i =1; (long)i*i<=x; i++){
                if(((long)i*i) == x){
                    return i; 
                }
                else{
                    current = i; 
                }
            }
        }

        return current; 
    }
}
