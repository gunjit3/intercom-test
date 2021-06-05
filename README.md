# Intercom Test

### Problem in brief
Given a customer file and a office location, figure out all customers within 100Km of office.

### Approach
Since the requirements were simple enough functional programming approach was taken. 
Each step is written as a function, constants are separated in a different file.
Customers are represented as a python dictionary instead of a class since no methods were needed to interact with customers or manipulate their data.
For testing pytest was used.


### How to run and test
1. Create and source python virtual environment
2. Install requirements.txt, it will install pytest as dependency for running tests

~~~
$ python3 -m venv ./venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ python nearby_customer.py -h  
usage: nearby_customer.py [-h] input_file output_file  
  
positional arguments:  
input_file path to customers file  
output_file path to output file  
  
optional arguments:  
-h, --help show this help message and exit

$ python nearby_customer.py ./customers.txt ./output.txt
~~~

#### How to test

~~~
$ pytest tests.py
~~~
