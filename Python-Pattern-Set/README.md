No guarantees/warranties.
This all assumes that the customer has installed and set up NITRO properly in their python environment.   This was done using python 2.7.13.

Deleting a pattern set:
Command line looks like
python del-patset.py <nsip> <userid> <password> <pattern-set-to-delete>
Run the command, and the pattern set and all its strings are as good as gone.
The script does NOT save the running configuration, but there is code in there – commented out.

Adding a pattern set:
Command looks like
python add-patset.py <nsip> <userid> <password> <file-containing-pattern-sets-to-add>
I’ve also included a sample pattern set file to enable addition of one or more.  Note that it is in JSON format (makes it easier to add this way). The opening tag in the file that says “patsets” MUST be there. It MUST. MUST. ☺

Don't mess with format of the file, otherwise it will not load properly.  The thing to watch for are the commas at the ends of each line.   The last pattern in a pattern set should NOT have a comma – all the previous ones do. This JSON parser here can help verify:  
http://json.parser.online.fr/

Otherwise, you should be able to add valid pattern sets and indices in bulk with this, as long as they are valid.

If you try to add a pattern set that is already there, it will leave the existing pattern set in place, however, it will replace any strings/indices that are in place already if there is an overlap.   In other words, if pattern set PAT-SET exists and it has holds patterns (ABC, DEF, GHI), and the customer attempts to add PAT-SET and patterns (ABC, UVW and XYZ), then pattern set PAT-SET will remain, the index number and any other definitions for ABC will be replaced, DEF and GHI will remain unchanged, and UVW and XYZ will be added.

There is no other error checking I did besides that.

The script does NOT save the running configuration, but there is code in there – commented out.