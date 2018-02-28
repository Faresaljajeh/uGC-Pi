import os

# Check where program is running
try:
    machine_name = os.uname()[1]
except AttributeError:
    print('Not running on correct machine!')
    pi = False
else:
    if machine_name == 'ugcpi':
        print('Running on correct machine!')
        pi = True
    else:
        print('Not running on correct machine!')
        pi = False
        

    
    
    
    