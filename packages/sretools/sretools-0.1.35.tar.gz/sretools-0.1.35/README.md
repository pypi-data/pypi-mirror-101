# sretools

A collection of SRE command line tools

1. sretools-incident    mini operation pastebin note.
2. sretools-nonascii    scan FS, files for non-ascii characters.  will help resovle issues caused by "invisiable" characters.
3. [sretools-table-format](https://github.com/laowangv5/sretools/blob/main/examples/sretools-table-format.md)  console table formatting tool.  pipe, CSV, etc. support UNICODE.
4. sretools-ssh        ssh command tool with expect integration.  run remote command, ship and run package on remote server, etc.
5. sretools-expect    command line expect tool.   help SRE to "expect' interactive applications in a very easy way.
6. sretools-json2html   format JSON from file or pipe to HTML tables.
7. sretools-json2yaml   format JSON from file or pipe 
8. sretools-yaml2json   format YAML from file or pipe 
9. sretools-yaml2html   format YAML from file or pipe 
10. [sretools-dbx](https://github.com/laowangv5/sretools/blob/main/examples/sretools-dbx.md)        generic JDBC calls. dump query in good table format.  open JDBC access to bash level.

Classes :

1. LE   expect class for develp sretools-ltexpect alike tools.
2. SimpleTable    console formatting table supporting wide chacaters.
3. JsonConverter  convert JSON str or dict/list object to HTML or YAML.
