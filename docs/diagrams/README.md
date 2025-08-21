# Diagramme erstellen
1. erstelle das .mmd file
2. Schreibe den Mermaid Code
3. Nutze als Style: 

```python
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
4. Füge für alle subgraphs die richtigen Namen in Dubgraph Styles hinzu
5. Gebe im Terminal ein: 
```python
mmdc -i Name.mmd -o Name.svg;  
```
6. Für png: 
```python
mmdc -i ROS2_Structure.mmd -o ROS2_Structure.png --scale 4
```
