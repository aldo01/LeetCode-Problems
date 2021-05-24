
//Given an integer array nums and an integer k, return the maximum length of a subarray that sums to k. If there isn't one, return 0 instead.
class Solution {
    public int maxSubArrayLen(int[] nums, int k) {
        
       int max=0;
        int sum=0;
        HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
        
        for(int i=0;i<nums.length;i++){
            
            sum+= nums[i];
            
            if(sum==k)
                max=i+1;
            
            else if(map.containsKey(sum-k))
                max= Math.max(max, i-map.get(sum-k));
            
            if(!map.containsKey(sum))
                map.put(sum,i);
        }
        
        return max;
    }
}