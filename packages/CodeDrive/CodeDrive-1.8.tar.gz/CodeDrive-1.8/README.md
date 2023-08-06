# CodeDrive

This is a **Python Library** contains some basic programs given in schools for assessments.

It has only one **Class**: **Functions**


```

Example of how to use this module:

from CodeDrive import Functions as fn
#or the alternative way
import CodeDrive.Functions as cf

#Now you want to run a palindrome test, so you need to do:

user = int(input("Enter number: "))

test = fn.palindromeNum(user) #This function will return True if the number passes the test, else False

if test == True:
    print(f"{user} is a palindrome number")
else:
    print(f"{user} is not a palindrome number")


```

To **upgrade** to the latest version, use:

```
pip install --upgrade CodeDrive
```

or 

```
python -m pip install --upgrade CodeDrive
```
