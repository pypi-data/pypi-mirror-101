#基于httprunner封装

本次更新：

一 、基于httprunner封装，改名为mkrunner

​	1、可通过pip install mkrunner直接下载，项目启动直接使用mkrun进行启动，不需要带allure各项参数

​	2、运行结束后，本地启动httpserver服务，链接可点击到报告详情页

二、报告优化

​	1、增加case运行步骤的request，response展示，可以根据步骤查看request及response。

​	2、增加可查看case重试次数，详情中可查看历史失败原因

​	3、根据目录结构，将用例报告分类在Suites中展示。

​	4、根据运行主模块，将用例进行分类放在报告Behaviors下展示

​	5、增加报告历史趋势

三、公共方法集成到mkrunner源码中。

​	1、将一些公共方法封装到源码内，用例项目结构删util及run.py文件，修改debugtalks中公共方法调用方式。

