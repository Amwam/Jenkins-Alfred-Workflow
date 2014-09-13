Jenkins-Alfred-Workflow ![travis ci](https://travis-ci.org/Amwam/Jenkins-Alfred-Workflow.svg?branch=master)
=======================

An Alfred workflow to lookup jobs on a Jenkins server


### Usage
- Firstly set the url of the Jenkins server using `jenkins_url`
- Use `jenkins` to show a list of jobs, which can be filtered further using a query
- Use `fail` or `jenkinsfail` to show a list of jobs that are currently failing, this can be fitlered further
- Use `building` to show a list of jobs that are currently building, this can be fitlered further


### Building
There are a few requirements related to testing needed. I'd recommend creating a `virtualenv` and using `pip` to install the requirements from `requirements.txt`

Running `paver` will run all the unit tests, and show the coverage reports for the workflow


### Installing
Added this directory to the Alfred workflows directory will install the workflow
