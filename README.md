# Opening Lines

This is a Python 3/Flask-based quiz based on the opening lines of famous novels. It was built as the Practical Python project of my Code Institute Full Stack Developer course.

## Functionality

One to four players can take part - each will get ten random questions. Scores are given as the players go on and there is also a hightest ever score, stored in a text file.

## Design

The site is responsive and mobile first.

## Build status

Complete, though I may expand the JSON file.

## Testing

The site has been tested on different browsers and via responsinator.com

It was built unit test-driven development, using the unittest test suite in test.py 

* test_can_generate_random_sequence - tests function to generate a random sequence. Hard to test randomness but tests that a short random sequence is an array of all the possible random sequences of that length.

* test_can_generate_random_question - tests that the right question is delivered, based on the radom sequence
           
* test_can_check_answer - check that True is returned if the question is the same as the answer, irrespective of case

* test_can_get_current_playern - tests that the current player is known, depending on the number of the turn
        
* test_can_amend_scores - tests that the correct value in a score array increases by 1 if a current player ges the question right

## Deployment


## License information

Open sources, and the opening lines are too short to be copyright.
 
