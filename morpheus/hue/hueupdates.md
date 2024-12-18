The hub sends updates as a list that has one are more dicts depending on  
how fast the data is sent.  Each dict has four keys:  
### creationtime
### data  
A list of dicts, not sure if ever more than one. Keys specific to the reporting device.  
All have 'type' key that indicates what type of update is being sent 
### id - of reporting device
### type - ‘update’, ‘add’, ‘delete’, ‘error’