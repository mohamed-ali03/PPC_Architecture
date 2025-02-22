cmake_minimum_required(VERSION 3.5)
project(ppc_interfaces)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(nav_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/MissionSRV.srv"
  "srv/CreatePlanSRV.srv"
  "msg/MissionMSG.msg"
  "action/Navigate.action"
  DEPENDENCIES nav_msgs
) 

ament_export_dependencies(rosidl_default_runtime)

ament_package()
