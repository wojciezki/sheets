

# Exam Sheets

Web application that solves the problem of preparing and evaluating exam sheets - recruitment task

## Getting Started


### Prerequisites

To start application you need to have installed Python 3.6.5 and Virtualenv

```
sudo apt-get install virtualenv
```


### Installing

To install application run in command line:

```
make install
```

If you wish to specify path to python run in command line:
```
make install PYTHON_VERSION=path/to/python/version
```

## Running the tests

To run applications tests run in command line:

```
make test
```

## Running apllication
To run application run in command line:
```
make run
```

### API

Registration:
```
/registration/
```

Login:
```
/login/
```

Logout:
```
/logout/
```

Create exam template
```
/exam_sheets/
```
Create task/question:
```
/tasks/
```
Create solution (note: remember, every task needs at least one solution):
```
/solutions/
```
Create answer (note: when answer is create exam instance is made based on exam template):
```
/answers/
```


### Additional API
Exam filtering options:
```
/exam_sheets/?template=True/
/exam_sheets/?creator={id}/

```




