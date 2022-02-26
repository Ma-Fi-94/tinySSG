# tinySSG
A tiny static site generator / text processor (e.g. for blogging) I am currently writing

Currently, two features are implemented:
  - Include the content of another file:
    ```
    #include filename
    ```
    
  - Define a variable that gets replaced globally, i.e. throughout the whole file including all the lines before the definition:
    ```
    #globaldefine VARNAME "content of the variable"
    ```

# Usage
Three modes of operation are possible:
  - Singe-file mode: 
  ```
  tinySSG.py --file inputfile outputfile
  ```
  
  - Whole-folder mode:
  ```
  tinySSG.py --folder path/to/folder inputextension outputextension
  ```
  
  - Recursive mode (NOT IMPLEMENTED YET, WILL FOLLOW SOON):
  ```
  tinySSG.py --recursive path/to/folder inputextension outputextension
  ```
  

