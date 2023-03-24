#include <iostream>
#include <string>
using namespace std;

int GetInt(string s)
{
    if (s.empty()) return 0;

    int ret = 0;
    int flag[96];

    memset(&flag, -1, sizeof(flag));
    int count = 0;
    int sIdx = -1;
    for (int idx = 0; idx < s.size(); ++idx)
    {
        char ele = (s.c_str())[idx];
        if (-1 == flag[ele - 32]
            || flag[ele - 32] <= sIdx)
        {
            ++count;
            if (count > ret) ret = count;
        }
        else
        {
            count = idx - flag[ele - 32];
            sIdx = flag[ele - 32];
        }

        flag[ele - 32] = idx;
    }

    return ret;
}

int lengthOfLongestSubstring(string s)
{
    if (s.empty()) return 0;
    int nMaxLen = 0;
    int nIdxDict[128];
    memset(&nIdxDict, -1, sizeof(nIdxDict));

    int nStart = -1;
    for (int i = 0; i < s.length(); ++i)
    {
        if (nIdxDict[s[i]] > nStart)
            nStart = nIdxDict[s[i]];

        nIdxDict[s[i]] = i;

        if ((i - nStart) > nMaxLen)
            nMaxLen = i - nStart;
    }

    return nMaxLen;
}

int main(int argc, char** argv)
{
    string str = "abcabcbb";
    if (argc > 1)
        str = argv[1];
    cout<<GetInt(str)<<endl;
    cout<<lengthOfLongestSubstring(str)<<endl;
    return 0;
}
