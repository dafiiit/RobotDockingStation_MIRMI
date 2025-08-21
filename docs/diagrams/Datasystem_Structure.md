# Diagram of the Datasystem

## Phsyical Connection of Sensors: 
```mermaid
graph LR

  %% === ROBOTER ===
  subgraph Robot
    PiR(Raspberry Pi):::tumBlue
    WiFiR(WiFi + 5G Router)
    TailscaleR(Tailscale VPN Client)
    Switch(Ethernet Switch)

    %% Sensor-ESPs
    ESP_Cam[ESP - RGB Camera]
    ESP_IR[ESP - IR Camera]
    ESP_LIDAR[ESP - LIDAR]
    ESP_GPSR[ESP - GPS Receiver]
    ESP_FlowPump[ESP - Flowrate Sensor + 2x Pumps]

    %% Sensoren & Aktoren
    Cam(Camera)
    IR(IR Camera)
    LIDAR(LIDAR)
    GPSR(GPS Receiver)
    Flow(Flowrate Sensor)
    Pump1(Pump 1)
    Pump2(Pump 2)

    %% Verbindungen intern
    PiR --> WiFiR --> TailscaleR
    PiR -->|ROS2| Switch
    Switch --> ESP_Cam
    Switch --> ESP_IR
    Switch --> ESP_LIDAR
    Switch --> ESP_GPSR
    Switch --> ESP_FlowPump

    ESP_Cam --> Cam
    ESP_IR --> IR
    ESP_LIDAR --> LIDAR
    ESP_GPSR --> GPSR
    ESP_FlowPump --> Flow
    ESP_FlowPump --> Pump1 & Pump2
  end

  %% === DOCKINGSTATION ===
  subgraph Docking_Station
    PiD(Raspberry Pi):::tumBlue
    WiFiD(WiFi Router / Hotspot)
    TailscaleD(Tailscale VPN Client)

    %% ESP-Controller nach Gruppen
    ESP_Actuator[ESP - 4x Linear Actuators]
    ESP_Fluid[ESP - 2x Pumps + 3x Fluid Valves]
    ESP_Signal[ESP - IR-LED + GPS]

    %% Aktoren
    LA1(Linear Actuator 1)
    LA2(Linear Actuator 2)
    LA3(Linear Actuator 3)
    LA4(Linear Actuator 4)

    DPump1(Pump A)
    DPump2(Pump B)
    Valve1(Valve 1)
    Valve2(Valve 2)
    Valve3(Valve 3)

    IRLED(IR-LED)
    GPS_Tx(GPS Emitter)

    %% Verbindungen Dock
    PiD --> WiFiD --> ESP_Signal
    WiFiD --> ESP_Actuator
    WiFiD --> ESP_Fluid
    WiFiD --> TailscaleD 

    ESP_Actuator --> LA1 & LA2 & LA3 & LA4
    ESP_Fluid --> DPump1 & DPump2 & Valve1 & Valve2 & Valve3
    ESP_Signal --> IRLED & GPS_Tx
  end

  %% === ROS2 Netzwerkkommunikation ===
  TailscaleR -->|ROS2 Topics / Services| TailscaleD
  %%PiR -->|ROS2 Nodes| PiD
  
    %% === Styles ===
    %% TUM Farben und modernes Design für alle Diagramme
    %% --- BASIS-STYLES ---
    classDef tumBlue fill:#0065BD,stroke:#003359,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    classDef tumLightBlue fill:#64A0C8,stroke:#003359,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    classDef tumOrange fill:#E87722,stroke:#B85A1A,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    classDef tumGreen fill:#A2AD00,stroke:#7A8500,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    %% --- SUBGRAPH-STYLES ---
    style Robot fill:#F8FBFF,stroke:#0065BD,stroke-width:3px,rx:20,ry:20,color:#000000,font-size:16px,font-weight:bold;

    style Docking_Station fill:#F2FAF9,stroke:#64A0C8,stroke-width:3px,rx:20,ry:20,color:#000000,font-size:16px,font-weight:bold;

    %% Alle Verbindungen einheitlich stylen
    linkStyle default stroke:#0065BD,stroke-width:2px;
```
## ROS2 connection of sensors

### Nodes
A Node is an executable program that performs a specific task. Think of each node as a small, independent specialist. You'll have nodes on both the robot and the docking station.

### Topics
A Topic is like a radio channel where nodes can publish (broadcast) messages. Other nodes can subscribe (listen) to these topics to get the data. Topics are for continuous data streams.

###  Services and Actions
While Topics are for continuous data, Services are for request/response interactions (like a function call). Actions are for long-running tasks where you need feedback.

```mermaid
graph LR
    subgraph Docking_Station
        %% --- STATION NODES ---
        station_manager[station_manager_node]
        door_controller[door_controller_node]
        fluid_controller[fluid_controller_node]
        emitter_controller[emitter_controller_node]
    end
    subgraph Robot
        %% --- SENSOR DRIVER NODES ---
        subgraph Sensor_Drivers
            direction LR
            cam_node[camera_node]
            ir_cam_node[ir_camera_node]
            lidar_node[lidar_node]
            gps_node[gps_node]
        end

        %% --- PERCEPTION NODES ---
        subgraph Perception
            direction LR
            apriltag_node[apriltag_detector_node]
            depth_node[depth_estimation_node]
        end
        
        %% --- CONTROL & NAVIGATION NODES ---
        subgraph Control&Navigation
            direction LR
            docking_controller[docking_controller_node]
            nav2_stack[NAV2 Stack]
            robot_state_publisher[robot_state_publisher]
            pump_controller[robot_pump_controller]
        end

        %% --- ROBOT DATA FLOW ---
        cam_node -- /camera/image_raw --> apriltag_node
        cam_node -- /camera/image_raw --> depth_node

        apriltag_node -- /apriltag/detections --> docking_controller
        
        ir_cam_node -- /ir_camera/image_raw --> docking_controller
        lidar_node -- /scan --> nav2_stack
        gps_node -- /gps/fix --> nav2_stack

        depth_node -- /depth/point_cloud --> nav2_stack


        docking_controller -- /cmd_vel --> nav2_stack
        nav2_stack -- /cmd_vel --> RobotHardwareInterface:::tumBlue
        
        docking_controller -- /robot/pump_cmd --> pump_controller
        
    end

    %% === Cross-System Communication (via Tailscale VPN) ===
    docking_controller -.->|/dock_robot| station_manager
    station_manager -- /station/control_door (Service) --> door_controller
    station_manager -- /station/start_filling (Service) --> fluid_controller
    station_manager -- /station/set_emitters (Service) --> emitter_controller
    
    %% === Styles ===
    %% TUM Farben und modernes Design für alle Diagramme
    %% --- BASIS-STYLES ---
    classDef tumBlue fill:#0065BD,stroke:#003359,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    classDef tumLightBlue fill:#64A0C8,stroke:#003359,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    classDef tumOrange fill:#E87722,stroke:#B85A1A,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    classDef tumGreen fill:#A2AD00,stroke:#7A8500,stroke-width:2px,color:#ffffff,rx:12,ry:12,font-size:14px,font-weight:bold;

    %% --- SUBGRAPH-STYLES ---
    style Robot fill:#F8FBFF,stroke:#0065BD,stroke-width:3px,rx:20,ry:20,color:#000000,font-size:16px,font-weight:bold;

    style Docking_Station fill:#F2FAF9,stroke:#64A0C8,stroke-width:3px,rx:20,ry:20,color:#000000,font-size:16px,font-weight:bold;

    style Sensor_Drivers fill:#D3D3D3, color:#000000
    style Perception fill:#D3D3D3, color:#000000
    style Control&Navigation fill:#D3D3D3, color:#000000

    %% Alle Verbindungen einheitlich stylen
    linkStyle default stroke:#0065BD,stroke-width:2px;

```

