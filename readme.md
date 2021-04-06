# 構造の厳密なリスト 

プロパティとしてリストを採用するのを想定し，変更時に自動で型チェックを行うリスト．
セッターなどで利用するときも簡単に型チェックできる．基本的に構造はコンストラクタで確定する(構造から空リストを作ることもできる．)．
あくまでも型チェック用のリストであり，速度の向上は無い．
より複雑なバリデーションを使いたいなら、[Cerberus](https://github.com/pyeve/cerberus)等のバリデーションツールを利用するべき

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
from py_strict_list import StructureStrictList, TypeStrictList, LengthStrictList, strict_list_property
```

## 型・長さ構造が厳密なリスト


```python
a = StructureStrictList([1,2],["a", "b"])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-3-905093049281> in <module>
    ----> 1 a = StructureStrictList([1,2],["a", "b"])
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in __init__(self, *args)
         56         """
         57         super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
    ---> 58         self._get_structure()  # 構造を取得
         59         self.hook_func.add(self._get_structure)  # ホック関数に追加
         60 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_structure(self)
         63         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
         64         """
    ---> 65         self._type_structure = self._get_type_structure(self)
         66         self._length_structure = self._get_length_structure(self)
         67 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_type_structure(list_like)
         91                 raise StructureInvalidError("list like object is enmty")
         92             if len(set(all_type_list)) > 1:  # リスト以外の型の種類が一つ以上の場合
    ---> 93                 raise StructureInvalidError("list like object have to have same type items")
         94 
         95         def type_dicision(item):
    

    StructureInvalidError: list like object have to have same type items



```python
a = StructureStrictList([1,2],[3])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-33-337e9e91693a> in <module>
    ----> 1 a = StructureStrictList([1,2],[3])
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in __init__(self, *args)
         56         """
         57         super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
    ---> 58         self._get_structure()  # 構造を取得
         59         self.hook_func.add(self._get_structure)  # ホック関数に追加
         60 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_structure(self)
         64         """
         65         self._type_structure = self._get_type_structure(self)
    ---> 66         self._length_structure = self._get_length_structure(self)
         67 
         68     @staticmethod
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_length_structure(list_like)
        122 
        123         if isinstance(list_like, list):
    --> 124             item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
        125 
        126         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in item_have_same_length(item)
        117                     is_list_list.append(False)
        118             if len(length_list)!=0 and len(set(length_list))!=1:
    --> 119                 raise StructureInvalidError("list like object have to have same length recursively")
        120             if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
        121                 raise StructureInvalidError("list like object has save dimension as tree")
    

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

    <ipython-input-11-da0a5ad497c3> in <module>
    ----> 1 a.append(1)
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in append(self, item)
        213     def append(self, item):
        214         if not self.check_item_structure(item):
    --> 215             raise StructureInvalidError("This item is restricted for append")
        216         return_value = super(StructureStrictList, self).append(item)
        217         return return_value
    

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

    <ipython-input-18-0292b4a997ee> in <module>
    ----> 1 e.append(1)
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in append(self, item)
        213     def append(self, item):
        214         if not self.check_item_structure(item):
    --> 215             raise StructureInvalidError("This item is restricted for append")
        216         return_value = super(StructureStrictList, self).append(item)
        217         return return_value
    

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

とすれば，型を比較しリストを更新できる．後述する`py_strict_list.strict_list_property`を利用してもよい．

## 型が厳密なリスト 


```python
a = TypeStrictList(["a","b"],[1,2])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-20-e265aa80b45c> in <module>
    ----> 1 a = TypeStrictList(["a","b"],[1,2])
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in __init__(self, *args)
         56         """
         57         super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
    ---> 58         self._get_structure()  # 構造を取得
         59         self.hook_func.add(self._get_structure)  # ホック関数に追加
         60 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_structure(self)
        235         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        236         """
    --> 237         self._type_structure = self._get_type_structure(self)
        238 
        239     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_type_structure(list_like)
         91                 raise StructureInvalidError("list like object is enmty")
         92             if len(set(all_type_list)) > 1:  # リスト以外の型の種類が一つ以上の場合
    ---> 93                 raise StructureInvalidError("list like object have to have same type items")
         94 
         95         def type_dicision(item):
    

    StructureInvalidError: list like object have to have same type items



```python
a = TypeStrictList(["a","b"],"c")
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-21-2ef8de3b788c> in <module>
    ----> 1 a = TypeStrictList(["a","b"],"c")
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in __init__(self, *args)
         56         """
         57         super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
    ---> 58         self._get_structure()  # 構造を取得
         59         self.hook_func.add(self._get_structure)  # ホック関数に追加
         60 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_structure(self)
        235         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        236         """
    --> 237         self._type_structure = self._get_type_structure(self)
        238 
        239     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_type_structure(list_like)
         86 
         87         if isinstance(list_like, list):  # リストでないと以下の処理が意味ないため
    ---> 88             item_have_same_type(list_like)  # リスト内のそれぞれの型が違う場合エラーがでる．
         89 
         90             if len(set(all_type_list)) == 0:  # リスト以外の型が存在しない場合
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in item_have_same_type(item)
         83                    all_type_list.append(type(item_child))
         84             if len(type_list)!=0 and len(set(type_list))!=1:
    ---> 85                 raise StructureInvalidError("list like object have to have same type recursively")
         86 
         87         if isinstance(list_like, list):  # リストでないと以下の処理が意味ないため
    

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

    <ipython-input-24-be817fbe9230> in <module>
    ----> 1 a.append("a")
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in append(self, item)
        213     def append(self, item):
        214         if not self.check_item_structure(item):
    --> 215             raise StructureInvalidError("This item is restricted for append")
        216         return_value = super(StructureStrictList, self).append(item)
        217         return return_value
    

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

    <ipython-input-28-ea8bf38fa590> in <module>
    ----> 1 b.append(["c"])
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in append(self, item)
        213     def append(self, item):
        214         if not self.check_item_structure(item):
    --> 215             raise StructureInvalidError("This item is restricted for append")
        216         return_value = super(StructureStrictList, self).append(item)
        217         return return_value
    

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

    <ipython-input-30-2fd35d765fe9> in <module>
    ----> 1 a = LengthStrictList([1,2,3],[1,2])
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in __init__(self, *args)
         56         """
         57         super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
    ---> 58         self._get_structure()  # 構造を取得
         59         self.hook_func.add(self._get_structure)  # ホック関数に追加
         60 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_structure(self)
        287         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        288         """
    --> 289         self._length_structure = self._get_length_structure(self)
        290 
        291     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_length_structure(list_like)
        122 
        123         if isinstance(list_like, list):
    --> 124             item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
        125 
        126         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in item_have_same_length(item)
        117                     is_list_list.append(False)
        118             if len(length_list)!=0 and len(set(length_list))!=1:
    --> 119                 raise StructureInvalidError("list like object have to have same length recursively")
        120             if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
        121                 raise StructureInvalidError("list like object has save dimension as tree")
    

    StructureInvalidError: list like object have to have same length recursively



```python
a = LengthStrictList([[1,2,3],[1,2]])
```


    ---------------------------------------------------------------------------

    StructureInvalidError                     Traceback (most recent call last)

    <ipython-input-31-d07a1ab9ed5c> in <module>
    ----> 1 a = LengthStrictList([[1,2,3],[1,2]])
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in __init__(self, *args)
         56         """
         57         super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
    ---> 58         self._get_structure()  # 構造を取得
         59         self.hook_func.add(self._get_structure)  # ホック関数に追加
         60 
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_structure(self)
        287         構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        288         """
    --> 289         self._length_structure = self._get_length_structure(self)
        290 
        291     def check_same_structure_with(self, list_like, include_outer_length=False):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in _get_length_structure(list_like)
        122 
        123         if isinstance(list_like, list):
    --> 124             item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
        125 
        126         def length_dicision(item, structure_dict):
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in item_have_same_length(item)
        112                 if isinstance(item_child, list):
        113                     length_list.append(len(item_child))
    --> 114                     item_have_same_length(item_child)
        115                     is_list_list.append(True)
        116                 else:
    

    E:\py_strict_list\py_strict_list\py_strict_list_ver2.py in item_have_same_length(item)
        117                     is_list_list.append(False)
        118             if len(length_list)!=0 and len(set(length_list))!=1:
    --> 119                 raise StructureInvalidError("list like object have to have same length recursively")
        120             if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
        121                 raise StructureInvalidError("list like object has save dimension as tree")
    

    StructureInvalidError: list like object have to have same length recursively



```python
a = LengthStrictList([2,3],[1,2])
a
```




    [[2, 3], [1, 2]]



## その他便利機能

### 要素の変更時に関数をホックできる． 

リストをプロパティとして利用する場合に，要素が変更したときに特定のメソッドを呼びたいことがある(そのプロパティの要素によって他のプロパティの値が変わる場合など)．
各リストの`hook_func`属性の`add`メソッドで関数を登録することによって，そのリストが変更されたときにその関数を呼ぶことができる．
その関数では再帰的な変更を行わないよう注意する．


```python
a = StructureStrictList(1,2,3,4)
b = sum(a)
b
```




    10




```python
def modify_b():  # 引数の無い関数
    global b
    b = sum(a)

a.hook_func.add(modify_b)
```


```python
a.append(5)
a
```




    [1, 2, 3, 4, 5]




```python
b
```



    15

ホック関数を追加した場合，セッターの定義は以下のようになる．

```python
@some_list.setter
def some_list(self, __some_list):
    if not self._some_list.check_same_structure_with(__some_list, include_outer_length=False):
        raise Exception("This some_list is invalid")
    pre_hook_func = self._some_list.hook_func
    self._some_list = StructureStrictList.from_list(__some_list)
    pre_hook_func()  # ホック関数の実行
    self._some_list.hook_func = pre_hook_func
```
これでは面倒なので、同じことのできる`py_strict_list.strict_list_property`が利用できる．property関数と同様に、クラスの直下に以下のように記述する．
```python
some_list = strict_list_property("_some_list", include_outer_length=False)
```