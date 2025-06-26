from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import os
import re

def generate_launch_description():
    TURTLEBOT3_MODEL = os.environ.get('TURTLEBOT3_MODEL', 'burger')
    number_of_robots = 1
    pose_list = [[0, -1.747]]

    ld = LaunchDescription()

    for idx in range(number_of_robots):
        robot_name = f"{TURTLEBOT3_MODEL}_{idx}"
        namespace = f"tb3_{idx}"
        x_pose = str(pose_list[idx][0])
        y_pose = str(pose_list[idx][1])

        # SDF 모델 경로
        sdf_path = os.path.join(
            get_package_share_directory('turtlebot3_gazebo'),
            'models',
            f'turtlebot3_{TURTLEBOT3_MODEL}',
            'model.sdf'
        )

        with open(sdf_path, 'r') as f:
            sdf_content = f.read()

        # 리더만 카메라 네임스페이스 적용
        if idx == 0: 
            camera_namespace = f"{namespace}/camera"

            def insert_namespace_to_camera_plugin(sdf, ns):
                pattern = r'(<plugin[^>]*filename="libgazebo_ros_camera.so"[^>]*>)(.*?)(</plugin>)'
                def repl(match):
                    start, body, end = match.groups()
                    if '<ros>' in body:
                        if '<namespace>' in body:
                            body = re.sub(r'<namespace>.*?</namespace>', f'<namespace>{ns}</namespace>', body)
                        else:
                            body = body.replace('<ros>', f'<ros>\n    <namespace>{ns}</namespace>')
                    else:
                        body += f'\n  <ros>\n    <namespace>{ns}</namespace>\n  </ros>'
                    return start + body + end
                return re.sub(pattern, repl, sdf, flags=re.DOTALL)
            
            sdf_content = insert_namespace_to_camera_plugin(sdf_content, camera_namespace)
        else:
            # 팔로워는 카메라 플러그인 제거
            def remove_camera_plugin(sdf):
                return re.sub(
                    r'<plugin[^>]*filename="libgazebo_ros_camera.so"[^>]*>.*?</plugin>',
                    '',
                    sdf,
                    flags=re.DOTALL
                )
            sdf_content = remove_camera_plugin(sdf_content)

        # 수정된 SDF 임시 저장
        tmp_sdf_path = f'/tmp/tb3_{idx}_model.sdf'
        with open(tmp_sdf_path, 'w') as f:
            f.write(sdf_content)

        # Gazebo 로봇 스폰 노드
        spawn_cmd = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity', robot_name,
                '-file', tmp_sdf_path,
                '-x', x_pose,
                '-y', y_pose,
                '-z', '0.01',
                '-robot_namespace', namespace
            ],
            output='screen',
            namespace=namespace
        )
        ld.add_action(spawn_cmd)

    return ld
