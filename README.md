Adding venv: 
    Command : python -m venv <nameOfVirtualEnv>
    Select Interpreter : ctrl + shift + p -> Select Interpreter -> Enter Interpreter Path -> paste the path of venv\Scripts\python.exe
    Terminal : venv\Scripts\activate

Earlier to start server in fastApi we had something like 
    "uvicorn main:app --reload" command
    
    but now we can use : "fastapi dev" command to run server it will give links for documentation and server