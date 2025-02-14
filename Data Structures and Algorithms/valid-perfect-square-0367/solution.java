class Solution {
    public boolean isPerfectSquare(int num) {
        int start = 0; 
        int mid = num / 2;
        int end = num; 

        if(num<0){
            return false; 
        }

        while(start <= end){
            mid = start + (end-start) / 2;

            if((long)mid*mid > num){
                end = mid-1; 
            }

            else if((long)mid * mid == num){
                return true; 
            }

            else{
                start = mid+1; 
            }

        }

        return false;
        
    }
}
