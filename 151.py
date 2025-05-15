def reverseWords(s):
        res=""
        count=0
        for i in range(len(s)-1,-1,-1):
            if s[i]==" ":
                res+=s[i+1:i+count+1]
                res+=" "
                count=0
                print(res)
            else:
                count+=1
        res+=s[0:count]
        res=" ".join(res.split())
        print(res)       
        return res
k="a good   example"        
reverseWords(k)