import unittest
from functools import reduce

from py_strict_list import StructureStrictList, TypeStrictList, LengthStrictList
from py_strict_list import StructureInvalidError, strict_list_property, StructureListValidator


class TestSSL(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(StructureInvalidError):
            StructureStrictList([1,2],2)
        with self.assertRaises(StructureInvalidError):
            StructureStrictList([1,2],[3,4,5])    
        with self.assertRaises(StructureInvalidError):
            StructureStrictList([1,2],["a","b"])
        with self.assertRaises(StructureInvalidError):
            StructureStrictList([[[1,2],[2]],[[3,4],[1,2]]])
        with self.assertRaises(StructureInvalidError):
            StructureStrictList("1",1)
            
        StructureStrictList([[1,2],[3,4]])
        
    def test_structures(self):
        x = StructureStrictList([1,2],[3,4])
        self.assertEqual(x.length_structure, {2:{2:None}})
        self.assertEqual(x.type_structure, [[int]])
        
    
    def test_check_save_structure_with(self):
        x = StructureStrictList([1,2],[3,4])
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]]))
        self.assertFalse(x.check_same_structure_with([3,4]))
        self.assertFalse(x.check_same_structure_with([["a","b"],["c","d"]]))
        
        self.assertFalse(x.check_same_structure_with([[5,6],[7,8],[9,10]], 
                                                     include_outer_length=True))
        
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]], 
                                                    include_outer_length=False))        
    
    def test_check_item_structure(self):
        x = StructureStrictList([1,2],[3,4])
        self.assertTrue(x.check_item_structure([5,6]))
        self.assertFalse(x.check_item_structure([7,8,9]))
        self.assertFalse(x.check_item_structure(5))
        self.assertFalse(x.check_item_structure(["a","b"]))
        
    def test_list_method_add(self):
        x = StructureStrictList([1,2],[3,4])
        with self.assertRaises(StructureInvalidError):
            x.append(2)
        with self.assertRaises(StructureInvalidError):
            x.append(["a","b"])
        with self.assertRaises(StructureInvalidError):
            x.append([[1,2]])
        with self.assertRaises(StructureInvalidError):
            x.append([1,2,3])
        
        x.append([1,2])
        
        with self.assertRaises(StructureInvalidError):
            x.extend([1,2])
        with self.assertRaises(StructureInvalidError):
            x.extend([[1,2],["a", "b"]])
        with self.assertRaises(StructureInvalidError):
            x.extend([[1,2],[3,4,5]])  
            
        x.extend([[11,12],[23,34]])
        
        
        with self.assertRaises(StructureInvalidError):
            x.insert(0,2)
        with self.assertRaises(StructureInvalidError):
            x.insert(0,["a","b"])
        with self.assertRaises(StructureInvalidError):
            x.insert(0,[[1,2]])
        with self.assertRaises(StructureInvalidError):
            x.insert(0,[1,2,3])
            
        x.insert(0,[1,2])
        
    def test_list_method_sub(self):
        x = StructureStrictList([1,2],[3,4])
        self.assertEqual([1,2],x.pop(0))
        self.assertEqual([[3,4]],x)
        self.assertTrue(x.check_same_structure_with([[3,4]], include_outer_length=True))
        
        
        x = StructureStrictList([1,2],[3,4])
        x.remove([3,4])
        self.assertEqual([[1,2]],x)
        self.assertTrue(x.check_same_structure_with([[1,2]], include_outer_length=True))


class TestTSL(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(StructureInvalidError):
            TypeStrictList([1,2],["a","b"])
        with self.assertRaises(StructureInvalidError):
            TypeStrictList("c",["a","b"])
        with self.assertRaises(StructureInvalidError):
            TypeStrictList("1",1)
            
        TypeStrictList([[1,2],[3,4]])
        TypeStrictList([1,2],[3,4,5]) 
        TypeStrictList([[[1,2],[2]],[[3,4],[1,2]]])
        
    def test_structures(self):
        x = TypeStrictList([1,2],[3,4])
        self.assertEqual(x.type_structure, [[int]])
        
    
    def test_check_save_structure_with(self):
        x = TypeStrictList([1,2],[3,4])
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]]))
        self.assertTrue(x.check_same_structure_with([[1],[2,3]]))
        self.assertFalse(x.check_same_structure_with([3,4]))
        self.assertFalse(x.check_same_structure_with([["a","b"],["c","d"]]))
        
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]], 
                                                     include_outer_length=True))
        
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]], 
                                                    include_outer_length=False))
        
        
    
    def test_check_item_structure(self):
        x = TypeStrictList([1,2],[3,4])
        self.assertTrue(x.check_item_structure([5,6]))
        self.assertTrue(x.check_item_structure([7,8,9]))
        self.assertFalse(x.check_item_structure(5))
        self.assertFalse(x.check_item_structure(["a","b"]))
        
    def test_list_method_add(self):
        x = TypeStrictList([1,2],[3,4])
        with self.assertRaises(StructureInvalidError):
            x.append(2)
        with self.assertRaises(StructureInvalidError):
            x.append(["a","b"])
        with self.assertRaises(StructureInvalidError):
            x.append([[1,2]])
        
        x.append([1,2])
        x.append([1,2,3])
        
        with self.assertRaises(StructureInvalidError):
            x.extend([1,2])
        with self.assertRaises(StructureInvalidError):
            x.extend([[1,2],["a", "b"]])

        x.extend([[11,12],[23,34]])
        x.extend([[1,2],[3,4,5]]) 
        
        
        with self.assertRaises(StructureInvalidError):
            x.insert(0,2)
        with self.assertRaises(StructureInvalidError):
            x.insert(0,["a","b"])
        with self.assertRaises(StructureInvalidError):
            x.insert(0,[[1,2]])
            
        x.insert(0,[1,2])
        x.insert(0,[1,2,3])
        
    def test_list_method_sub(self):
        x = TypeStrictList([1,2],[3,4])
        self.assertEqual([1,2],x.pop(0))
        self.assertEqual([[3,4]],x)
        self.assertTrue(x.check_same_structure_with([[3,4]], include_outer_length=True))
        
        
        x = TypeStrictList([1,2],[3,4])
        x.remove([3,4])
        self.assertEqual([[1,2]],x)
        self.assertTrue(x.check_same_structure_with([[1,2]], include_outer_length=True))


class TestLSL(unittest.TestCase):
    def test_constructor(self):
        with self.assertRaises(StructureInvalidError):
            LengthStrictList([1,2],[3,4,5])  
        with self.assertRaises(StructureInvalidError):
            LengthStrictList([[[1,2],[2]],[[3,4],[1,2]]])    
        with self.assertRaises(StructureInvalidError):
            LengthStrictList("c",["a","b"])
            
        LengthStrictList([[1,2],[3,4]])
        LengthStrictList([1,2],["a","b"])
        LengthStrictList("1",1)
        
        
    def test_structures(self):
        x = LengthStrictList([1,2],[3,4])
        self.assertEqual(x.length_structure, {2:{2:None}})
        
    
    def test_check_save_structure_with(self):
        x = LengthStrictList([1,2],[3,4])
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]]))
        self.assertFalse(x.check_same_structure_with([[1],[2,3]]))
        self.assertFalse(x.check_same_structure_with([3,4]))
        self.assertTrue(x.check_same_structure_with([["a","b"],["c","d"]]))
        
        self.assertFalse(x.check_same_structure_with([[5,6],[7,8],[9,10]], 
                                                      include_outer_length=True))
        
        self.assertTrue(x.check_same_structure_with([[5,6],[7,8],[9,10]], 
                                                    include_outer_length=False))
        
        
    def test_check_item_structure(self):
        x = LengthStrictList([1,2],[3,4])
        self.assertTrue(x.check_item_structure([5,6]))
        self.assertFalse(x.check_item_structure([7,8,9]))
        self.assertFalse(x.check_item_structure(5))
        self.assertTrue(x.check_item_structure(["a","b"]))
        
    def test_list_method_add(self):
        x = LengthStrictList([1,2],[3,4])
        with self.assertRaises(StructureInvalidError):
            x.append(2)
        with self.assertRaises(StructureInvalidError):
            x.append([1,2,3])
        with self.assertRaises(StructureInvalidError):
            x.append([[1,2]])
        
        x.append([1,2])
        x.append(["a","b"])
        
        with self.assertRaises(StructureInvalidError):
            x.extend([1,2])
        with self.assertRaises(StructureInvalidError):
            x.extend([[1,2],[3,4,5]])

        x.extend([[11,12],[23,34]])
        x.extend([[1,2],["a", "b"]])
        
        with self.assertRaises(StructureInvalidError):
            x.insert(0,2)
        with self.assertRaises(StructureInvalidError):
            x.insert(0,[1,2,3])
        with self.assertRaises(StructureInvalidError):
            x.insert(0,[[1,2]])
            
        x.insert(0,[1,2])
        x.insert(0,["a","b"])
        
    def test_list_method_sub(self):
        x = LengthStrictList([1,2],[3,4])
        self.assertEqual([1,2],x.pop(0))
        self.assertEqual([[3,4]],x)
        self.assertTrue(x.check_same_structure_with([[3,4]], include_outer_length=True))
        
        
        x = LengthStrictList([1,2],[3,4])
        x.remove([3,4])
        self.assertEqual([[1,2]],x)
        self.assertTrue(x.check_same_structure_with([[1,2]], include_outer_length=True))


def flatten(_list):
    def flatten_gen(_list):
        for item in _list:
            if isinstance(item, list):
                yield from flatten_gen(item)
            else:
                yield item
    return list(flatten_gen(_list))


class A_false:
    SL = StructureStrictList
    def __init__(self, list_like):
        self._inner_list = A_false.SL.from_list(list_like)
        self.make_sum()
        self._inner_list.hook_func.add(self.make_sum)

    def make_sum(self):
        self.sum = reduce(lambda x,y:x+y, flatten(self._inner_list))

    inner_list = strict_list_property("_inner_list", include_outer_length=False)


class A_true:
    SL = StructureStrictList
    def __init__(self, list_like):
        self._inner_list = A_true.SL.from_list(list_like)
        self.make_sum()
        self._inner_list.hook_func.add(self.make_sum)

    def make_sum(self):
        self.sum = reduce(lambda x,y:x+y, flatten(self._inner_list))

    inner_list = strict_list_property("_inner_list", include_outer_length=True)


class B:
    SL = StructureStrictList
    include_outer_length = False
    def __init__(self, list_like):
        self._inner_list = B.SL.from_list(list_like)
        self.make_sum()
        self._inner_list.hook_func.add(self.make_sum)

    def make_sum(self):
        self.sum = reduce(lambda x,y:x+y, flatten(self._inner_list))

    @property
    def inner_list(self):
        return self._inner_list
    
    @inner_list.setter
    def inner_list(self, list_like):
        if not self._inner_list.check_same_structure_with(list_like,
                                                          B.include_outer_length
                                                         ):
            raise StructureInvalidError("This list is invalid")
            
        pre_hook_fnnc = self._inner_list.hook_func
        self._inner_list = B.SL.from_list(list_like)
        pre_hook_fnnc()  # hook_funcの実行
        self._inner_list.hook_func = pre_hook_fnnc


class C_false:
    SL = StructureStrictList
    inner_list = StructureListValidator(include_outer_length=False)
    def __init__(self, list_like):
        self._inner_list = C_false.SL.from_list(list_like)
        self.inner_list = self._inner_list
        self.make_sum()
        self._inner_list.hook_func.add(self.make_sum)
        
    def make_sum(self):
        self.sum = reduce(lambda x,y:x+y, flatten(self._inner_list))


class C_true:
    SL = StructureStrictList
    inner_list = StructureListValidator(include_outer_length=True)
    def __init__(self, list_like):
        self._inner_list = C_true.SL.from_list(list_like)
        self.inner_list = self._inner_list
        self.make_sum()
        self._inner_list.hook_func.add(self.make_sum)
        
    def make_sum(self):
        self.sum = reduce(lambda x,y:x+y, flatten(self._inner_list))


class TestProperty(unittest.TestCase):
    def test_ssl_property(self):   
        # A
        # include_outer_length = False
        a = A_false([1,2,3,4])
        with self.assertRaises(StructureInvalidError):
            a.inner_list.append([2])
        with self.assertRaises(StructureInvalidError):
            a.inner_list = [[5,6],[7,8]]
        
        a.inner_list.append(5)
        self.assertEqual(a.sum, 15)
        a.inner_list = [3,4]
        self.assertEqual(a.sum, 7)
        a.inner_list = [5,6,7,8]
        self.assertEqual(a.sum, 26)
        
        # include_outer_length = True
        a = A_true([1,2,3,4])
        
        with self.assertRaises(StructureInvalidError):
            a.inner_list.append([2])
            
        with self.assertRaises(StructureInvalidError):
            a.inner_list = [[5,6],[7,8]]
            
        with self.assertRaises(StructureInvalidError):
            a.inner_list = [3,4]

        a.inner_list = [5,6,7,8]
        self.assertEqual(a.sum, 26)
        
        # B
        B.include_outer_length = False
        b = B([1,2,3,4])
        with self.assertRaises(StructureInvalidError):
            b.inner_list.append([2])
            
        with self.assertRaises(StructureInvalidError):
            b.inner_list = [[5,6],[7,8]]
        
        b.inner_list.append(5)
        self.assertEqual(b.sum, 15)
        b.inner_list = [3,4]
        self.assertEqual(b.sum, 7)
        b.inner_list = [5,6,7,8]
        self.assertEqual(b.sum, 26)
        
        B.include_outer_length = True
        b = B([1,2,3,4])
        
        with self.assertRaises(StructureInvalidError):
            b.inner_list.append([2])
            
        with self.assertRaises(StructureInvalidError):
            b.inner_list = [[5,6],[7,8]]
            
        with self.assertRaises(StructureInvalidError):
            b.inner_list = [3,4]

        b.inner_list = [5,6,7,8]
        self.assertEqual(b.sum, 26)
        
    def test_ssl_discriptor(self):
        # C
        # include_outer_length = False
        c = C_false([1,2,3,4])
        with self.assertRaises(StructureInvalidError):
            c.inner_list.append([2])
            
        with self.assertRaises(StructureInvalidError):
            c.inner_list = [[5,6],[7,8]]
        
        c.inner_list.append(5)
        self.assertEqual(c.sum, 15)
        c.inner_list = [3,4]
        self.assertEqual(c.sum, 7)
        c.inner_list = [5,6,7,8]
        self.assertEqual(c.sum, 26)
        
        # include_outer_length = True
        c = C_true([1,2,3,4])
        
        with self.assertRaises(StructureInvalidError):
            c.inner_list.append([2])
            
        with self.assertRaises(StructureInvalidError):
            c.inner_list = [[5,6],[7,8]]
            
        with self.assertRaises(StructureInvalidError):
            c.inner_list = [3,4]

        c.inner_list = [5,6,7,8]
        self.assertEqual(c.sum, 26)



if __name__ == "__main__":
    unittest.main()