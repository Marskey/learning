#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result;
        unordered_map<int, int> subNum;
        for (int i = 0; i < nums.size(); ++i)
        {
            unordered_map<int, int>::iterator it = subNum.find(nums[i]);
            if (subNum.end() != it)
            {
                result.push_back(i);
                result.push_back(it->second);
                break;
            }
            int need = target - nums[i];
            subNum[need] = i;
        }
        return result;
    }
};

int main ()
{
    std::string str("0");
    //cout << str;
    return 0;
}
