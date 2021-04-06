from .hook_func_ver1 import HookFunc


class PropertyList(list):
    """
    基底となるリスト
    """
    def __init__(self, *args):
        super(PropertyList, self).__init__(args)
        self._hook_func = HookFunc()  # ホック関数
        
    @property
    def hook_func(self):
        return self._hook_func

    @hook_func.setter
    def hook_func(self, another_hook_func):
        if isinstance(another_hook_func, HookFunc):
            self._hook_func = another_hook_func
    
    def append(self, *args, **kwargs):
        return_value = super(PropertyList, self).append(*args, **kwargs)
        self._hook_func()  # ホック関数の実行
        return return_value
    
    def extend(self, *args, **kwargs):
        return_value = super(PropertyList, self).extend(*args, **kwargs)
        self._hook_func()  # ホック関数の実行
        return return_value
    
    def insert(self, *args, **kwargs):
        return_value = super(PropertyList, self).insert(*args, **kwargs)
        self._hook_func()  # ホック関数の実行
        return return_value
    
    def remove(self, *args, **kwargs):
        return_value = super(PropertyList, self).remove(*args, **kwargs)
        self._hook_func()  # ホック関数の実行
        return return_value
    
    def pop(self, *args, **kwargs):
        return_value = super(PropertyList, self).pop(*args, **kwargs)
        self._hook_func()  # ホック関数の実行
        return return_value      


class StructureInvalidError(Exception):
    def __init__(self, strings):
        self.strings = strings
    def __str__(self):
        return self.strings


class StructureStrictList(PropertyList):
    """
    型と長さが再帰的に厳密なリスト
    """
    def __init__(self, *args):
        """
        コンストラクタの引数は普通のリストと変わらない
        """
        super(StructureStrictList, self).__init__(*args)  # PropertyListには展開して渡す
        self._get_structure()  # 構造を取得
        self.hook_func.add(self._get_structure)  # ホック関数に追加
        
    def _get_structure(self):
        """
        構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        """
        self._type_structure = self._get_type_structure(self)
        self._length_structure = self._get_length_structure(self)
        
    @staticmethod
    def _get_type_structure(list_like):
        """
        型構造を取得．取得する前に再帰的に型が正しいかチェックしている．
        """
        # (リスト以外の)型が全て等しいかチェック・リスト内のそれぞれの型が等しいかチェック
        all_type_list = [] 
        
        def item_have_same_type(item):
            type_list = []
            for item_child in item:
                type_list.append(type(item_child))
                if isinstance(item_child, list):
                    item_have_same_type(item_child)
                else:  # リスト以外
                   all_type_list.append(type(item_child)) 
            if len(type_list)!=0 and len(set(type_list))!=1:
                raise StructureInvalidError("list like object have to have same type recursively")
        
        if isinstance(list_like, list):  # リストでないと以下の処理が意味ないため
            item_have_same_type(list_like)  # リスト内のそれぞれの型が違う場合エラーがでる．

            if len(set(all_type_list)) == 0:  # リスト以外の型が存在しない場合
                raise StructureInvalidError("list like object is enmty")
            if len(set(all_type_list)) > 1:  # リスト以外の型の種類が一つ以上の場合
                raise StructureInvalidError("list like object have to have same type items")
        
        def type_dicision(item):
            if isinstance(item, list):  # リストの場合
                return [type_dicision(item[0])]
            else:
                return type(item)
        return type_dicision(list_like)
    
    @staticmethod
    def _get_length_structure(list_like):
        """
        長さ構造を取得．取得する前に長さが再帰的に等しいかチェックしている．
        """
        # それぞれのリストの長さが等しいかつリストとそれ以外が混在しない
        def item_have_same_length(item):
            length_list = []
            is_list_list = []
            for item_child in item:
                if isinstance(item_child, list):
                    length_list.append(len(item_child))
                    item_have_same_length(item_child)
                    is_list_list.append(True)
                else:
                    is_list_list.append(False)
            if len(length_list)!=0 and len(set(length_list))!=1:
                raise StructureInvalidError("list like object have to have same length recursively")
            if not (all(is_list_list) or not any(is_list_list)):  #（すべてリストかすべてリストでないとき）以外
                raise StructureInvalidError("list like object has save dimension as tree")
        
        if isinstance(list_like, list):
            item_have_same_length(list_like)  # 長さが違う場合エラーがでる．
        
        def length_dicision(item, structure_dict):
            if isinstance(item, list):  # リストの場合
                inner_structure_dict = {}
                inner_structure_dict[len(item)]=length_dicision(item[0],{})
                return inner_structure_dict
            else:
                return None
            
        all_structure_dict = length_dicision(list_like, {})
        return all_structure_dict
        
    def check_same_structure_with(self, list_like, include_outer_length=False):
        """
        list_like: list like object
            構造を自身と比較したいリスト
        include_outer_length int
            最も外側の長さを比較する構造に含めるかどうか
        """
        try:
            list_like_type_structure = self._get_type_structure(list_like)
            list_like_length_structure = self._get_length_structure(list_like)
        except:  #構造の取得に失敗した場合
            return False
        is_same_type_structure = self._type_structure == list_like_type_structure
        
        if include_outer_length: # 一番外側の比較も行う
            is_same_length_structure = self._length_structure == list_like_length_structure

        else:  # 一番外側の比較は行わない
            list_like_item_length_structure = list_like_length_structure[list(list_like_length_structure.keys())[0]]
            self_item_length_structure = self._length_structure[list(self._length_structure.keys())[0]]
            is_same_length_structure = self_item_length_structure == list_like_item_length_structure

        return is_same_type_structure and is_same_length_structure
        
    def check_item_structure(self, item):
        """
        item: any
            構造を自身の要素と比較したい要素候補
        """
        try:
            item_type_structure = self._get_type_structure(item)
            item_length_structure = self._get_length_structure(item)
        except:  #構造の取得に失敗した場合
            return False
        if isinstance(item, list):# itemがリストの場合
            is_same_type_structure = self._type_structure[0] == item_type_structure
            is_same_length_structure = self._length_structure[list(self._length_structure.keys())[0]] == item_length_structure
        else:  # itemがリストじゃない場合
            if not isinstance(self._type_structure[0], list):  # 自身のtype_structureのitemもリストでない場合
                is_same_type_structure = isinstance(item, self._type_structure[0])
                is_same_length_structure = True
            else:
                is_same_type_structure = False
                is_same_length_structure = False
        
        return is_same_type_structure and is_same_length_structure
    
    @classmethod
    def from_list(cls, _list):
        """
        リストからStructureStrictListを作成
        _list: list
            リスト
        """
        return cls(*_list)
    
    @classmethod
    def from_structures(cls, _type_structure, _length_structure):
        """
        型構造・長さ構造の二つから，空のStructureStrictListを作成
        """
        # 空の自身を作成
        instance = cls(None)
        super(PropertyList, instance).remove(None)  # 基底のスーパークラスのメソッド呼び出し
        instance._type_structure = _type_structure
        instance._length_structure = _length_structure
        return instance
    
    @property
    def type_structure(self):
        return self._type_structure
        
    @property
    def length_structure(self):
        return self._length_structure
    
    def append(self, item):
        if not self.check_item_structure(item):
            raise StructureInvalidError("This item is restricted for append")
        return_value = super(StructureStrictList, self).append(item)
        return return_value
        
    def extend(self, iterable):
        if not self.check_same_structure_with(list(iterable), include_outer_length=False):  # 外側の長さの比較は行わない
            raise StructureInvalidError("This iterable is restricted for extend")
        return_value = super(StructureStrictList, self).extend(iterable)
        return return_value
        
    def insert(self, i, item):
        if not self.check_item_structure(item):
            raise StructureInvalidError("This item is restricted for insert")
        return_value = super(StructureStrictList, self).insert(i, item)
        return return_value


class TypeStrictList(StructureStrictList):
    def _get_structure(self):
        """
        構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        """
        self._type_structure = self._get_type_structure(self)
    
    def check_same_structure_with(self, list_like, include_outer_length=False):
        """
        list_like: list like object
            構造を自身と比較したいリスト
        include_outer_length int
            最も外側の長さを比較する構造に含めるかどうか
        """
        try:
            list_like_type_structure = self._get_type_structure(list_like)
        except StructureInvalidError:  #構造の取得に失敗した場合
            return False
        is_same_type_structure = self._type_structure == list_like_type_structure
        
        return is_same_type_structure
    
    def check_item_structure(self, item):
        """
        item: any
            構造を自身の要素と比較したい要素候補
        """
        try:
            item_type_structure = self._get_type_structure(item)
        except StructureInvalidError:  #構造の取得に失敗した場合
            return False
        if isinstance(item, list):# itemがリストの場合
            is_same_type_structure = self._type_structure[0] == item_type_structure
        else:  # itemがリストじゃない場合
            if not isinstance(self._type_structure[0], list):  # 自身のtype_structureのitemもリストでない場合
                is_same_type_structure = isinstance(item, self._type_structure[0])
            else:
                is_same_type_structure = False
        
        return is_same_type_structure
    
    @classmethod
    def from_type_structure(cls, _type_structure):
        """
        型構造構造から，空のStructureStrictListを作成
        """
        instance = cls(None)
        super(PropertyList, instance).remove(None)  # 基底のスーパークラスのメソッド呼び出し
        instance._type_structure = _type_structure
        return instance


class LengthStrictList(StructureStrictList):
    def _get_structure(self):
        """
        構造を取得するためのメソッド．基本的に自身が変更されたときに呼ぶ
        """
        self._length_structure = self._get_length_structure(self)
       
    def check_same_structure_with(self, list_like, include_outer_length=False):
        """
        list_like: list like object
            構造を自身と比較したいリスト
        include_outer_length int
            最も外側の長さを比較する構造に含めるかどうか
        """
        try:
            list_like_length_structure = self._get_length_structure(list_like)
        except StructureInvalidError:  #構造の取得に失敗した場合
            return False
        
        if include_outer_length: # 一番外側の比較も行う
            is_same_length_structure = self._length_structure == list_like_length_structure

        else:  # 一番外側の比較は行わない
            list_like_item_length_structure = list_like_length_structure[list(list_like_length_structure.keys())[0]]
            self_item_length_structure = self._length_structure[list(self._length_structure.keys())[0]]
            is_same_length_structure = self_item_length_structure == list_like_item_length_structure

        return is_same_length_structure
    
    def check_item_structure(self, item):
        """
        item: any
            構造を自身の要素と比較したい要素候補
        """
        try:
            item_length_structure = self._get_length_structure(item)
        except StructureInvalidError:  #構造の取得に失敗した場合
            return False
        if isinstance(item, list):# itemがリストの場合
            is_same_length_structure = self._length_structure[list(self._length_structure.keys())[0]] == item_length_structure
        else:  # itemがリストじゃない場合
            is_same_length_structure = self._length_structure[list(self._length_structure.keys())[0]] is None  # 自身ののitemもリストでない場合
        
        return is_same_length_structure
    
    @classmethod
    def from_length_structure(cls, _length_structure):
        instance = cls(None)
        super(PropertyList, instance).remove(None)  # 基底のスーパークラスのメソッド呼び出し
        instance._length_structure = _length_structure
        return instance


def strict_list_property(private_name, include_outer_length=False):
    """
    StructureStrictListをpropertyに登録する関数
    
    private_name: str
        propertyで隠す変数
    include_outer_lengh: bool
        もっとも外側の長さを比較に含めるかどうか
    
    """
    def getter(instance):
        return instance.__dict__[private_name]

    def setter(instance, list_like):
        if not instance.__dict__[private_name].check_same_structure_with(list_like,
                                                                         include_outer_length=include_outer_length
                                                                         ):
            raise StructureInvalidError("This list-like is invalid")
        previous_hook_func = instance.__dict__[private_name].hook_func
        instance.__dict__[private_name] = type(instance.__dict__[private_name]).from_list(list_like)
        previous_hook_func()  # hook_funcの実行
        instance.__dict__[private_name].hook_func = previous_hook_func
        
    return property(getter, setter)

if __name__ == "__main__":
    pass