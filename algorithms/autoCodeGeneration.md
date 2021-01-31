## Workflow to create automatic code

* check if the user has left the code field as blank, auto-generate code only if user input is null
* Using a db cursor get the latest issued code
* After spliting the code by '/' character, if the code does not end with a valid positive integer, 
throw an error and inform user that code needs to created manually this time 
* Add +1 to the latest code and return this value for further operations
* Within the db cursor transaction, create a new code with the auto generated code