# Numworks-workshop.py

This project is a python wrapper for the numworks [workshop](workshop.numworks.com/).

## How to install ?

Just install the pypi package :

## How to use ? 

```py
from numWorkshop import Script, Workshop
 
workshop = Workshop("email", "password")

toaster = Script(name="name", description="description", content="print('hello-world')", public=True)
workshop.createScript(toaster)
toaster.content = "print('nsi.xyz')"
# since we use the script name to get acess and edit your script, your should use the name parameter 
# of the editScript function, this will update the script at the end of the process and not break script
# Other parameter are updated throught Script object...
workshop.editScript(toaster, name="namev2")
workshop.deleteScript(toaster)

script = workshop.getScript(https://workshop.numworks.com/python/thierry-barry/annuite_constante) # this return a script object
print(script)
```

If you find a bug or want a new feature you can open an issue.

