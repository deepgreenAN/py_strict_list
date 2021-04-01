# 構造の厳密なリスト 

プロパティとしてリストを採用する際などで，変更時に型チェックできる．セッターなどで利用するときも簡単に型チェックできるようにした．基本的に構造はコンストラクタで確定される．(構造から空リストを作ることもできる．)
あくまでも型チェック用のリストであり，速度の向上は無い．

## test
```
python setup.py test
```

## installation
```
pip install git+https://github.com/deepgreenAN/py_strict_list
```
あるいは
クローンした後，そのディレクトリで以下を実行する．
```
python setup.py install
```

## 使い方
```python
from py_strict_list import StructureStrictList, TypeStrictList, LengthStrictList
```

## 型・長さ構造が厳密なリスト


```python
a = StructureStrictList([1,2],["a", "b"])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-3-905093049281> in <module>
    ----> 1 a = StructureStrictList([1,2],["a", "b"])
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in __init__(self, *args)
         15         """
         16         super(StructureStrictList, self).__init__(args)
    ---> 17         self._get_structure()  # 構造を取得
         18 
         19     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_structure(self)
         21         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
         22         """
    ---> 23         self._type_structure = self._get_type_structure(self)
         24         self._length_structure = self._get_length_structure(self)
         25 
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_type_structure(list_like)
         49                 raise StructureInvalidError("list like object is enmty")
         50             if len(set(all_type_list)) > 1:  # リスト以外の型の種類が一つ以上の場合
    ---> 51                 raise StructureInvalidError("list like object have to have same type items")
         52 
         53         def type_dicision(item):
    

    StructureInvalidError: list like object have to have same type items



```python
a = StructureStrictList([1,2],[3])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-4-337e9e91693a> in <module>
    ----> 1 a = StructureStrictList([1,2],[3])
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in __init__(self, *args)
         15         """
         16         super(StructureStrictList, self).__init__(args)
    ---> 17         self._get_structure()  # 構造を取得
         18 
         19     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_structure(self)
         22         """
         23         self._type_structure = self._get_type_structure(self)
    ---> 24         self._length_structure = self._get_length_structure(self)
         25 
         26     @staticmethod
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_length_structure(list_like)
         80 
         81         if isinstance(list_like, list):
    ---> 82             item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
         83 
         84         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in item_have_same_length(item)
         75                     is_list_list.append(False)
         76             if len(length_list)!=0 and len(set(length_list))!=1:
    ---> 77                 raise StructureInvalidError("list like object have to have same length recursively")
         78             if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
         79                 raise StructureInvalidError("list like object has save dimension as tree")
    

    StructureInvalidError: list like object have to have same length recursively



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

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-12-da0a5ad497c3> in <module>
    ----> 1 a.append(1)
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in append(self, item)
        171     def append(self, item):
        172         if not self.check_item_structure(item):
    --> 173             raise StructureInvalidError("This item is restricted for append")
        174         return_value = super(StructureStrictList, self).append(item)
        175         self._get_structure()
    

    StructureInvalidError: This item is restricted for append



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



もちろん，その他のリストのメソッドも利用できる．

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

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-19-0292b4a997ee> in <module>
    ----> 1 e.append(1)
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in append(self, item)
        171     def append(self, item):
        172         if not self.check_item_structure(item):
    --> 173             raise StructureInvalidError("This item is restricted for append")
        174         return_value = super(StructureStrictList, self).append(item)
        175         self._get_structure()
    

    StructureInvalidError: This item is restricted for append



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

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-21-e265aa80b45c> in <module>
    ----> 1 a = TypeStrictList(["a","b"],[1,2])
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in __init__(self, *args)
         15         """
         16         super(StructureStrictList, self).__init__(args)
    ---> 17         self._get_structure()  # 構造を取得
         18 
         19     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_structure(self)
        204         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        205         """
    --> 206         self._type_structure = self._get_type_structure(self)
        207 
        208     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_type_structure(list_like)
         49                 raise StructureInvalidError("list like object is enmty")
         50             if len(set(all_type_list)) > 1:  # リスト以外の型の種類が一つ以上の場合
    ---> 51                 raise StructureInvalidError("list like object have to have same type items")
         52 
         53         def type_dicision(item):
    

    StructureInvalidError: list like object have to have same type items



```python
a = TypeStrictList(["a","b"],"c")
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-22-2ef8de3b788c> in <module>
    ----> 1 a = TypeStrictList(["a","b"],"c")
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in __init__(self, *args)
         15         """
         16         super(StructureStrictList, self).__init__(args)
    ---> 17         self._get_structure()  # 構造を取得
         18 
         19     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_structure(self)
        204         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        205         """
    --> 206         self._type_structure = self._get_type_structure(self)
        207 
        208     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_type_structure(list_like)
         44 
         45         if isinstance(list_like, list):  # リストでないと以下の処理が意味ないため
    ---> 46             item_have_same_type(list_like)  # リスト内のそれぞれの型が違う場合エラーがでる．
         47 
         48             if len(set(all_type_list)) == 0:  # リスト以外の型が存在しない場合
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in item_have_same_type(item)
         41                    all_type_list.append(type(item_child))
         42             if len(type_list)!=0 and len(set(type_list))!=1:
    ---> 43                 raise StructureInvalidError("list like object have to have same type recursively")
         44 
         45         if isinstance(list_like, list):  # リストでないと以下の処理が意味ないため
    

    StructureInvalidError: list like object have to have same type recursively



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

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-25-be817fbe9230> in <module>
    ----> 1 a.append("a")
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in append(self, item)
        171     def append(self, item):
        172         if not self.check_item_structure(item):
    --> 173             raise StructureInvalidError("This item is restricted for append")
        174         return_value = super(StructureStrictList, self).append(item)
        175         self._get_structure()
    

    StructureInvalidError: This item is restricted for append



```python
a.append(["e"])
a
```




    [['a', 'b'], ['c', 'd'], ['e']]



### 構造から空のTSLを作成する


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

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-29-ea8bf38fa590> in <module>
    ----> 1 b.append(["c"])
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in append(self, item)
        171     def append(self, item):
        172         if not self.check_item_structure(item):
    --> 173             raise StructureInvalidError("This item is restricted for append")
        174         return_value = super(StructureStrictList, self).append(item)
        175         self._get_structure()
    

    StructureInvalidError: This item is restricted for append



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

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-31-2fd35d765fe9> in <module>
    ----> 1 a = LengthStrictList([1,2,3],[1,2])
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in __init__(self, *args)
         15         """
         16         super(StructureStrictList, self).__init__(args)
    ---> 17         self._get_structure()  # 構造を取得
         18 
         19     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_structure(self)
        256         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        257         """
    --> 258         self._length_structure = self._get_length_structure(self)
        259 
        260     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_length_structure(list_like)
         80 
         81         if isinstance(list_like, list):
    ---> 82             item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
         83 
         84         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in item_have_same_length(item)
         75                     is_list_list.append(False)
         76             if len(length_list)!=0 and len(set(length_list))!=1:
    ---> 77                 raise StructureInvalidError("list like object have to have same length recursively")
         78             if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
         79                 raise StructureInvalidError("list like object has save dimension as tree")
    

    StructureInvalidError: list like object have to have same length recursively



```python
a = LengthStrictList([[1,2,3],[1,2]])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-32-d07a1ab9ed5c> in <module>
    ----> 1 a = LengthStrictList([[1,2,3],[1,2]])
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in __init__(self, *args)
         15         """
         16         super(StructureStrictList, self).__init__(args)
    ---> 17         self._get_structure()  # 構造を取得
         18 
         19     def _get_structure(self):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_structure(self)
        256         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        257         """
    --> 258         self._length_structure = self._get_length_structure(self)
        259 
        260     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in _get_length_structure(list_like)
         80 
         81         if isinstance(list_like, list):
    ---> 82             item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
         83 
         84         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in item_have_same_length(item)
         70                 if isinstance(item_child, list):
         71                     length_list.append(len(item_child))
    ---> 72                     item_have_same_length(item_child)
         73                     is_list_list.append(True)
         74                 else:
    

    E:\py_strict_list\py_strict_list\py_strict_list.py in item_have_same_length(item)
         75                     is_list_list.append(False)
         76             if len(length_list)!=0 and len(set(length_list))!=1:
    ---> 77                 raise StructureInvalidError("list like object have to have same length recursively")
         78             if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
         79                 raise StructureInvalidError("list like object has save dimension as tree")
    

    StructureInvalidError: list like object have to have same length recursively



```python
a = LengthStrictList([2,3],[1,2])
a
```




    [[2, 3], [1, 2]]