# TPJL (TechGeeks Portable JSON Language)
![PyPI Release](https://github.com/TechGeeks-Dev/PJSONLang/actions/workflows/Release-Create.yml/badge.svg)
TPJL (TechGeeks Portable JSON Language) is a free & OpenSource Portable version of JSON.
<br>You can send a .tpjl file to anyone and he can open it with the read() function and can write with the write() function!
<br>Please Support us by Contributing by creating a pull request on GitHub.<br>
                                                                                           Thanks,<br><br>
                                                                                                                                                                                                        Rajdeep Malakar,<br>
                                                                                                                                                                                                    Chief Executive Director,<br><br>
                                                                                                                                                                                                [TechGeeks](https://tgeeks.cf)<br>
                                                                                                            
## Usage

```python3
from tpjl import TPJLang
data = {
    "0": {
        "_id": 0,
        "_name": "Rajdeep Malakar",
        "email": "Rajdeep@tgeeks.cf",
        "technology": [
            "Python",
            "PHP",
            "HTML/CSS/JavaScript",
            "C/C++",
            "Java",
            "TPJLang.py3"
        ]
    }
}
# To Write
TPJLang.write("sample", data) # You'll get a new sample.tpjl file
# To Read
sample = TPJLang.read("sample")
print(sample) # To Print All
sample = sample["0"]
print(sample["_name"]) # To Print the name of the Person with the ID of 0
```