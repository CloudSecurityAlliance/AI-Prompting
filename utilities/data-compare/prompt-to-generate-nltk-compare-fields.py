I have a CSV file with a list of items, each item has an id (CSA_ID) and a name (NAME_OF_ITEM), a possible alternate name (ALSO_KNOWN_AS) and a description (DESCRIPTION). I want you to write a python script that  will compare each NAME_OF_ITEM to each other NAME_OF_ITEM, ALSO_KNOWN_AS and DESCRIPTION, and group similar ones together based on matches between the NAME_OF_ITEM and the other fields in other records. First lets decide on a strategy to compare these together,  can I suggest we start by trying to extract keywords first and fine entries with the same keywords?

Can you make the input file a command line argument? Also can you make sure the script handles entries that don't have a ALSO_KNOWN_AS or a DESCRIPTION. also can you print the output to a file specified by a command line argument?

Can you fix this: The 'sklearn' PyPI package is deprecated, use 'scikit-learn'
      rather than 'sklearn' 

Resource stopwords not found.
  Please use the NLTK Downloader to obtain the resource:

  >>> import nltk
  >>> nltk.download('stopwords')


ok let's change the output to print a list of all the CSA-AI-WVA-XXXXXX ID's that are related in each cluster, one cluster per line in the file

  File "/mnt/c/Users/kurt/Downloads/merge/./process.py", line 49, in <module>
    clustering = AgglomerativeClustering(affinity='precomputed', linkage='complete', distance_threshold=0, n_clusters=None)
TypeError: AgglomerativeClustering.__init__() got an unexpected keyword argument 'affinity'

can you now update the script to take a command line argument called "input-fields"  of the fields in the CSV file to compare, and a command line argument called "id-field" to take the ID field to print out in the output 

can you also make your_input_file.csv your_output_file.csv arguments called "input-file" and "output-file"
