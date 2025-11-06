from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('ur5_rg2_description')
    desc = PathJoinSubstitution([pkg, 'urdf', 'ur5_rg2.urdf.xacro'])
    controllers = PathJoinSubstitution([pkg, 'config', 'controllers.yaml'])

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', desc])},
                    {'use_sim_time': True}]
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'ur5_rg2', '-topic', 'robot_description', '-z', '0.0'],
        output='screen'
    )

    jsb = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster',
                   '--controller-manager', '/controller_manager',
                   '--param-file', controllers],
        output='screen'
    )

    jtc = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller',
                   '--controller-manager', '/controller_manager',
                   '--param-file', controllers],
        output='screen'
    )

    return LaunchDescription([
        rsp,
        TimerAction(period=2.0, actions=[spawn]),
        TimerAction(period=4.0, actions=[jsb]),
        TimerAction(period=5.0, actions=[jtc]),
    ])