# {{ name }}
{% if __project_description__ %}
{{ __project_description__ }}
{% endif %}

This is a template for a renku data science project using python. It has predifined folders and a installed tool for documentation.
Both are further explained in the sections below.

### Project Setup
Before using the template you should do the following
    [] change the folder name of the folder "name" to the name of your project
    [] edit the setup.py file by replacing "name" with your projects name

Doing both will enable installing you project with `pip install -e .`. 
This will let you import your python code within the src folder but also from other directories.

Imports can then be of the form.
```python
from projectname.data.Dataloader import Dataloader
```


### Workflow File and Renku
One of the most important ideas behind Renku is the concept of capturing the provenance of the analysis process. 
For that renku provides workflows. In short a renku workflow is an execution of your code where you explicitly define inputs and ouputs. 
This way renku can keep track of the dependencies. 

A workflow is best defined in a workflow file. An example is given in this template. 
The workflow can be executed with `renku run workflow.yml`
An overview of the dependencies can be displayed with `renku workflow visualize -i`


### Documentation
how to use sphinx


### Folder Structure
```
├───.renku                  <- renku internal folder 
├───data                        
│   ├───external            <- data from third party sources
│   ├───processed           <- the final data sets for modeling
│   └───raw                 <- the original immutable data dump
│ 
├───docs                    <- a default Sphinx project; see sphinx-doc.org for details
│   └───source
│ 
├───models                  <- trained and serialized models
│ 
├───notebooks               <- jupyter notebooks
│ 
├───references              <- data dictonaries, manuals, and other explanatory materials
│ 
├───reports                 <- generated analysis
│   └───figures
│ 
├───setup.py                <- make this project pip installable with `pip install -e`          
│ 
├───src                     <- source code for use in this project
│   ├───data                <- scripts to download and generate data
│   ├───features            <- scripts to turn raw data into features for modeling
│   ├───model               <- scripts to train models and use them for predictions
│   └───visualization       <- scripts to create exploratory and results oriented visualizations
│ 
├───tests                   <- unit tests for pytest
│ 
└───workflow.yml            <- renku workflow file
```