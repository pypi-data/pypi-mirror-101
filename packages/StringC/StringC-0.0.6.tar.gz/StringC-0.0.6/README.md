# StringC
This Package inherits from str Class   
Attributes:  
    Any string  

# Example:
```
from StringC import StringC
string = StringC("تاریخ برعکس ۱۳۹۹-۱۱-۳۰ تاریخ میلادی 1999/03/02 و تاریخ میلادی برعکس 05/12/95 حروف عربی مثل
كيك ۱۳۹۹/۱۱/۳۰ تاریخ")
string.convert
```
# Output:
"تاریخ برعکس 1399-11-30 تاریخ میلادی 1999/03/02 و تاریخ میلادی برعکس 05/12/95 حروف عربی مثل کیک 1399/11/30 تاریخ"  
# dates method
:param content: str  
:return: list of datetime object  
At the beginning :  
-Any Number in string will convert to En string Number -Any Arabic Character in string will convert to Farsi  
For now, it just finds dates in numeric formats which are separated with characters like "-" or "/" or "."  
There is no difference if date is Jalali or Gregorian or Characters are Fa or Ar, this function convert date to  
Gregorian datetime object  
# Example:
```
from StringC import StringC
string = "Today is 1400/01/18"
type(StringC.dates(string))
type(StringC.dates(string)[0])
StringC.dates(string)
```
# Output:
`<class 'list'>  
<class 'datetime.datetime'>  
[datetime.datetime(2021, 4, 7, 0, 0)]  
# Example:
```
string = "today is 2021/04/05"
```
# Output:
[datetime.datetime(2021, 4, 5, 0, 0)]  
# Example:
```
string = "today is 2021/04/07 and Today is 1400/01/18 yesterday was 17/01/1400 yesterday also was 06/04/2021"
```
# Output:
[  
datetime.datetime(2021, 4, 7, 0, 0),  
datetime.datetime(2021, 4, 7, 0, 0),  
datetime.datetime(2021, 4, 6, 0, 0),  
datetime.datetime(2021, 4, 6, 0, 0)  
]  
