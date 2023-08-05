# <h1> pyqccapi<sub><sub><sup>is a simple component for human to use qcc(企查查) api .</sup></sub></sub></h1><br>

### Installation

First of all we have to install it:
```Shell
pip install pyqccapi
```
I recommend using the parameter ``-i https://pypi.douban.com/simple`` via the the installation above in person.

### Sample  

Create a config.yaml :
```Shell
appkey:
    <your-appkey-here>
seckey:
    <your-seckey-here>
```

```Python
# Prepare parameters
params = {
    'keyword': '长风',
    'provinceCode': 'SH'
}

# initialize a task
task = Task('8d23ff9d-a8ee-4c32-99d3-2129f101617b', params)
# initialize a ApiInvoker
invoker = ApiInvoker('config.yaml')
result = invoker.invoke(task)
print(result)
