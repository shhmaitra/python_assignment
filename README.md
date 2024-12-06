# python_assignment
 Python program, that takes a json file (which contains the information of a directory in nested structure) and prints out its content in the console in the style of ls (linux utility)
Command:
* python -m pyls (Defult ls functionality)
* python -m pyls -l (Long listing)
* python -m pyls -A (All files)
* python -m pyls -l -r (Long listing and reverse)
* python -m pyls -l -r -t (long listing and reverse and sorted by time)
* python -m pyls -R (Recursive)
* python -m pyls --help (Help)

Including test : test_pyls.py has been added to test the functionality. To run the test_pyls.py we need to first install pytest module using "pip install pytest"
Command:
* pytest test_pyls.py
