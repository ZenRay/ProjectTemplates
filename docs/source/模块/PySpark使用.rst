================
PySpark 使用
================

模块结构说明
----------------
PySpark 支持 make 编译，因此目录需要保持原有结构以方便编译和运行 Application

.. code-block:: bash

    ├── Makefile # 编译文件
    ├── __init__.py
    ├── jobs # 任务 module
    │   └── testjob.py
    ├── libs # 需要依赖的 jar 包和 Python 包相关文件
    │   ├── jars
    │   └── python
    ├── requirements # 存放 Python 环境依赖文件，分为了开发、生产部署以及测试不同阶段
    │   ├── dev.txt
    │   ├── prod.txt
    │   └── test.txt
    ├── settings.py # 可定制化的配置数据信息
    ├── spark.cfg   # 顶层项目说明相关配置
    └── utils   # 其他需要相关的功能功能脚本
        └── context.py

使用说明
----------

环境依赖
+++++++++
在提交 Spark 应用中，第三方的依赖包可能会出现不能被调用的问题。因此需要使用 *requirements* 文件，将相关依赖包安装到指定的目录中——该思路类似于需要调用 JAR 包的方式。

安装包依赖的命令示例，使用 ``pip install -r requirements.txt -t ./src`` 可以将 *requirements.txt* 的依赖安装到 *src* 目录中。

编译
++++++++
为了方便管理，使用 ``make`` 命令进行编译，将相关编译的流程放在 *Makefile* 中——主要包括了 **文件压缩** 和 **文件复制**。整个编译过程是将需要的环境依赖参照 ``spark-submit`` 需要的相关参数值进行编译：

1. ``--py-files`` 选项需要的是 python 相关的脚本、包及其 zip 文件
#. ``--jars`` 是提交的应用中需要依赖的外部 JAR 包

Job 编写和部署
+++++++++++++++++++
本项目的结构中，任务是统一放在 *jobs* 文件目录中。在编写任务过程中需要注意，因编译而出现的文件移动导致项目的顶层目录变化会影响应用的部署。因此在编写任务的过程中，需要注意包和脚本的导入。

部署过程：

1. 使用 ``make build`` 命令编译（实际使用编译哪个阶段，需要从 Makefile 确认）。项目会生成一个 *dependence.zip* 文件
#. 使用 ``spark-submit  --py-files dependence.zip jobs/testjob.py`` 可以提交 *jobs* 中 *testjob.py* 任务


参考
------

1. `Best Practices Writing Production-Grade PySpark Jobs <https://developerzen.com/best-practices-writing-production-grade-pyspark-jobs-cb688ac4d20f>`_
