# {{ name }}
{% if __project_description__ %}
{{ __project_description__ }}
{% endif %}

## Project Setup
    - change folder name
    - change setup.py




## Workflow File and Renku



## Documentation
how to use sphinx


## Folder Structure
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
└───tests                   <- unit tests for pytest
```