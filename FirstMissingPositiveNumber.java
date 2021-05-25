//Given an unsorted integer array nums, find the smallest missing positive integer.

//You must implement an algorithm that runs in O(n) time and uses constant extra space.



class Solution {
    public int firstMissingPositive(int[] nums) {
         
        int n = nums.length;
        int isPresent =0;
        for(int i=0 ; i<n; i++){
            
            if(nums[i]==1){
                isPresent++;
            }
        }
        if(isPresent==0)
            return 1;
        
        for(int i=0; i< n ; i++){
            if(nums[i]<=0 || nums[i]> n ){
                nums[i]=1;
            }
        }
        
        for(int i=0; i<n ; i++){
           int a = Math.abs(nums[i]);
            if (a==n)
                nums[0]= -Math.abs(nums[0]);
            
            else
                nums[a]= -Math.abs(nums[a]); 
        }
        for(int i=1; i<n ;i++){
            if(nums[i]>0)
                return i;
        }
        
        if(nums[0]>0)
            return n;
        
        return n+1;
    }
}