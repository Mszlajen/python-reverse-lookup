import unittest
from reverse_lookup import ReverseLookup, Inner

class ReverseLookUpTest(unittest.TestCase):
    def test_A_to_B_use_A(self):
        class A(ReverseLookup):
            def m(self):
                return 'A'
        
        class B(A):
            def m(self):
                return 'B'
        
        self.assertEqual(B().m(), 'A')
    
    def test_A_to_B_uses_inner(self):
        class A(ReverseLookup):
            def m(self):
                return 'A' + Inner(self, A).m()
                
        class B(A):
            def m(self):
                return 'B'
        
        self.assertEqual(B().m(), 'AB')
    
    def test_A_uses_inner_without_implementation(self):
        class A(ReverseLookup):
            def m(self):
                return 'A' + Inner(self, A).m()
        
        with self.assertRaises(AttributeError):
            A().m()
    
    @unittest.skip("May not implement")
    def test_B_uses_reversed_when_accessing_from_class(self):
        class A(ReverseLookup):
            def m(self):
                return 'A'
        
        class B(A):
            def m(self):
                return 'B'
        
        self.assertEqual(B.m(B()), 'A')
    
    def test_B_has_a_reversed_mro(self):
        class A(ReverseLookup):
            ...
        
        class B(A):
            ...
        
        self.assertListEqual(B.mro(), [object, ReverseLookup, A, B])
    
    def test_A_uses_its_own_to_string(self):
        class A(ReverseLookup):
            def __str__(self):
                return 'A'
        
        self.assertEqual(str(A()), 'A')