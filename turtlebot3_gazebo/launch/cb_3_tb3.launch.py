from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    launch_files = [
        # (패키지명, 런치파일명, 추가 인자)
        ("turtlebot3_gazebo", "turtlebot3_autorace_2020.launch.py", {}),
        ("turtlebot3_autorace_camera", "intrinsic_camera_calibration.launch.py", {}),
        ("turtlebot3_autorace_camera", "extrinsic_camera_calibration.launch.py", {}),
        ("turtlebot3_autorace_detect", "detect_lane.launch.py", {"calibration_mode": "True"}),
        #("turtlebot3_autorace_detect", "detect_lane.launch.py", {}),
        #("turtlebot3_autorace_detect", "detect_sign.launch.py", {"mission": "intersection"}),
        #("turtlebot3_autorace_detect", "detect_sign.launch.py", {"mission": "construction"}),
        #("turtlebot3_autorace_detect", "detect_sign.launch.py", {"mission": "parking"}),
        #("turtlebot3_autorace_detect", "detect_sign.launch.py", {"mission": "level_crossing"}),
        #("turtlebot3_autorace_detect", "detect_sign.launch.py", {"mission": "tunnel"}),
        #("turtlebot3_autorace_detect", "detect_traffic_light.launch.py", {}),
        #("turtlebot3_autorace_detect", "detect_level_crossing.launch.py", {}),
        #("turtlebot3_autorace_mission", "mission_construction.launch.py", {}),
        #("turtlebot3_autorace_mission", "mission_tunnel.launch.py", {}),
        ("turtlebot3_autorace_mission", "control_lane.launch.py", {}),
    ]

    includes = []
    for pkg, file, args in launch_files:
        launch_args = [(k, v) for k, v in args.items()]
        launch_path = os.path.join(get_package_share_directory(pkg), "launch", file)
        includes.append(
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(launch_path), launch_arguments=launch_args
            )
        )


    follower_node = ExecuteProcess(
        cmd=[
            'python3',
            '/home/rokey/turtlebot3_ws/src/turtlebot3_autorace/turtlebot3_autorace_mission/turtlebot3_autorace_mission/tb3_follower.py'
        ],
        output='screen'
    )

    # teleop_keyboard 노드 실행 추가 (필요시 주석 해제)
    # teleop = ExecuteProcess(
    #     cmd=['ros2', 'run', 'turtlebot3_teleop', 'teleop_keyboard'],
    #     output='screen'
    # )

    # return LaunchDescription(includes + [teleop])
    return LaunchDescription(includes + [follower_node])