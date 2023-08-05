# coh-piggs-extrator

A module that allows the extracting of files from a City Of Heroes. The pigg file is used to create "virtual drives" to
load data from during the running of the game.

Basically it is similar to a zip file and therefore can be processed by parsing the files and extracting the information

## Usage
The design of this library is simple in use. The library makes use of a simple implementation of the
[strategy](https://en.wikipedia.org/wiki/Strategy_pattern) pattern to process each of the entries of the pigg file. 

With this in mind there are two objects of interest:
```python
    coh_piggs_extractor.coh_piggs_extractor.PiggFile(pigg_file_path, strategy)
```

This is used to load the pigg file and process the contents to get the metadata and data for each of the contained files.
The constructor takes two parameters (as shown above):
* pigg_file_path: The path to the pigg file
* The strategy implementation used to process each of the file

```
    coh_piggs_extractor.coh_piggs_extractor.PiggFileEntryProcessingStrategy
```
This is a simple no op class that implements the expected strategy interface. It has one function 
```process_pigg_file_entry``` that is called for each of the files in the pigg file. The function takes two parameters 
as follows:
* meta: This is the metadata of the file and is a simple value object DirEntry (defined in 
  [coh_piggs_extractor](src/coh_piggs_extractor/coh_piggs_extractor.py)). The main entry of use is the name field.
* data: This is the binary data that has been extracted for the file.

A simple file extracting strategy has been provided as well
```python
    coh_piggs_extractor.coh_piggs_extractor.SimpleFileOutputEntryProcessingStrategy(out_dir)
```
This will output each of the contained files into the specified ```out_dir``` provided during construction.

