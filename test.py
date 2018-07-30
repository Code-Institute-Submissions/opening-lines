import unittest
import run

class TestRun(unittest.TestCase):
    
    def test_can_generate_random_sequence(self):
        random_sequence = run.get_random_sequence([{"excerpt": "Excerpt 1"},{"excerpt": "Excerpt 2"},{"excerpt": "Excerpt 3"}])
        self.assertIn(random_sequence,[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]])
        
    def test_can_generate_random_question(self):
        question = run.get_question([{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"},{"excerpt": "Excerpt 2", "book": "Book 2", "author": "Author 2"},{"excerpt": "Excerpt 3", "book": "Book 3", "author": "Author 3"}],2,[1, 2, 0])
        self.assertEqual(question,{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"})
        question = run.get_question([{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"},{"excerpt": "Excerpt 2", "book": "Book 2", "author": "Author 2"},{"excerpt": "Excerpt 3", "book": "Book 3", "author": "Author 3"}],1,[0, 2, 1])
        self.assertEqual(question,{"excerpt": "Excerpt 3", "book": "Book 3", "author": "Author 3"})
           
    
    def test_can_check_answer(self):
        correct_or_not = run.check_answer("Book 1",{"excerpt": "Excerpt 1", "book": "Book 1", "author": "Author 1"} )
        self.assertEqual(correct_or_not,True)
        correct_or_not = run.check_answer("Book 2",{"excerpt": "Excerpt 2", "book": "Book 2", "author": "Author 2"} )
        self.assertEqual(correct_or_not,True)
    
        
    def test_can_get_current_player(self):
        current_player = run.get_current_player(["Rod"], 0)
        self.assertEqual(current_player, "Rod")
        current_player = run.get_current_player(["Rod","Jane"], 0)
        self.assertEqual(current_player, "Rod")
        current_player = run.get_current_player(["Rod","Jane","Freddy"], 1)
        self.assertEqual(current_player, "Jane")
        current_player = run.get_current_player(["Rod","Jane","Freddy"], 5)
        self.assertEqual(current_player, "Freddy")
        
    def test_can_amend_scores(self):
        list_of_scores = run.amend_scores(["Rod", "Jane", "Freddy"], ["0","0","0"], "Jane")
        self.assertEqual(list_of_scores, ["0","1","0"])
        list_of_scores = run.amend_scores(["Rod", "Jane", "Freddy", "Bungle"], ["0","3","5","2"], "Bungle")
        self.assertEqual(list_of_scores, ["0","3","5","3"])
        
      
      