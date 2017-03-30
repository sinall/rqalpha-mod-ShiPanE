=======
rqalpha-mod-ShiPanE
=======

`RQAlpha`_ 不支持股票实盘交易， 不过通过他的 Mod 机制，可以很方便的扩展自己的实盘交易接口。

`ShiPanE Python SDK`_ 提供了 RESTFul 接口，可以管理通达信等交易终端，因此可以实现 RQAlpha 产生的下单逻辑通过实盘易进行下单操作。


## Installation

### 安装环境

*   建议使用 Anaconda Env 来搭建 Python 虚拟环境，传送门: `基于Anaconda的环境搭建`_
*   安装 RQAlpha，参考 `RQAlpha 安装指南`_
*   更新 `lxml`

.. code-block:: bash

    $ conda install -f lxml

*   安装 `rqalpha-mod-shipane`

.. code-block:: bash

    $ pip install rqalpha-mod-shipane

### 安装实盘易扩展Mod

RQAlpha 提供了非常简单的 Mod 安装机制，直接使用如下命令即可完成 Mod 安装


.. code-block:: bash

    # 安装实盘易Mod
    $ rqalpha install shipane

    # 启用实盘易Mod
    $ rqalpha enable shipane

    # 关闭实盘易Mod
    $ rqalpha disable shipane

    # 卸载实盘易Mod
    $ rqalpha uninstall shipane

### FAQ

如果报如下错误

.. code-block:: bash

    ImportError: dlopen(/Users/eric/anaconda/envs/rqalpha/lib/python3.6/site-packages/lxml/etree.cpython-36m-darwin.so, 2): Library not loaded: @rpath/libxml2.2.dylib
      Referenced from: /Users/eric/anaconda/envs/rqalpha/lib/python3.6/site-packages/lxml/etree.cpython-36m-darwin.so
      Reason: Incompatible library version: etree.cpython-36m-darwin.so requires version 12.0.0 or later, but libxml2.2.dylib provides version 10.0.0


解决方案:

.. code-block:: bash

    conda install libxml2
    pip install -f lxml==3.6.4

.. _RQAlpha: https://github.com/ricequant/rqalpha
.. _ShiPanE Python SDK: https://github.com/sinall/ShiPanE-Python-SDK
.. _基于Anaconda的环境搭建: http://rqalpha.readthedocs.io/zh_CN/stable/intro/detail_install.html
.. _RQAlpha 安装指南: http://rqalpha.readthedocs.io/zh_CN/stable/intro/install.html
