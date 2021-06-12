#database 

## CMakeLists lines for compiling with PostgreSQL dependencies

```cmake
# This command attempts to find the library, REQUIRED argument is optional
find_package(PostgreSQL REQUIRED)

# Add include directories to your target. PRIVATE is useful with multi-target projects - see documentation of target_include_directories for more info
target_include_directories(MyTarget PRIVATE ${PostgreSQL_INCLUDE_DIRS})

# Add libraries to link your target againts. Again, PRIVATE is important for multi-target projects
target_link_libraries(MyTarget PRIVATE ${PostgreSQL_LIBRARIES})
```
