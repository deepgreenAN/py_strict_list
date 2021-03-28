# 構造の厳密なリスト 

プロパティとしてリストを採用する際などで，変更時に型チェックできる．セッターなどで利用するときも簡単に型チェックできるようにした．基本的に構造はコンストラクタで確定される．(構造から空リストを作ることもできる．)
あくまでも型チェック用のリストであり，速度の向上は無い．

## 使い方
ワーキングディレクトリにクローンするかパスを通せば使える． 

```python
from py_strict_list import StructureStrictList, TypeStrictList, LengthStrictList
```

## 型・長さ構造が厳密なリスト


```python
a = StructureStrictList([1,2],["a", "b"])
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-34-905093049281> in <module>
    ----> 1 a = StructureStrictList([1,2],["a", "b"])
    

    E:\py_strict_list\py_strict_list_ver1.py in __init__(self, *args)
          8         """
          9         super(StructureStrictList, self).__init__(args)
    ---> 10         self._get_structure()  # 構造を取得
         11 
         12     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_structure(self)
         14         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
         15         """
    ---> 16         self._type_structure = self._get_type_structure(self)
         17         self._length_structure = self._get_length_structure(self)
         18 
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_type_structure(list_like)
         35             raise Exception("list like object is enmty")
         36         if len(set(type_list)) > 1:  # リストの型の種類が一つ以上の場合
    ---> 37             raise Exception("list like object have to have same type items")
         38 
         39         # それぞれの型が全て等しいかチェック
    

    Exception: list like object have to have same type items



```python
a = StructureStrictList([1,2],[3])
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-35-337e9e91693a> in <module>
    ----> 1 a = StructureStrictList([1,2],[3])
    

    E:\py_strict_list\py_strict_list_ver1.py in __init__(self, *args)
          8         """
          9         super(StructureStrictList, self).__init__(args)
    ---> 10         self._get_structure()  # 構造を取得
         11 
         12     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_structure(self)
         15         """
         16         self._type_structure = self._get_type_structure(self)
    ---> 17         self._length_structure = self._get_length_structure(self)
         18 
         19     @staticmethod
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_length_structure(list_like)
         73                     raise Exception("list like object have to have same length recursive")
         74 
    ---> 75         item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
         76 
         77         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list_ver1.py in item_have_same_length(item)
         71                         item_have_same_length(item_child)
         72                 if len(length_list)!=0 and len(set(length_list))!=1:
    ---> 73                     raise Exception("list like object have to have same length recursive")
         74 
         75         item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
    

    Exception: list like object have to have same length recursive



```python
a = StructureStrictList([1,2],[3,4])
```


```python
a.length_structure
```




    {2: {2: None}}




```python
a.type_structure
```




    [[int]]



### 他のSSLとの比較


```python
b = StructureStrictList(3,4)
a.check_same_structure_with(b)
```




    False



### 他のリストとの比較


```python
c = [[5,6],[7,8]]
a.check_same_structure_with(c)
```




    True



### 要素との比較 

appendとかの型判定で利用


```python
a.check_item_structure([1,2])
```




    True




```python
a.check_item_structure([3])
```




    False



### append 


```python
a.append(1)
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-43-da0a5ad497c3> in <module>
    ----> 1 a.append(1)
    

    E:\py_strict_list\py_strict_list_ver1.py in append(self, item)
        202     def append(self, item):
        203         if not self.check_item_structure(item):
    --> 204             raise Exception("this item is restricted for append")
        205         super(StructureStrictList, self).append(item)
        206         self._get_structure()
    

    Exception: this item is restricted for append



```python
a.append([5,6])
a
```




    [[1, 2], [3, 4], [5, 6]]



###  extend


```python
a.extend([[7,8],[9,10],[11,12]])
a
```




    [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]]



### from_list 


```python
d = StructureStrictList.from_list([1,2,3])
d
```




    [1, 2, 3]




```python
d.length_structure
```




    {3: None}




```python
d.type_structure
```




    [int]



### 構造から空のSSLを作る 


```python
e = StructureStrictList.from_structures([[int]],{2: {2: None}})
e
```




    []




```python
e.append(1)
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-50-0292b4a997ee> in <module>
    ----> 1 e.append(1)
    

    E:\py_strict_list\py_strict_list_ver1.py in append(self, item)
        202     def append(self, item):
        203         if not self.check_item_structure(item):
    --> 204             raise Exception("this item is restricted for append")
        205         super(StructureStrictList, self).append(item)
        206         self._get_structure()
    

    Exception: this item is restricted for append



```python
e.append([1,2])
e
```




    [[1, 2]]



### セッターの定義時について 

リストをプロパティとする場合，セッターを

```python
@some_list.setter
def some_list(self, __some_list):
    if not self._some_list.check_same_structure_with(__some_list, include_outer_length=False):
        raise Exception("This some_list is invalid")
    self._some_list = StructureStrictList.from_list(__some_list)
```

とすれば，型を比較しリストを更新できる．

## 型が厳密なリスト 


```python
a = TypeStrictList(["a","b"],[1,2])
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-53-e265aa80b45c> in <module>
    ----> 1 a = TypeStrictList(["a","b"],[1,2])
    

    E:\py_strict_list\py_strict_list_ver1.py in __init__(self, *args)
          8         """
          9         super(StructureStrictList, self).__init__(args)
    ---> 10         self._get_structure()  # 構造を取得
         11 
         12     def _get_structure(self):
    

    <ipython-input-52-e53e34044fd4> in _get_structure(self)
          4         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
          5         """
    ----> 6         self._type_structure = self._get_type_structure(self)
          7 
          8     def check_same_structure_with(self, list_like, include_outer_length=True):
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_type_structure(list_like)
         35             raise Exception("list like object is enmty")
         36         if len(set(type_list)) > 1:  # リストの型の種類が一つ以上の場合
    ---> 37             raise Exception("list like object have to have same type items")
         38 
         39         # それぞれの型が全て等しいかチェック
    

    Exception: list like object have to have same type items



```python
a = TypeStrictList(["a","b"],"c")
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-54-2ef8de3b788c> in <module>
    ----> 1 a = TypeStrictList(["a","b"],"c")
    

    E:\py_strict_list\py_strict_list_ver1.py in __init__(self, *args)
          8         """
          9         super(StructureStrictList, self).__init__(args)
    ---> 10         self._get_structure()  # 構造を取得
         11 
         12     def _get_structure(self):
    

    <ipython-input-52-e53e34044fd4> in _get_structure(self)
          4         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
          5         """
    ----> 6         self._type_structure = self._get_type_structure(self)
          7 
          8     def check_same_structure_with(self, list_like, include_outer_length=True):
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_type_structure(list_like)
         48                     raise Exception("list like object have to have same type recursive")
         49 
    ---> 50         item_have_same_type(list_like)  # 長さが違う場合エラーがでる．
         51 
         52         def type_dicision(item):
    

    E:\py_strict_list\py_strict_list_ver1.py in item_have_same_type(item)
         46                         item_have_same_type(item_child)
         47                 if len(type_list)!=0 and len(set(type_list))!=1:
    ---> 48                     raise Exception("list like object have to have same type recursive")
         49 
         50         item_have_same_type(list_like)  # 長さが違う場合エラーがでる．
    

    Exception: list like object have to have same type recursive



```python
a = TypeStrictList(["a","b"],["c","d"])
```


```python
a.type_structure
```




    [[str]]



### append 


```python
a.append("a")
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-57-be817fbe9230> in <module>
    ----> 1 a.append("a")
    

    E:\py_strict_list\py_strict_list_ver1.py in append(self, item)
        202     def append(self, item):
        203         if not self.check_item_structure(item):
    --> 204             raise Exception("this item is restricted for append")
        205         super(StructureStrictList, self).append(item)
        206         self._get_structure()
    

    Exception: this item is restricted for append



```python
a.append(["e"])
a
```




    [['a', 'b'], ['c', 'd'], ['e']]




```python
b = TypeStrictList.from_type_structure([str])
```


```python
b.type_structure
```




    [str]




```python
b.append(["c"])
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-61-ea8bf38fa590> in <module>
    ----> 1 b.append(["c"])
    

    E:\py_strict_list\py_strict_list_ver1.py in append(self, item)
        202     def append(self, item):
        203         if not self.check_item_structure(item):
    --> 204             raise Exception("this item is restricted for append")
        205         super(StructureStrictList, self).append(item)
        206         self._get_structure()
    

    Exception: this item is restricted for append



```python
b.append("a")
b
```




    ['a']



## 長さが厳密なリスト


```python
a = LengthStrictList([1,2,3],[1,2])
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-64-2fd35d765fe9> in <module>
    ----> 1 a = LengthStrictList([1,2,3],[1,2])
    

    E:\py_strict_list\py_strict_list_ver1.py in __init__(self, *args)
          8         """
          9         super(StructureStrictList, self).__init__(args)
    ---> 10         self._get_structure()  # 構造を取得
         11 
         12     def _get_structure(self):
    

    <ipython-input-63-fcedf1fd2ad8> in _get_structure(self)
          4         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
          5         """
    ----> 6         self._length_structure = self._get_length_structure(self)
          7 
          8     def check_same_structure_with(self, list_like, include_outer_length=True):
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_length_structure(list_like)
         73                     raise Exception("list like object have to have same length recursive")
         74 
    ---> 75         item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
         76 
         77         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list_ver1.py in item_have_same_length(item)
         71                         item_have_same_length(item_child)
         72                 if len(length_list)!=0 and len(set(length_list))!=1:
    ---> 73                     raise Exception("list like object have to have same length recursive")
         74 
         75         item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
    

    Exception: list like object have to have same length recursive



```python
a = LengthStrictList([[1,2,3],[1,2]])
```


    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-65-d07a1ab9ed5c> in <module>
    ----> 1 a = LengthStrictList([[1,2,3],[1,2]])
    

    E:\py_strict_list\py_strict_list_ver1.py in __init__(self, *args)
          8         """
          9         super(StructureStrictList, self).__init__(args)
    ---> 10         self._get_structure()  # 構造を取得
         11 
         12     def _get_structure(self):
    

    <ipython-input-63-fcedf1fd2ad8> in _get_structure(self)
          4         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
          5         """
    ----> 6         self._length_structure = self._get_length_structure(self)
          7 
          8     def check_same_structure_with(self, list_like, include_outer_length=True):
    

    E:\py_strict_list\py_strict_list_ver1.py in _get_length_structure(list_like)
         73                     raise Exception("list like object have to have same length recursive")
         74 
    ---> 75         item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
         76 
         77         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list_ver1.py in item_have_same_length(item)
         69                     if isinstance(item_child, list):
         70                         length_list.append(len(item_child))
    ---> 71                         item_have_same_length(item_child)
         72                 if len(length_list)!=0 and len(set(length_list))!=1:
         73                     raise Exception("list like object have to have same length recursive")
    

    E:\py_strict_list\py_strict_list_ver1.py in item_have_same_length(item)
         71                         item_have_same_length(item_child)
         72                 if len(length_list)!=0 and len(set(length_list))!=1:
    ---> 73                     raise Exception("list like object have to have same length recursive")
         74 
         75         item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
    

    Exception: list like object have to have same length recursive



```python
a = LengthStrictList([2,3],[1,2])
a
```




    [[2, 3], [1, 2]]


