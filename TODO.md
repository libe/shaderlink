# Decouple SL code from XML nodes #
Currently SL code is stored in XML node files. This turned out being a super bad design choice! A much better solution would be storing in XML files only calls to functions defined in headers acting as a kind of interface. Shader logic should only be created by linking nodes and NOT by editing/modifying node code content.
This major change will bring a lot of benefits as:
  * much less bloated SL code generated (just list of header file function calls)
  * much more code reuse
  * much smaller turnaround time in creating a node net, updating node code (header files) and checking result in preview

# Serialize project files as XML #
Currently Shaderlink uses Python binary serialization. By doing so it's easy and fast to save/load but user cannot understand content very easily.

# Add add add nodes... #