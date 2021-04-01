import unittest

from py_strict_list import StructureStrictList, TypeStrictList, LengthStrictList
from py_strict_list import StructureInvalidError


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

if __name__ == "__main__":
    unittest.main()