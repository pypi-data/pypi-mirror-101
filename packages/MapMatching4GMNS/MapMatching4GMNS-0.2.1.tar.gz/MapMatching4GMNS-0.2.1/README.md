# MapMatching4GMNS

Please send your comments to <xzhou74@asu.edu> if you have any suggestions and
questions.

Based on input network and given GPS trajectory data, the map-matching program
of Matching2Route aims to find most likely route in terms of node sequence in
the underlying network, with the following data flow chart.

![](media/5d46d46e6d66cfe932399f796dcd713c.png)

The 2D grid system aims to speed up the indexing of GSP points to the network.
For example, a 10x10 grid for a network of 100 K nodes could lead to 1K nodes in
each cell. We first identify all cells traveled by a GPS trace, so only a small
subset of the network will be loaded in the resulting shortest path algorithm.

The link cost estimation step calculates a generalized weight/cost for each link
in the cell, that is, the distance from nearly GPS points to a link inside the
cell. The likely path finding algorithm selects the least cost path with the
smallest generalized cumulative cost from the beginning to the end of the GPS
trace.


1.  **Data flow**

| **Input files** | **Output files** |
| --------------- | ---------------- |
| node.csv        | agent.csv        |
| link.csv        |                  |
| input_agent.csv |                  |

2.  **Input file description**

    **File node.csv** gives essential node information of the underlying
    (subarea) network in GMNS format, including node_id, x_coord and y_coord.

![](media/1fa21c1d6e8cfdd05b74ce9d3f48bf9f.png)

**File link.csv** provides essential link information of the underlying
(subarea) network, including link_id, from_node_id and to_node_id.

![](media/1f78e34e3e8ff4091a1997e44825a503.png)

**Input trace file** as input_agent.csv. The geometry field describes longitude
and latitude of each GPS point along the trace of each agent. In the following
example there are exactly 2 GPS points as the origin and destination locations,
while other examples can include more than 2 GPS points along the trace. The
geometry field follows the WKT format.

https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry

![](media/308de5075f12b12dab40c3309182b047.png)

3.  **Output file description**

    **File agent.csv** describes the most-likely path for each agent based on
    input trajectories.

![](media/caec124ffd9a88d841b924a0dda3d3b7.png)


4. **Installation**
   Path4GMNS has been published on [PyPI](https://pypi.org/project/MapMatching4GMNS/), and can be installed using
```
$ pip install MapMatching4GMNS
```
If you need a specific version of Path4GMNS, say, 0.21,
If you want to test the latest features of Path4GMNS, you can build the package from sources and install it offline, where **Python 3.x** is required.
```
$ pip install MapMatching4GMNS==0.2
```
# from the root directory of PATH4GMNS
$ python setup.py sdist bdist_wheel
$ cd dist
$ python -m pip install MapMatching4GMNS-version.tar.gz
``` 
The shared libraries of [MapMatching4GMNS](https://github.com/asu-trans-ai-lab/MapMatching4GMNS/engine)  for Path4GMNS can be built with a C++ compiler supporting C++11 and higher, where we use CMake to define the building process. Take MapMatching4GMNS_engine for example,
# from the root directory of engine
$ mkdir build
$ cd build
$ cmake ..
$ cmake --build .
You can replace the last command with $ make if your target system has Make installed.
### Caveat
As **CMAKE_BUILD_TYPE** will be **IGNORED** for IDE (Integrated Development Environment) generators, e.g., Visual Studio and Xcode, you will need to manually update the build type from debug to release in your IDE and build your target from there. 

5. **Getting Started**
```
$ #To avoid complex data folder settings, please always first put the input data on the current directory
$ !pip install MapMatching4GMNS --upgrade
$ import time
$ start = time.time() 
$ """Once the package is imported, agent.csv can be generated"""
$ import MapMatching4GMNS as mmg
$ end = time.time()
$ print('time cost: %.6f'%(end-start))
```

6. **Features:**

   1: The grid size is dynamically calculated based on the number of nodes per cell.
   2: To avoid complex data folder settings, please always first assume work on the current directory. 
  
7. **Challenges:**

   1: The boundary identification might still have issues.
   2: Outputing matched time and delay information is needed for traffic performance evaluation.


**Reference:**

This code is implemented based on a published paper in Journal of Transportation
Research Part C:

Estimating the most likely space–time paths, dwell times and path uncertainties
from vehicle trajectory data: A time geographic method

https://www.sciencedirect.com/science/article/pii/S0968090X15003150
