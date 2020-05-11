# COVID-19 Dashboard for India

A web application for data visualization and analysis of the current COVID-19 pandemic in India. Provides state-wise analysis of the data using a time-dependant  _Susceptible, Infected and Recovered model_.

[Source Code in Github](https://github.com/Aniruddha-S-Prasad/COVID19-Dashboard-India)

---

## Web Application

This application is written in Python and is based on the [Dash framework](https://dash.plotly.com/introduction), and uses [Bootstrap](https://getbootstrap.com/) for implementing a responsive layout.

The required modules and frameworks for running and deploying this application is available in the `requirements.txt` file and can be installed in a machine running python(3+) by executing 

```bash
pip install -r requirements.txt
```

in the project's root folder.

The web server can then be started on the local machine by executing

```bash
python application.py
```

which launches development flask server on the __localhost__ port __8080__ and can be accessed through going to the addresses `127.0.0.1:8080` or `0.0.0.0:8080`  in a web browser.

Currently, an instance of this web application is running at [COVID-19 Dashboard](http://covid19-stats-india.herokuapp.com/), which is deployed using [Heroku](https://www.heroku.com)

---

## Analysis

The file `tracker.py` queries the [API](https://api.covid19india.org/) to get state-wise data on the cases identified, recovered and deceased on a certain date and stores it in a JSON database file. From this data, the date wise total, active and recovered cases can be obtained. These are then analyzed according to a time-dependent  _Susceptible, Infected and Recovered model_ given by Yi-Cheng Chen et al. in their paper [A Time-dependent SIR model for COVID-19 with Undetectable Infected Persons](http://gibbs1.ee.nthu.edu.tw/A_TIME_DEPENDENT_SIR_MODEL_FOR_COVID_19.PDF) 

This model yields three parameters that govern the progression of the disease through the population, which are __Beta__, __Gamma__, and the ratio of the two which is the __Reproductive Number__.
* __Beta__ is the probability of transmission of the infection from an active case to a person in the _Suceptible_ population. In the case where the disease progression is being halted by measures taken, such as lockdown, social distancing, and patient isolation, __Beta__ reduces.
* __Gamma__ is the probability of recovery from the infection, i.e. on a given date with "_n_" number of active cases, "_n*Gamma_" will be the number of recovered people. An increase in __Gamma__ over time denotes that the treatments being received by infected patients are being effective.
* __Reproductive Number__ is the ratio of __Beta__ to __Gamma__ and according to the model, this parameter denotes the number of new cases an infected person generates before recovering. The disease can be said to be under control when the __Reproductive Number__ reduces below zero, which denotes that the peak of active cases has been reached, and the number of active cases will reduce with time. 

The model implementation is an analysis model and not a predictive model, and these parameters alone cannot provide complete information on the future progression of the disease. (Please see the case of the state "Tamil Nadu", which is currently undergoing a second wave of infections). The data provided in the dashboard after analysis can be useful for gauging the effectiveness of the measures taken by the people and can guide decision making for the future. 

---

## Project Structure

This project tries to follow the __Model-View-Controller__ design pattern. The structure of the project is as follows,

* __Model__: The data model is implemented in the `tracker.py` file, which takes care of loading the data from a web API, analyzing the same and outputs the data in the form of a _**DataContainer**_ object implemented in `data_container.py`.
    * The data is loaded using several helper files such as `json_database_builder.py`, `patient_sql_database_builder.py`, `recovered_handler.py` and `deceased_handler.py`. 
    * All of the data is stored in the `databases` folder and the file `database_handler.py` provides an interface for accessing this data. __Update__: As the API changed during the development of this project, the `database_handler.py` no longer provides for complete handling of the database interface, hence additional features had to be implemented in the `tracker.py` file to handle the new format.
* __View__: The application view is implemented in the `app_view.py` file using the Dash framework which mimics HTML.
* __Controller__: `application.py` is the main controller of the web application. It sets up the Dash(Flask) web server, and implements functions relating to loading the __View__ and data from the __Model__ and controlling the web interface by using Dash callbacks 

---

#### Data Sources

The data for this project is provided by the [COVID-19 India](https://www.covid19india.org/) project, using their [API](https://api.covid19india.org/). This provides granular data on the patients in India and can be filtered easily.


