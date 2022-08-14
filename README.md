# CP2KAtomicSimProcessor
Python code package for automatically processing and analysing CP2K atomic simulations results

### Required Python Library dependencies [subject to change]
- ASE
- Pandas
- qt4 [only qt4 is compatible with mayavi and pyface - needed for wavefunction analysis]
- qt5 or qt6
- PySide6
- mayavi
- pyface

#### Using mayavi and pyface with PySide6
In order for CP2KAtomicSimProcessor to be able to process and analyse Gaussian Cube wavefunction files, mayavi and pyface need to be compatible with PySide6. At current, pip installed pyface does not include an option to create a QVTKRenderWindow with PySide6, however, the pip installed *QVTKRenderWindowInteractor.py* file can be altered to work using PySide6. The *QVTKRenderWindowInteractor.py* file included in this git repository has already been altered to work with pyside6, all the user needs to do is replace their pip installed *QVTKRenderWindowInteractor.py* with this file [there is no github page for pyface or mayavi to submit a git pull request to change *QVTKRenderWindowInteractor.py* at source].

In order to replace the pip installed *QVTKRenderWindowInteractor.py*, the user will first need to find the file on their local machine. This can be done via:
1. Enter your git cloned CP2KAtomicSimProcessor directory.
2. Find your local machine's python site-packages directory using <img src="/Users/appleair/Desktop/Screenshot 2022-08-13 at 09.40.13.png" height="25">. 
3. Take the file path which ends in the installed python version [e.g. <img src= "/Users/appleair/Desktop/Screenshot 2022-08-13 at 09.47.43.png" height="25">] and input this path into the appropriate find command based on your OS system.
    
    For MacOS use:

    <img src= "/Users/appleair/Desktop/Screenshot 2022-08-13 at 09.59.38.png" height=25>

    For Windows use:

   <img src="/Users/appleair/Desktop/Screenshot 2022-08-13 at 10.03.00.png" height="25">
4. Take the filepath to QVTKRenderWindowInteractor.py returned by this command and then run a simple copy command to replace the pip installed QVTKRenderWindowInteractor.py with the QVTKRenderWindowInteractor.py file in the CP2KAtomicSimProcessor depository, 

   e.g. <img src = "/Users/appleair/Desktop/Screenshot 2022-08-13 at 10.12.34.png" height="25">



### How to use CP2KAtomicSimProcessor
CP2KAtomicSimProcessor is an atomic simulation data processing and analysis tool specifically for CP2K data that is designed to be run from command-line. The full CP2KAtomicSimProcessor depository must be downloaded onto the users local machine to avoid missing file errors. The user must be within the CP2KAtomicSimProcessor root directory when they run the *MAIN.py* file with python3. 

Before the user runs the tool for the first time, they must change the ***os.chdir*** command within the *MAIN.py* file to the path of their local CP2K calculation data storage directory. 

![Screenshot 2022-08-05 at 15 07 10](https://user-images.githubusercontent.com/92368623/183094131-a96d139b-1203-48a8-9801-05464f5ed349.png)

The directory specified by the path inputted into the ***os.chdir*** command will act as the suedo current working directory while the tool runs. This directory must be the immediate parent directory to at least one subdirectory set. A subdirectory set must consist of: 
1) a defect-free subdirectory, containing CP2K data related to a material's defect-free atomic structure.
2) a defect subdirectory, acting as the parent directory for all directories containing CP2K data related to defect simulation within a material.
3) a chemical potentials subdirectory, containing CP2K data produced for deriving all atomic kind chemical potentials within a material's defect-free and defect-containing structures. 

The optimal file structure within the calculation parent directory for compatibility with CP2KAtomicSimProcessor would be as depicted.

<img src="https://user-images.githubusercontent.com/92368623/183087889-a920d997-ffc2-47b7-ad83-7e5c42699d4b.png" width="700" height="500">

This is because there must be, at least, four arguments which follow *MAIN.py* within the python3 command. The first argumemnt must be the name of the material's defect-free subdirectory, while the second is the name of the defect subdirectory and the third is the name of the chemical potential subdirectory. The fourth argument can then be choosen from the following list based on user preference
- all : causes data to be processed from all defect calculation directories within the defect subdir 
- only : allows data to be processed from specific calculation irectories whose names contain the string(s) stated in the command after the 4th argument
- except : allows data to be processed from all defect directories except for those who have names that contain the string(s) stated in the command after the 4th argument

![Screenshot 2022-08-05 at 15 00 36](https://user-images.githubusercontent.com/92368623/183092909-cdbdedfa-50ff-4197-9fb1-739371801ad9.png)


It is recomended that a new set of subdirectories is created for every material studied via CP2K so that data mixing between multiple different materials is avoided during the tool's processing stage. The except/only arguments are only applied by the tool when looking for directories within the named defect subdirectory, so cannot be used to distinguish between two different materials that are held within the same defect-free subdirectory.  

### CP2KAtomicSimProcessor's user questionnaire
When CP2kAtomicSimProcessor is run, the user is asked a series of questions to allow the tool to determine the user's processing and analytical wants. 

The first main question asked allows the user to input the types of results they would like the tool to process. One or more results options from the options stated can be inputted by the user as an answer. Depending on which result options are inputted, the user may be asked follow-up questions to help the tool process the specific results. 

![Screenshot 2022-08-05 at 15 26 27](https://user-images.githubusercontent.com/92368623/183097869-92ddbebf-ec1d-45fb-bee8-74100c764b93.png)

The user will then be asked to type either '*y*' pr '*n*' depending on whether they would like the tool to perform data analysis. If the user is looking to obtain purely processed data results for use in other analytical methods not yet implemented within CP2KAtomicSimProcessor or to collate the progression of results, choosing '*n*' will allow generate a csv file names processed_data.csv within the user's specified root directory. The user will then be asked the follow up question of whether they would like to append or overwrite the processed_data.csv file if the file currently already exists. By default the file illbe appended to for collation of results progression, however typing '*overwrite*' will cause the existing processed_data.csv file to be deleted and a new processed_data.csv to be created. 

![Screenshot 2022-08-05 at 15 47 42](https://user-images.githubusercontent.com/92368623/183101904-86e1a296-0f27-4134-8562-4d44565b342b.png)

If the user instead chooses '*y*' to question two, they will then be asked if they would like to create a graphic user interface to display their analysed results. 

![Screenshot 2022-08-05 at 15 58 14](https://user-images.githubusercontent.com/92368623/183104248-b3d13fd2-8e93-4576-811d-0fcff785bd00.png)

Choosing '*n*' for this question will produce png files for each result option whose data is normally ploted in a figure and csv files for reuslts options whose data is best displayed in a dataframe. These png and csv files will then be saved to the corresponding source defect calculation directory of the data displayed within them. 

Choosing '*y*' will produce a graphic user interface with a similar layout to that shown below.
![Screenshot 2022-08-05 at 16 42 53](https://user-images.githubusercontent.com/92368623/183112882-ff1cda6e-d19b-46eb-8058-86285b953f00.png)

