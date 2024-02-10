I have a CSV file with a list of items, each item has an id (CSA_ID) and a name (NAME_OF_ITEM), a possible alternate name (ALSO_KNOWN_AS) and a description (DESCRIPTION). I want you to write a python script that  will compare each NAME_OF_ITEM to each other NAME_OF_ITEM, ALSO_KNOWN_AS and DESCRIPTION, and group similar ones together based on matches between the NAME_OF_ITEM and the other fields in other records. First lets decide on a strategy to compare these together,  can I suggest we start by trying to extract keywords first and fine entries with the same keywords?

Can you make the input file a command line argument? Also can you make sure the script handles entries that don't have a ALSO_KNOWN_AS or a DESCRIPTION. also can you print the output to a file specified by a command line argument?

Traceback (most recent call last):
  File "/mnt/c/Users/kurt/Downloads/merge/./gemini.py", line 24, in <module>
    data["name_keywords"] = data["NAME_OF_ITEM"].apply(tokenize)
  File "/home/kurt/.local/lib/python3.10/site-packages/pandas/core/series.py", line 4760, in apply
    ).apply()
  File "/home/kurt/.local/lib/python3.10/site-packages/pandas/core/apply.py", line 1207, in apply
    return self.apply_standard()
  File "/home/kurt/.local/lib/python3.10/site-packages/pandas/core/apply.py", line 1287, in apply_standard
    mapped = obj._map_values(
  File "/home/kurt/.local/lib/python3.10/site-packages/pandas/core/base.py", line 921, in _map_values
    return algorithms.map_array(arr, mapper, na_action=na_action, convert=convert)
  File "/home/kurt/.local/lib/python3.10/site-packages/pandas/core/algorithms.py", line 1814, in map_array
    return lib.map_infer(values, mapper, convert=convert)
  File "lib.pyx", line 2920, in pandas._libs.lib.map_infer
  File "/mnt/c/Users/kurt/Downloads/merge/./gemini.py", line 19, in tokenize
    tokens = word_tokenize(text.lower())
AttributeError: 'float' object has no attribute 'lower'

can you print out the entire script in a way that fixes this?
