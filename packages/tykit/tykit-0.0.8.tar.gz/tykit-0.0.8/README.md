<!--
 * @Description: 
 * @version: 
 * @Author: TianyuYuan
 * @Date: 2021-04-02 15:42:10
 * @LastEditors: TianyuYuan
 * @LastEditTime: 2021-04-07 00:16:11
-->
# tykit (Tell You kit) ![version](https://img.shields.io/badge/tykit-v0.0.8-blue.svg) ![rich](https://img.shields.io/badge/Powered-Rich-brightgreen.svg)

![Alt Text](./image/Kapture%202021-04-02%20at%2017.18.06.gif)

## 📜 Description
'tykit--Tell You kit', pronounced like 'ticket', is a toolkit to monitor your scripts' status easily, which haves rich and pretty output for progress bar and console logs.
The tykit may support more decent output in the future

## ⚙️ Install
tykit can be easily installed with `pip` as below
```bash
# for python2
pip install tykit
# for python3
pip3 install tykit
```

## 🌟 Features
---
## 🚀 ProgressBar 进度条
for ***loop,range,multi-threading and multi-threading with multi-params***

> ___pb_range(*args)___

This function is just like the python builtin function `range()`
```python
from tykit import pb_range
from time import sleep

# use pb_range just like range()
for i in pb_range(50):
    sleep(0.001)

# or use it as a generator, with some iterabel_files
from tykit import pb_iter
some_task = lambda x: x*x
iterable_file = [x for x in range(100)]

for i in pb_iter(iterable_file):
    some_task(i)
```
![pbrange](./image/pbrange.gif)



> ___pb_multi_thread(workers:int,task,iter_files)___

This function intergrates the multi-threading with `ProgressBar`, which could show the master task's progress in a multi-threading script. The `param: workers` defined the max-worker of the multi-threading.

```python
from tykit import pb_multi_thread as pbmt

# Firstly, define your task func
task_func = lambda x: x*x*x
# Put your jobs in a iterable data structure
jobs = [x for x in range(1000)]
# run multi-threading with pb(ProgressBar)
# and save the result in a list
max_workers = 20
result = pbmt(max_workers,task_func,jobs)
print(result[10])
```

> ___pb_multi_thread_partial(workers:int,task,iter_files,**kwargs)___

This function is a higher api of ```pb_multi_thread()```, which is suitable for the multi-threading tasks with more than one parameters.

```python
from tykit import pb_multi_thread_partial as pbmtp

# define a task func with multi params
def task(x,a,b,c):
    return x+a+b+c
# Put your jobs in a iterable data structure
jobs = [x for x in range(1000)]
# run multi-threading with partial
max_workers = 20

result = pbmtp(max_workers,task,jobs,a=10,b=100,c=-20)
print(result[:10])
```

## 🛎️ rlog (Rich-log)
rlog is a module for log printing with ***rich***. It has some functions to print pretty logs and hints. The usage is simple and neat. The samples are shown below👇(for more details, you can find in [usage_of_rlog.py](https://github.com/paperplane110/tykit/blob/master/examples/usage_of_rlog.py) in examples)
![rlog_show](./image/rlog.gif)

## 💻 ~~FaceXClient~~ (used in work)
