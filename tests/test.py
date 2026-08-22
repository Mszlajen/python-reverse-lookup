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