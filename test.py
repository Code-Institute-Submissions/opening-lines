import unittest
import run

class TestRun(unittest.TestCase):
    
  def test_can_check_answer(self):
        correct_or_not = run.check_answer("Book 1",[{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"},{"excerpt": "Excerpt 2", "book": "Book 2", "author": "Author 2"}],0 )
        self.assertEqual(correct_or_not,True)
        correct_or_not = run.check_answer("Book 2",[{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"},{"excerpt": "Excerpt 2", "book": "Book 2", "author": "Author 2"}],1 )
        self.assertEqual(correct_or_not,True)
        correct_or_not = run.check_answer("book 2",[{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"},{"excerpt": "Excerpt 2", "book": "Book 2", "author": "Author 2"}],1 )
        self.assertEqual(correct_or_not,True)
      
      