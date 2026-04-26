## how to run it
- press green run button in github
- download as zip
- extract zip folder
- use vscode and run and debug option for either the console, web or desktop version of the ide
- else run it from terminal using python

- if error that python isn't there or unable to run it, go to python.org and install latest version
- if using terminal to run
- run vm_ide.py for the desktop ide
- run vm_web.py for the web ide that opens in localhost
- run src/vmexecuter.py for the terminal version

## how it works
- in the src folder, there is the ByteCode.txt that has an examples of syntax
- there is also ByteCodeReader.py which contains a couple of methods to read the text file and output it along with other methods.
- one method reads the file line by line and returns the commands in a array
- the second method finds where they are and outputs tuples
- the last method is used for converting various forms of true and false for use in the logical expression instruction set
- vmexecuter.py is the actual logic of the entire PythonAssembly, it contains all commands in the class called Commands and that is used in another class called Vmexecuter
- it first checks if its running in the web or on desktop by trying to detect pyodide support which is only on the web.
- it uses a collection for output or direct print based on what version it is, collection for the web version and direct print as executed in the desktop version

## why it was made
- it was 

