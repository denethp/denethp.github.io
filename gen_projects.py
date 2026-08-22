import os, html, subprocess

SITE = "/home/claude/site"
PROJ_DIR = os.path.join(SITE, "projects")
MICE_DIR = os.path.join(PROJ_DIR, "mice")
os.makedirs(PROJ_DIR, exist_ok=True)
os.makedirs(MICE_DIR, exist_ok=True)

_ASPECT_CACHE = {}

def video_aspect_ratio(path):
    """Return 'W/H' CSS aspect-ratio string for a video file, via ffprobe.
    Falls back to 16/9 if the file is missing or ffprobe fails."""
    if path in _ASPECT_CACHE:
        return _ASPECT_CACHE[path]
    ratio = "16/9"
    if os.path.exists(path):
        try:
            out = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height",
                 "-of", "csv=s=x:p=0", path],
                capture_output=True, text=True, timeout=10,
            ).stdout.strip()
            w, h = out.split("x")
            w, h = int(w), int(h)
            if w > 0 and h > 0:
                ratio = f"{w}/{h}"
        except Exception:
            pass
    _ASPECT_CACHE[path] = ratio
    return ratio


def mouse_card_html(label, date, tagline, meta, img_src, href):
    return f'''<a class="mouse-card" href="{href}">
          <img src="{img_src}" alt="{html.escape(label)}" loading="lazy">
          <div class="mouse-card-body">
            <span class="mouse-card-date">{html.escape(date)}</span>
            <h3>{html.escape(label)}</h3>
            <p class="mouse-card-tagline">{html.escape(tagline)}</p>
            <span class="mouse-card-meta">{html.escape(meta)}</span>
          </div>
        </a>'''

projects = [
  dict(
    slug="6dof-robotic-arm",
    title="6-DOF Robotic Arm",
    github="https://github.com/denethp/6-dof-robotic-arm",
    tag="Robotics Project",
    status="Completed",
    accent=True,
    dates="Feb 2026 – Jul 2026",
    role="Firmware, Kinematics & Digital Twin, and Mechanical Design of the Arm",
    team="Collaborative build",
    lede="A 6-DOF robotic arm built entirely from scratch: mechanics, firmware, kinematics, and a live digital twin, all driven from a single command.",
    overview=[
      "A fully custom 6-axis robotic arm, not a kit. Every layer was designed, debugged and integrated in-house. A SolidWorks CAD assembly feeds a Simscape Multibody digital twin, which shares its rigid-body model with a MATLAB inverse-kinematics solver; solved trajectories stream over USB CDC to an STM32H743 running at 420MHz, which drives six stepper axes and a gripper while reading back position from six AS5047P absolute encoders. The headline feature: a single command moves the physical arm and its 3D digital twin simultaneously, in sync, in real time.",
      "Motor selection followed one rule: torque scales with how much arm you're carrying. The base and shoulder/elbow joints (which lift the entire outboard arm) run on NEMA 24 and NEMA 23 steppers through closed-loop CL57T drivers, so a missed step gets detected and corrected before it becomes a dropped arm. The wrist joints only have to position the end-effector, so they run smaller NEMA 17s on onboard TMC2209 drivers instead. All six axes are computed independently inside a single 2kHz timer interrupt running a trapezoidal accelerate–cruise–decelerate profile.",
      "The kinematic model is the same rigidBodyTree on both sides of the USB link: MATLAB's inverseKinematics solver turns a target position and orientation into six joint angles, which are blended into a quintic (5th-order) trajectory for zero velocity and acceleration at both ends of every move, so the arm starts and stops smoothly instead of jerking. Along the way this project proved out a real kinematics constraint: a 6-DOF arm cannot hold both tip position and tool orientation fixed while it reconfigures (that needs a 7th degree of freedom), so every demo deliberately locks one and sweeps the other.",
      "The hardest bug wasn't mechanical; it was a phantom one. Encoder readings on a stationary joint appeared to swing 60–70° between samples, and slowing the SPI clock down made it worse, which ruled out a signal-integrity problem. The actual cause was a −1 error sentinel from a failed read being silently averaged in with valid samples; filtering it out before averaging brought repeatability to ±0.01°. A separate Web Serial control panel now lets anyone drive the arm from Chrome or Edge alone, offering recorded sequences, per-joint sliders and a live command log, with no MATLAB license required to operate it, even though MATLAB remains the authoring environment for kinematics and trajectory design.",
    ],
    features=[
      "Tiered stepper drivetrain (NEMA 24/23/17) matched to torque and stall risk per joint, with closed-loop CL57T drivers on the two lifting joints",
      "Six AS5047P absolute magnetic encoders (14-bit, SPI) giving every joint real position feedback",
      "2kHz trapezoidal motion-profile ISR on an STM32H743 @ 420MHz, computing accel/cruise/decel independently per axis",
      "MATLAB rigidBodyTree + inverseKinematics solver with quintic-blended trajectories for jerk-free motion",
      "Synchronised digital twin — one command drives the physical arm and the Simscape 3D model together, in real time",
      "Custom control PCB (Altium Designer) integrating the STM32H743, encoder SPI bus and mixed open-drain/push-pull driver interfacing",
      "Standalone Web Serial control panel — browser-only jogging, recorded sequences and live command logging, no MATLAB or Python required to operate",
      "OpenCV colour-segmentation and homography pipeline converting camera pixels into real-world XYZ targets for the inverse-kinematics solver",
    ],
    stack=["STM32H743", "C (HAL)", "MATLAB / Simscape", "Altium Designer", "SolidWorks", "AS5047P Encoders", "Web Serial API", "OpenCV / Python"],
    tags="robotics embedded vision",
    gallery=[
      ("arm-final-hero.jpg", "The completed 6-DOF arm — gripper detail"),
      ("arm-side-profile.jpg", "Full side profile — base to gripper"),
      ("arm-front-angle.jpg", "Front three-quarter view"),
      ("arm-rear-view.jpg", "Rear view showing the shoulder and elbow drivetrain"),
    ],
    videos=[
      ("arm-vision-detection.mp4", "Vision-Guided Object Detection"),
      ("arm-object-localization.mp4", "Object Localization & Reach"),
      ("arm-wrist-roll.mp4", "Wrist Roll"),
      ("arm-base-rotation.mp4", "Base Rotation"),
      ("arm-motors-bench.mp4", "Motors & Drivers Bench Test"),
      ("arm-prototype-build.mp4", "Early Prototype Build"),
    ],
    youtube=[
      ("oTu1l9RB2gY", "Full Summary Video"),
    ],
  ),
  dict(
    slug="micromouse-maze-solver",
    github="https://github.com/denethp/micromouse-showcase",
    title="Micromouse Autonomous Maze Solver",
    tag="Robotics Project",
    status="Ongoing",
    accent=True,
    dates="Jun 2025 – Present",
    role="End-to-End Design: 3D CAD Design, Hardware, Electronic & PCB Design, Soldering, Firmware & Control Systems, and Trajectory Planning",
    team="Collaborative build",
    lede="A micromouse built to explore, map and solve a 16×16 maze at speed, competing nationally.",
    overview=[
      "Micromouse competitions reward the intersection of speed and certainty: a robot has to map an unknown 16×16 maze in real time, then commit to the fastest verified route through it. This project tackles both halves of that problem, exploration and optimal-path execution, on a custom STM32-based mouse.",
      "Real-time maze mapping runs alongside a flood-fill algorithm that recomputes the shortest known path to the goal as new walls are discovered. Once the maze is sufficiently mapped, the mouse switches to a speed run using motion-profiled trajectories.",
      "Getting the mouse to actually hit those trajectories required PID control tuned with both feedback and feedforward terms, with the control loop parameters first modeled and validated in MATLAB before being deployed to hardware. This was critical for a robot where a few degrees of heading error compounds fast in a tight maze."
    ],
    features=[
      "Real-time maze mapping during exploration runs, updated wall-by-wall as the mouse moves",
      "Flood-fill algorithm for continuously recomputing the shortest verified path to the goal",
      "Motion profiling for smooth acceleration/deceleration through straights and turns",
      "PID motor control with feedback and feedforward terms tuned via MATLAB system modeling",
      "Custom-designed control PCB (\"BLAZE v2.0\") integrating the STM32, motor drivers and sensor interfacing on a maze-scale footprint",
      "Selected among the Top 10 teams at Micromaze 2.0, IIT",
    ],
    stack=["STM32", "N20 DC Motors (1000 RPM)", "C/C++", "Altium Designer", "SOLIDWORKS", "MATLAB"],
    tags="robotics embedded",
    gallery=[
      ("blaze-v2/blaze-v2-1.jpg", "Fully assembled micromouse — front three-quarter view"),
      ("blaze-v2/blaze-v2-2.jpg", "Fully assembled micromouse — rear three-quarter view"),
      ("blaze-v2/blaze-v2-3.jpg", "Top-down view — battery, control board and wiring"),
      ("blaze-v2/blaze-v2-4.jpg", "Fully assembled micromouse — side three-quarter view"),
      ("blaze-v2/blaze-v2-5.jpg", "Ground-level view showing wheel and chassis clearance"),
      ("blaze-v2/blaze-v2-6.jpg", "Partially assembled — motors and sensor wiring"),
      ("blaze-v2/blaze-v2-7.jpg", "Partially assembled — control board and buzzer close-up"),
      ("blaze-v2/blaze-v2-8.jpg", "The custom control PCB — front and back"),
      ("blaze-v2/blaze-v2-9.jpg", "The custom control PCB — routing layout"),
    ],
    youtube=[
      ("k_U8wT8emE4", "Search Run Demo"),
      ("94TpTno4ck4", "Fast Run Demo"),
    ],
    older_mice=[
      dict(
        gid="blaze-v1",
        label="Blaze v1",
        date="Dec. 2025",
        tagline="First STM32 build",
        meta="STM32G431CBU6 · Custom PCB",
        role="Hardware Design, Electronic Design, PCB Design, Soldering, Firmware & Control Systems / Trajectory Planning",
        blurb="The first STM32-based mouse, moving off the Teensy platform onto an STM32G431CBU6 microcontroller for tighter real-time control and a cleaner custom PCB design. It's the direct predecessor to the current Blaze v2.",
        images=[
          ("blaze-v1/blaze-v1.jpg", "Blaze v1"),
          ("blaze-v1/blaze-v1-circuit-front.jpg", "Blaze v1 control board — front"),
          ("blaze-v1/blaze-v1-circuit-back.jpg", "Blaze v1 control board — back"),
        ],
        videos=[
          ("blaze-v1/blaze-v1-intro-video.mp4", "Intro"),
        ],
      ),
      dict(
        gid="chia-v3",
        label="Chia v3",
        date="Sep. 2025",
        tagline="Custom PCB, more power",
        meta="Teensy 4.1 · Custom 2-layer PCB",
        role="Firmware & Control Systems / Trajectory Planning",
        blurb="An enhanced iteration on the same Teensy 4.1 core, moving to a custom 2-layer PCB with integrated motor drivers and 1000 RPM DC motors. Power management and the mechanical design were refined based on lessons from Chia v2.",
        images=[
          ("chia-v3/chia-v3.jpg", "Chia v3 — assembled board"),
          ("chia-v3/chia-v3-pcb-layout.jpg", "Chia v3 control board — PCB routing layout"),
        ],
      ),
      dict(
        gid="chia-v2",
        label="Chia v2",
        date="Aug. 2025",
        tagline="First working platform",
        meta="Teensy 4.1 · Custom electronics",
        role="Firmware & Control Systems / Trajectory Planning",
        blurb="The foundational platform: a Teensy 4.1 at the core, with hand-built electronics, IR wall-detection sensors and encoder-based motor control. Chia v2 proved out the basic exploration-and-solve loop and went on to compete at Micromaze 2.0, IIT.",
        images=[
          ("chia-v2/chia-v2.jpg", "Chia v2 — assembled control board"),
        ],
      ),
      dict(
        gid="chia-v1",
        label="Chia v1",
        date="Jun. 2025",
        tagline="Where it all started",
        meta="Teensy 3.2 · Custom electronics",
        role="Firmware & Control Systems / Trajectory Planning",
        blurb="The very first build: a Teensy 3.2 at the core, with hand-wired electronics and simple IR wall-detection. Chia v1 is where the exploration-and-solve logic was first proven out on real hardware.",
        images=[
          ("chia-v1/chia-v1.jpg", "Chia v1 — the first working mouse"),
        ],
        videos=[
          ("chia-v1/chia-v1-clip-1.mp4", "Run Clip 1"),
          ("chia-v1/chia-v1-clip-2.mp4", "Run Clip 2"),
          ("chia-v1/chia-v1-clip-3.mp4", "Run Clip 3"),
        ],
      ),
    ],
    current_mouse=dict(
      gid="blaze-v2",
      label="Blaze v2",
      date="Mar. 2026",
      tagline="Current generation",
      meta="STM32 · Custom 4-layer PCB",
      thumb="blaze-v2/blaze-v2-1.jpg",
    ),
  ),
  dict(
    slug="ros2-vision-line-follower",
    title="ROS 2 Vision-Based Autonomous Line Following Robot",
    tag="Personal Project",
    status="Ongoing",
    accent=True,
    dates="Jun 2026 – Present",
    role="Full-stack Robotics (Perception → Control)",
    team="Individual (Personal Project)",
    lede="A ROS 2 mobile robot that follows a line using nothing but a camera and a modular perception-to-control pipeline.",
    overview=[
      "This is a personal project to build a proper ROS 2 stack from scratch rather than relying on simple analog line sensors. A Raspberry Pi 4 runs the core ROS 2 graph, receiving frames from a camera and processing them through an OpenCV-based image pipeline to detect the line's position and curvature in real time.",
      "Rather than one monolithic control script, the system is split into modular ROS 2 nodes: one for image processing and line detection, one for decision-making (translating detected line geometry into a target heading), and one for motion control that converts that heading into differential drive commands for the N20 motors, coordinated through an ESP32.",
      "The modular node structure means each part of the pipeline (perception, decision, and control) can be tuned, tested or swapped independently, which has made it much easier to debug failure modes (e.g. lighting changes) in isolation."
    ],
    features=[
      "Camera-based real-time line detection and curvature estimation using OpenCV",
      "Modular ROS 2 node architecture: perception, decision-making, and motion control as separate nodes",
      "Runs on Raspberry Pi 4 with an ESP32 handling low-level motor control",
      "rclcpp-based nodes for low-latency C++ performance in the perception pipeline",
      "Designed to be extensible toward more complex path-following and obstacle-avoidance behaviors",
    ],
    stack=["ROS 2 (rclcpp)", "OpenCV", "C/C++", "Raspberry Pi 4", "ESP32", "Camera", "N20 DC Motors"],
    tags="robotics vision software",
  ),
  dict(
    slug="master-slave-robot-slrc",
    github="https://github.com/denethp/autonomous-dual-world-robot",
    title="Autonomous Physical-Virtual Master-Slave Robot System",
    tag="Robotics Project",
    status="Completed",
    accent=False,
    dates="Jan 2026 – Mar 2026",
    role="Firmware (Distributed Control), Control Systems, Vision, Navigation & Networked Control",
    team="Collaborative build",
    lede="A physical robot that discovers a maze and remotely commands a simulated 'slave' robot through 14 waypoints, built for the Sri Lankan Robotics Challenge 2026.",
    overview=[
      "SLRC 2026's University Category set an unusual challenge: a real-world robot has to explore and decode a maze, then use what it learns to control a separate, networked simulated robot in real time, all while a dynamically patrolling hostile agent tries to intercept it.",
      "Our physical robot used AprilTag-based navigation to localize itself and decode a sequence of multi-key coordinates hidden throughout the maze. It also performed physical object pick-and-place using a custom-built slider mechanism as part of the task sequence.",
      "The decoded waypoint sequence was then transmitted over a REST API to control a networked simulated 'slave' robot through 14 sequenced waypoints, with logic built in to dynamically avoid a hostile agent patrolling the simulated environment. The entry was selected among the Top 8 nationally."
    ],
    features=[
      "AprilTag-based localization and maze navigation for the physical 'master' robot",
      "Multi-key coordinate decoding to build the waypoint sequence for the virtual robot",
      "Custom slider mechanism for physical object pick-and-place",
      "Real-time REST API control of a networked simulated robot across 14 sequenced waypoints",
      "Dynamic avoidance logic against a patrolling hostile agent in the simulated environment",
      "Finalist — Top 8 nationally, SLRC 2026 University Category",
    ],
    stack=["Raspberry Pi 4", "Camera", "Arduino Mega", "Arduino Nano", "OpenCV", "C/C++", "REST API"],
    tags="robotics vision embedded",
    gallery=[
      ("master-slave-robot-1.png", "The completed physical robot — arm and onboard electronics"),
      ("master-slave-robot-2.png", "Close-up of the arm, sensor wiring and control board"),
      ("master-slave-robot-3.png", "Navigating the maze during the SLRC 2026 competition round"),
      ("master-slave-robot-4.png", "Reviewing the robot's run beside the maze during competition"),
      ("master-slave-robot-5.jpg", "The full electronics stack — Raspberry Pi 4, Arduino Mega, camera and driver boards"),
    ],
    youtube=[
      ("xlX__w1153E", "Summary Video"),
    ],
  ),
  dict(
    slug="multi-challenge-competition-robot",
    github="https://github.com/denethp/autonomous-multi-challenge-competition-robot",
    title="Autonomous Multi-Challenge Competition Robot",
    tag="Robotics Project",
    status="Completed",
    accent=False,
    dates="Feb 2025 – Jul 2025",
    role="Firmware (Distributed Control), Control Systems, Navigation & Networked Control",
    team="Collaborative build",
    lede="A single autonomous robot engineered to clear grid navigation, line tracking, ramp ascent, wall following and target shooting in one uninterrupted run.",
    overview=[
      "Built for a Robot Design and Competition challenge, this robot had to autonomously complete a sequence of very different physical challenges without any operator intervention: navigating a structured grid by detecting intersections and reasoning about direction, tracking a broken/dotted line under closed-loop PID correction, climbing and descending an inclined ramp under active velocity control, following the curvature of a circular wall using an IR sensor array, and finally aligning to a target and firing a motor-driven projectile launcher.",
      "The firmware is organized as a modular, task-based Arduino codebase rather than one monolithic sketch: each behavior (grid mapping, dotted-line PID, ramp climbing, wall following, shooting) lives in its own file, with a central main control loop handling task switching, mode management and execution sequencing so the robot can hand off cleanly from one challenge to the next.",
      "Underneath every task sits the same differential-drive foundation: shared translational and rotational motion primitives, a common low-level motor instruction layer, and sensor filtering utilities that feed the IR array readings into whichever task is currently active. Ramp ascent in particular relies on active motor power compensation to hold a stable climb rate as the incline changes the load on the drivetrain.",
    ],
    features=[
      "Grid navigation with intersection detection, mapping and directional decision logic",
      "PID-controlled line tracking that holds trajectory across broken/dotted line segments",
      "Velocity-controlled ramp ascent and descent with active motor power compensation",
      "Circular wall following via a continuous IR sensor array distance measurement",
      "Motor-driven projectile launcher with target alignment and triggered firing",
      "Modular task-based Arduino firmware with centralized task switching and mode management",
    ],
    stack=["Arduino", "C/C++", "IR Sensor Array", "PID Control", "Differential Drive"],
    tags="robotics embedded",
    gallery=[
      ("robot-front.jpg", "The completed competition robot"),
      ("robot-isometric.jpg", "Isometric CAD view of the robot chassis"),
    ],
    videos=[
      ("multi-challenge-robot-line-following.mp4", "Dotted Line Following"),
      ("multi-challenge-robot-ramp.mp4", "Ramp Ascent"),
      ("multi-challenge-robot-circular-wall.mp4", "Circular Wall Following"),
    ],
  ),
  dict(
    slug="analog-line-follower",
    github="https://github.com/denethp/fully-analog-line-follower",
    title="Fully Analog Line Follower",
    tag="Robotics Project",
    status="Completed",
    accent=False,
    dates="Aug 2025 – Dec 2025",
    role="Electronic Design, 1kHz PWM Generation, and Analog-Level Control Systems Design",
    team="Collaborative build",
    lede="A microcontroller-free autonomous line follower: sensing, PD control, PWM generation and motor driving all done in continuous-time analog hardware, with no firmware anywhere in the loop.",
    overview=[
      "Most line followers process an IR sensor array in software. This one doesn't: there's no microcontroller, no programmable logic, and no code anywhere on the robot. An 8-channel TCRT5000 infrared array feeds resistor-weighted summing amplifiers built from LM324 op-amps, which continuously compute a single error voltage representing the line's position, direction of deviation and magnitude, entirely in continuous time.",
      "That error voltage drives a hardware Proportional-Derivative controller (adjustable Kp and Kd set by trimpots rather than software constants) which reacts immediately with no ADC conversion, no sampling delay, and no loop-execution time. PWM for the motors is generated the same way: a Schmitt-trigger oscillator and analog integrator produce a stable triangular carrier, which a comparator mixes against the PD output to produce continuously variable, adjustable-frequency PWM. An L293D H-bridge then drives the two DC gear motors with independent left/right differential steering.",
      "My focus was the drive side of the loop: designing the Triangular Waveform Generator and the comparator-based PWM generation circuitry, then carrying that through to motor control implementation, hardware assembly/soldering and end-to-end system debugging. The full analog signal path (sensing, PD control, and PWM/motor drive) was laid out on a custom 4-layer PCB to keep the ground plane clean and EMI low, since a noisy analog front end is far more forgiving in software than it is when the 'processor' is a breadboard of op-amps.",
    ],
    features=[
      "Fully analog control loop — zero microcontrollers, zero firmware, zero digital logic",
      "8-channel TCRT5000 IR array with resistor-weighted analog error summation (LM324 op-amps)",
      "Hardware PD controller with adjustable proportional (Kp) and derivative (Kd) gain trimpots",
      "Analog triangular-wave PWM generator (Schmitt trigger + integrator + comparator) with adjustable frequency",
      "L293D H-bridge driving independent left/right differential steering with adjustable minimum wheel speed",
      "Custom 4-layer PCB with isolated analog/motor power rails and dedicated debugging switches",
    ],
    stack=["LM324 Op-Amps", "L293D Motor Driver", "TCRT5000 IR Sensors", "Altium Designer", "LTspice"],
    tags="embedded",
    gallery=[
      ("analog-line-follower-1.jpg", "The completed analog line follower"),
      ("analog-line-follower-2.jpg", "Assembled board — top-down view"),
      ("analog-line-follower-3.png", "Custom 4-layer PCB — routing layout"),
      ("analog-line-follower-4.png", "PCB 3D render — top view"),
      ("analog-line-follower-5.png", "PCB 3D render — bottom view"),
    ],
    youtube=[
      ("-q05K0lNBug", "Final Demo"),
    ],
  ),
  dict(
    slug="analog-motor-speed-controller",
    github="https://github.com/denethp/fully-analog-dc-motor-speed-controller",
    title="Fully Analog DC Motor Speed Controller",
    tag="Electronics Project",
    status="Completed",
    accent=False,
    dates="Feb 2026 – Jul 2026",
    role="Electronic Design, 1kHz PWM Generation, and Analog-Level Control Systems Design",
    team="Collaborative build",
    lede="A closed-loop DC motor speed controller with no microcontroller anywhere in the loop: encoder feedback, PID and PWM generation done entirely with op-amps and discrete power electronics.",
    overview=[
      "This project regulates DC motor speed in closed loop without a single digital component in the control path. Encoder pulses are converted to a proportional analog voltage by a custom frequency-to-voltage converter (an RC low-pass filter, peak detector and signal-conditioning stage), giving continuous real-time speed feedback with no ADC sampling anywhere in between.",
      "That feedback voltage is compared against a reference and run through a full analog PID controller built from TL072 op-amp stages implementing proportional, integral and derivative action directly in the analog domain. The PID output drives a custom analog PWM generator (a Schmitt-trigger oscillator, integrator and comparator producing a clean triangular carrier, followed by a precision rectifier and positive clipper to shape it into a clean 0–5V PWM signal), which finally switches an IRLZ44N logic-level MOSFET (with flyback diode and gate/pull-down protection) to drive the motor.",
      "My part of the loop was the PWM generation stage: designing the Schmitt-trigger oscillator, integrator and comparator chain, and getting the precision-rectifier output clean enough to reliably switch the MOSFET stage. Testing and tuning the whole loop entirely on hardware, with no software knob to fall back on, meant every gain, corner frequency and clipping threshold had to be nailed down through component selection and bench iteration.",
    ],
    features=[
      "Fully analog closed-loop speed control — no microcontroller, DSP or FPGA anywhere in the loop",
      "Custom frequency-to-voltage converter turning encoder pulses into continuous analog speed feedback",
      "Analog PID controller (P + I + D) built from TL072 op-amp stages",
      "Analog PWM generator: Schmitt-trigger oscillator, integrator, comparator, precision rectifier and clipper",
      "IRLZ44N MOSFET power driver stage with flyback protection for reliable motor switching",
    ],
    stack=["TL072 Op-Amps", "IRLZ44N MOSFET", "Frequency-to-Voltage Converter", "Analog PID"],
    tags="embedded",
    presentation=(
      "https://www.canva.com/design/DAHIBe1Ph3U/AgemTcLJaJtfteaBAiZ2Lg/view?utm_content=DAHIBe1Ph3U&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hecbe5c174b#1",
      "Neural Nexus — Analog Project (Sem 4)",
    ),
    gallery=[
      ("analog-motor-speed-controller-1.jpg", "Bench testing — laptop analysis alongside the breadboard circuit"),
      ("analog-motor-speed-controller-2.png", "The breadboard circuit — top-down view"),
    ],
  ),
  dict(
    slug="smart-flow-meter",
    github="https://github.com/denethp/Smart-Contact-Based-Flow-Meter",
    title="Smart Contact-based Flow Meter",
    tag="IoT Project",
    status="Completed",
    accent=False,
    dates="Feb 2025 – Jul 2025",
    role="Firmware Development & Full-Stack Development of the App",
    team="Collaborative build",
    lede="An IoT-enabled smart water flow meter: live flow monitoring, historical analytics and threshold alerts on a cross-platform mobile app, built around an affordable, locally manufacturable design.",
    overview=[
      "This engineering design project turns a basic paddle-wheel flow sensor into a fully connected IoT device. An ESP8266 reads flow rate and water temperature, drives a local OLED display for standalone operation, and streams live readings over Wi-Fi, with the whole board running off a rechargeable Li-ion cell through a TP4056 charging circuit and a custom PCB in a 3D-printed enclosure.",
      "On the software side, a React Native mobile app connects to the device in real time over WebSockets, backed by a Node.js server and SQLite database that store historical consumption data and enforce JWT-based authentication. Beyond live flow rate and temperature, the app surfaces total consumption, historical trends, multi-device management and configurable overflow/underflow alerts.",
      "I owned both ends of this stack: the ESP8266 firmware reading and conditioning the flow-sensor and temperature signals and pushing them out over Wi-Fi, and the React Native app (Android and iOS) that consumes that stream, renders it live, and handles authentication and historical analytics. Getting both sides talking reliably over WebSockets, with the app staying responsive and the firmware staying real-time, was the core engineering problem.",
    ],
    features=[
      "Real-time flow rate and water temperature monitoring via a paddle-wheel sensor and ESP8266",
      "Local OLED display for standalone, app-free operation",
      "React Native mobile app (Android & iOS) with live WebSocket monitoring and historical analytics",
      "JWT-authenticated Node.js backend with a SQLite data store for consumption history",
      "Configurable overflow/underflow notifications and multi-device management in-app",
      "Custom PCB and 3D-printed enclosure, powered by a rechargeable Li-ion cell via TP4056 charging",
    ],
    stack=["ESP8266", "Paddle Wheel Flow Sensor", "OLED Display", "React Native", "Node.js", "SQLite", "WebSockets", "JWT", "C/C++ (Arduino)", "JavaScript"],
    tags="embedded software",
    gallery=[
      ("smart-flow-meter-final.jpg", "The completed smart flow meter"),
      ("smart-flow-meter-internals.jpg", "Internal electronics and PCB"),
      ("smart-flow-meter-app-1.png", "The mobile app — welcome screen"),
      ("smart-flow-meter-app-2.png", "The mobile app — sign up"),
      ("smart-flow-meter-app-3.png", "The mobile app — sign in"),
      ("smart-flow-meter-app-4.png", "The mobile app — dashboard, active flow meters"),
      ("smart-flow-meter-app-5.png", "The mobile app — live monitoring view"),
      ("smart-flow-meter-app-6.png", "The mobile app — flow rate, temperature and total volume"),
      ("smart-flow-meter-app-7.png", "The mobile app — device info, limits and WiFi"),
      ("smart-flow-meter-app-8.png", "The mobile app — device settings"),
      ("smart-flow-meter-app-9.png", "The mobile app — historical analytics, last 30 seconds"),
      ("smart-flow-meter-app-10.png", "The mobile app — historical analytics, last 60 seconds"),
      ("smart-flow-meter-app-11.png", "The mobile app — historical analytics, last 5 minutes"),
      ("smart-flow-meter-app-12.png", "The mobile app — historical analytics, last 10 minutes"),
      ("smart-flow-meter-app-13.png", "The mobile app — about"),
      ("smart-flow-meter-app-14.png", "The mobile app — account and owned devices"),
      ("smart-flow-meter-app-15.png", "The mobile app — splash screen"),
    ],
    videos=[
      ("smart-flow-meter-demo.mp4", "Project Demonstration"),
    ],
  ),
  dict(
    slug="unilink",
    github="https://github.com/Zunehfu/unilink",
    title="UniLink (beta)",
    tag="Personal Project",
    status="Completed",
    accent=False,
    dates="Apr 2024 – Aug 2024",
    role="Full-stack Development",
    team="Individual (Personal Project)",
    lede="A social networking platform for university students and lecturers to share ideas, collaborate and communicate.",
    overview=[
      "UniLink was built to give university communities a dedicated space to share ideas and collaborate, separate from general-purpose social platforms. Students and lecturers can post, discuss and connect around academic and campus life.",
      "The backend runs on Express.js with a MySQL data store, while real-time features (notifications, live discussion updates) are handled over WebSockets. Authentication uses JWT to keep sessions stateless and scalable.",
      "This was one of my earliest full-stack projects, and it's where I first worked through the real-world tradeoffs of session management, real-time updates, and relational schema design at a 'real users' scale rather than a toy example."
    ],
    features=[
      "React front end with a component-driven UI for posts, profiles and discussions",
      "Express.js REST API backed by a MySQL relational schema",
      "Real-time updates and notifications via WebSockets",
      "JWT-based authentication for stateless, scalable sessions",
    ],
    stack=["JavaScript", "React", "Express.js", "WebSockets", "JWT", "HTML", "CSS", "MySQL"],
    tags="software",
    gallery=[
      ("unilink-1.jpg", "User profile — photos"),
      ("unilink-2.jpg", "User profile — mutual connections"),
      ("unilink-3.jpg", "User profile — contact info"),
      ("unilink-4.jpg", "Creating a post"),
      ("unilink-5.jpg", "Home feed — posts, links and mentions"),
      ("unilink-6.jpg", "Searching and networking with people"),
      ("unilink-7.jpg", "Messages"),
    ],
  ),
  dict(
    slug="samp-gaming-server",
    github="https://github.com/denethp/lggw-samp-server",
    title="SAMP Online Gaming Server",
    tag="Personal Project",
    status="Completed",
    accent=False,
    dates="2017 – 2019",
    role="Server Development & Scripting",
    team="Individual (Personal Project)",
    lede="A persistent multiplayer server for GTA: San Andreas, with custom gameplay mechanics and admin tooling, built and maintained solo through school.",
    overview=[
      "Long before university, this was the project that got me into programming seriously: an online multiplayer server for Grand Theft Auto: San Andreas built on the SA-MP (San Andreas Multiplayer) platform.",
      "Everything from custom gameplay mechanics to player management systems and administration tools was written in Pawn, SA-MP's scripting language, and run as a persistent, always-on server that real players connected to over several years.",
      "Maintaining a live multiplayer server, with real players, real bugs reported in real time, and real moderation problems, was an early, practical lesson in building and operating software that has to keep running, not just run once."
    ],
    features=[
      "Custom gameplay mechanics and game modes scripted in Pawn",
      "Player management and persistence systems for an always-on server",
      "In-game administration tools for moderation and server operations",
      "Maintained continuously over roughly two years with an active player base",
    ],
    stack=["Pawn"],
    tags="software",
    gallery=[
      ("samp-gaming-server-1.jpg", "Attacking a rival gang's turf during a live turf war"),
      ("samp-gaming-server-2.jpg", "The custom account, gang-membership and event-join systems firing in real time"),
      ("samp-gaming-server-3.jpg", "Sniping with the live scoreboard and gang tags visible"),
      ("samp-gaming-server-4.jpg", "The turf control map — gang-owned territory across Los Santos, color-coded per gang"),
      ("samp-gaming-server-5.jpg", "Lazer Gaming — the community website built alongside the server"),
      ("samp-gaming-server-6.jpg", "The site's About Us section describing the Gang Wars project"),
      ("samp-gaming-server-7.jpg", "The custom Gang System feature highlighted on the site"),
      ("samp-gaming-server-8.jpg", "VIP membership packages offered through the site"),
    ],
  ),
  dict(
    slug="intellicon-website",
    github="https://github.com/denethp/intellicon-24",
    title="Website for IntelliCon 2.0",
    tag="AIESEC / SLIIT",
    status="Completed",
    accent=False,
    dates="Apr 2024",
    role="Web Development",
    team="AIESEC, SLIIT",
    lede="The official registration and event site for IntelliCon 2.0, a coding competition organized by AIESEC at SLIIT, Sri Lanka.",
    overview=[
      "IntelliCon 2.0 needed a full event website (schedule, a CodeRun competition section, an FAQ, and a working registration flow) built and shipped ahead of the competition date. The front end runs an animated particle-network hero and scroll-triggered reveal animations across a Node.js/Express backend with Handlebars templating.",
      "Registration itself is a full account system rather than a static form: JWT-based authentication backs both a public registration flow and a separate admin login for managing entrants, with an SQLite database storing registration and event data behind it.",
      "Working to a hard external deadline for an organizer outside the university was good practice in scoping a small web project tightly: client, server and database all had to be functional and polished by a fixed competition date rather than an open-ended one."
    ],
    features=[
      "Animated particle-network hero and scroll-triggered section reveals",
      "Server-rendered pages using Express.js and Handlebars (hbs) templating",
      "JWT-authenticated registration flow with a separate admin login for managing entrants",
      "SQLite-backed storage for event and registration data",
      "Schedule, CodeRun competition and FAQ sections built for the live event",
    ],
    stack=["JavaScript", "Node.js", "Express.js", "Handlebars (hbs)", "JWT", "HTML", "CSS", "SQLite"],
    tags="software",
  ),
]

# The top-level `dates` field on a project is the single source of truth for its overall
# timeline (used on the index card and detail-page header). current_mouse.date is a distinct,
# shorter "generation" date (e.g. "Mar. 2026") shown alongside the other mouse generations on
# the family page, so it's set explicitly per mouse rather than derived from `dates` — only
# fall back to `dates` if a mouse dict doesn't set its own date.
for _p in projects:
    if _p.get("current_mouse") and "date" not in _p["current_mouse"]:
        _p["current_mouse"]["date"] = _p["dates"]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title} — Deneth Priyadarshana</title>
<meta name="description" content="{lede_attr}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22 fill=%22%2300e5c7%22>&#9670;</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>

<div class="bg-grid" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>

<a class="skip-link" href="#main">Skip to content</a>

<header class="nav proj-page-nav" id="nav">
  <div class="nav-inner container">
    <a href="../index.html#home" class="brand">
      <span class="brand-mark">DP</span><span class="brand-dot">.</span>
    </a>
    <a href="../index.html#projects" class="btn btn-outline">&larr; All Projects</a>
  </div>
</header>

<main id="main">
  <section class="proj-hero container">
    <div class="proj-hero-top">
      <div class="proj-meta-row">
        <span class="proj-badge{accent_class}">{status}</span>
        <span class="proj-badge">{dates}</span>
      </div>
      {github_block}
    </div>
    <h1 class="proj-title">{title}</h1>
    <p class="proj-lede">{lede}</p>

    {media_block}
  </section>

  <section class="section" style="padding-top:0; border-top:none;">
    <div class="container proj-body">
      <div class="proj-main">
        <h2>Overview</h2>
        {overview_html}

        <h2>Key Features</h2>
        <ul class="feature-list">
          {features_html}
        </ul>

        {video_block}
      </div>

      <aside class="proj-side">
        <div class="side-card">
          <h4>Project Info</h4>
          <div class="side-row"><span>Status</span><span>{status}</span></div>
          <div class="side-row"><span>Timeline</span><span>{dates}</span></div>
          <div class="side-row"><span>Role</span><span>{role}</span></div>
        </div>
        <div class="side-card">
          <h4>Tech Stack</h4>
          <div class="chip-row">{stack_html}</div>
        </div>
        <div class="side-card side-cta">
          <p class="cv-note">CV available upon request</p>
          <a href="https://wa.me/94721432218?text=Hi%2C%20I%27d%20like%20to%20request%20your%20CV" target="_blank" rel="noopener" class="btn btn-primary cv-request-btn" data-contact-url="../index.html#contact">Request CV</a>
          <a href="../index.html#contact" class="btn btn-outline">Get in Touch</a>
        </div>
      </aside>
    </div>

    {generations_block}

    <div class="container proj-nav">
      <a href="{prev_slug}.html" class="proj-nav-link prev">
        <span class="proj-nav-label">&larr; Previous</span>
        <span class="proj-nav-title">{prev_title}</span>
      </a>
      <a href="{next_slug}.html" class="proj-nav-link next">
        <span class="proj-nav-label">Next &rarr;</span>
        <span class="proj-nav-title">{next_title}</span>
      </a>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container footer-inner">
    <p>&copy; <span id="year"></span> Deneth Priyadarshana. Built with HTML, CSS &amp; JS.</p>
    <a href="../index.html#home" class="back-top">Back to top &uarr;</a>
  </div>
</footer>

<script src="../assets/js/main.js"></script>
</body>
</html>
"""

n = len(projects)
for i, p in enumerate(projects):
    prev_p = projects[(i - 1) % n]
    next_p = projects[(i + 1) % n]

    overview_html = "\n        ".join(f"<p>{html.escape(para)}</p>" for para in p["overview"])
    features_html = "\n          ".join(
        f'<li><span class="f-num">{j+1:02d}</span><span>{html.escape(f)}</span></li>'
        for j, f in enumerate(p["features"])
    )
    stack_html = "".join(f"<span>{html.escape(t)}</span>" for t in p["stack"])

    presentation = p.get("presentation")
    gallery = p.get("gallery")
    if presentation and gallery:
        # Presentation link shown first (the default view), with the actual
        # photos available right after it as additional thumbnails — lets a
        # project lead with slides while still surfacing real photos.
        pres_url, pres_label = presentation
        main_file, main_alt = gallery[0]
        thumbs = ['''<button class="gallery-thumb presentation-thumb is-active" data-type="presentation" aria-label="View presentation">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
        </button>''']
        thumbs += [
            f'''<button class="gallery-thumb" data-type="photo" data-src="../assets/img/projects/{p['slug']}/{fname}" data-alt="{html.escape(alt)}" aria-label="View photo {j+1}">
          <img src="../assets/img/projects/{p['slug']}/{fname}" alt="{html.escape(alt)}" loading="lazy">
        </button>'''
            for j, (fname, alt) in enumerate(gallery)
        ]
        thumbs_html = "\n        ".join(thumbs)
        media_block = f'''<div class="proj-media proj-gallery">
      <a class="proj-presentation is-active" id="presentationMedia" href="{pres_url}" target="_blank" rel="noopener noreferrer">
        <div class="presentation-glow" aria-hidden="true"></div>
        <div class="presentation-content">
          <span class="presentation-icon">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
          </span>
          <h3>{html.escape(pres_label)}</h3>
          <span class="presentation-cta">View Presentation
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M7 17L17 7M7 7h10v10"/></svg>
          </span>
        </div>
      </a>
      <img id="galleryMain" src="../assets/img/projects/{p['slug']}/{main_file}" alt="{html.escape(main_alt)}" style="display:none">
    </div>
    <div class="gallery-thumbs">
        {thumbs_html}
    </div>'''
    elif presentation:
        pres_url, pres_label = presentation
        media_block = f'''<a class="proj-media proj-presentation" href="{pres_url}" target="_blank" rel="noopener noreferrer">
      <div class="presentation-glow" aria-hidden="true"></div>
      <div class="presentation-content">
        <span class="presentation-icon">
          <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
        </span>
        <h3>{html.escape(pres_label)}</h3>
        <span class="presentation-cta">View Presentation
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M7 17L17 7M7 7h10v10"/></svg>
        </span>
      </div>
    </a>'''
    elif gallery:
        main_file, main_alt = gallery[0]
        thumbs_html = "\n        ".join(
            f'''<button class="gallery-thumb{' is-active' if j == 0 else ''}" data-src="../assets/img/projects/{p['slug']}/{fname}" data-alt="{html.escape(alt)}" aria-label="View photo {j+1}">
          <img src="../assets/img/projects/{p['slug']}/{fname}" alt="{html.escape(alt)}" loading="lazy">
        </button>'''
            for j, (fname, alt) in enumerate(gallery)
        )
        media_block = f'''<div class="proj-media proj-gallery">
      <img id="galleryMain" src="../assets/img/projects/{p['slug']}/{main_file}" alt="{html.escape(main_alt)}">
    </div>
    <div class="gallery-thumbs">
        {thumbs_html}
    </div>'''
    elif os.path.exists(os.path.join(SITE, "assets/img/projects", f"{p['slug']}.jpg")):
        media_block = f'''<div class="proj-media">
      <img src="../assets/img/projects/{p['slug']}.jpg" alt="{html.escape(p['title'])}" loading="lazy">
    </div>'''
    else:
        media_block = f'''<div class="proj-media">
      <div class="media-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8.5" cy="8.5" r="1.6"/><path d="M21 15l-5-5-9 9"/></svg>
        <span>Image coming soon</span>
      </div>
    </div>'''

    videos = p.get("videos") or []
    youtube = p.get("youtube") or []
    if videos or youtube:
        def _vcard(fname, label):
            fpath = os.path.join(SITE, "assets/img/projects", p["slug"], fname)
            missing = not os.path.exists(fpath)
            ratio = video_aspect_ratio(fpath)
            src = f"../assets/img/projects/{p['slug']}/{fname}"
            return f'''<div class="video-card{'' if not missing else ' is-missing'}" style="aspect-ratio:{ratio}" data-video-src="{src}" data-video-label="{html.escape(label)}">
          <video controls preload="metadata" poster="">
            <source src="{src}" type="video/mp4">
          </video>
          <button type="button" class="video-expand-btn" aria-label="Expand video">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4M15 3h4a2 2 0 0 1 2 2v4M9 21H5a2 2 0 0 1-2-2v-4M15 21h4a2 2 0 0 0 2-2v-4"/></svg>
          </button>
          <div class="video-placeholder">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor" stroke="none"/></svg>
            <span>Video coming soon</span>
          </div>
          <p class="video-label">{html.escape(label)}</p>
        </div>'''
        def _ytcard(vid, label):
            thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
            return f'''<div class="video-card yt-card" style="aspect-ratio:16/9" data-yt-id="{vid}" data-video-label="{html.escape(label)}">
          <img src="{thumb}" alt="{html.escape(label)}" loading="lazy">
          <span class="yt-badge">YouTube</span>
          <button type="button" class="yt-play-btn" aria-label="Play on YouTube" tabindex="-1">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
          </button>
          <p class="video-label">{html.escape(label)}</p>
        </div>'''
        cards_html = "\n        ".join(
            [_vcard(fname, label) for fname, label in videos] +
            [_ytcard(vid, label) for vid, label in youtube]
        )
        video_block = f'''<h2>Demos</h2>
        <div class="video-grid">
        {cards_html}
        </div>'''
    else:
        video_block = ""

    older_mice = p.get("older_mice")
    if older_mice:
        cards_html = "\n        ".join(
            mouse_card_html(
                label=g["label"], date=g["date"], tagline=g["tagline"], meta=g["meta"],
                img_src=f"../assets/img/projects/{p['slug']}/{g['images'][0][0]}",
                href=f"mice/{g['gid']}.html",
            )
            for g in older_mice
        )
        generations_block = f'''<div class="container family-section">
      <h2>Older Micromice</h2>
      <p class="gen-intro">Blaze v2 (above) is the current mouse. Before it came four earlier builds. Full write-ups for all of them live in the
        <a href="https://github.com/denethp/micromouse-showcase" target="_blank" rel="noopener">micromouse-showcase</a> repo.</p>
      <div class="mouse-card-grid">
        {cards_html}
      </div>
    </div>'''
    else:
        generations_block = ""

    github_url = p.get("github")
    if github_url:
        github_block = f'''<a class="btn proj-github-btn" href="{html.escape(github_url)}" target="_blank" rel="noopener">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
        View GitHub Repository
      </a>'''
    else:
        github_block = ""

    out = TEMPLATE.format(
        title=html.escape(p["title"]),
        lede=html.escape(p["lede"]),
        lede_attr=html.escape(p["lede"]),
        slug=p["slug"],
        tag=html.escape(p["tag"]),
        status=html.escape(p["status"]),
        dates=html.escape(p["dates"]),
        role=html.escape(p["role"]),
        accent_class=" is-accent" if p["accent"] else "",
        overview_html=overview_html,
        features_html=features_html,
        stack_html=stack_html,
        media_block=media_block,
        video_block=video_block,
        generations_block=generations_block,
        github_block=github_block,
        prev_slug=prev_p["slug"],
        prev_title=html.escape(prev_p["title"]),
        next_slug=next_p["slug"],
        next_title=html.escape(next_p["title"]),
    )
    with open(os.path.join(PROJ_DIR, f"{p['slug']}.html"), "w") as f:
        f.write(out)

MOUSE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{label} — {project_title} — Deneth Priyadarshana</title>
<meta name="description" content="{tagline_attr}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22 fill=%22%2300e5c7%22>&#9670;</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../assets/css/style.css">
</head>
<body>

<div class="bg-grid" aria-hidden="true"></div>
<div class="noise" aria-hidden="true"></div>

<a class="skip-link" href="#main">Skip to content</a>

<header class="nav proj-page-nav" id="nav">
  <div class="nav-inner container">
    <a href="../../index.html#home" class="brand">
      <span class="brand-mark">DP</span><span class="brand-dot">.</span>
    </a>
    <a href="../{project_slug}.html" class="btn btn-outline">&larr; {project_title}</a>
  </div>
</header>

<main id="main">
  <section class="proj-hero container">
    <div class="proj-hero-top">
      <div class="proj-meta-row">
        <span class="proj-badge is-accent">{date}</span>
        <span class="proj-badge">{meta}</span>
      </div>
    </div>
    <h1 class="proj-title">{label}</h1>
    <p class="proj-lede">{tagline}, an earlier generation of the <a href="../{project_slug}.html">{project_title}</a>.</p>

    {media_block}
  </section>

  <section class="section" style="padding-top:0; border-top:none;">
    <div class="container proj-body">
      <div class="proj-main">
        <h2>Overview</h2>
        <p>{blurb}</p>

        {mouse_video_block}
      </div>

      <aside class="proj-side">
        <div class="side-card">
          <h4>Mouse Info</h4>
          <div class="side-row"><span>Built</span><span>{date}</span></div>
          <div class="side-row"><span>Platform</span><span>{meta}</span></div>
          <div class="side-row"><span>Role</span><span>{role}</span></div>
          <div class="side-row"><span>Part of</span><span><a href="../{project_slug}.html">{project_title}</a></span></div>
        </div>
        <div class="side-card side-cta">
          <p class="cv-note">CV available upon request</p>
          <a href="https://wa.me/94721432218?text=Hi%2C%20I%27d%20like%20to%20request%20your%20CV" target="_blank" rel="noopener" class="btn btn-primary cv-request-btn" data-contact-url="../../index.html#contact">Request CV</a>
          <a href="../../index.html#contact" class="btn btn-outline">Get in Touch</a>
        </div>
      </aside>
    </div>

    <div class="container family-section">
      <h2>All Micromice</h2>
      <p class="gen-intro">Every generation of this platform, all built for the same 16&times;16 maze.</p>
      <div class="mouse-card-grid">
        {sibling_cards_html}
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container footer-inner">
    <p>&copy; <span id="year"></span> Deneth Priyadarshana. Built with HTML, CSS &amp; JS.</p>
    <a href="../../index.html#home" class="back-top">Back to top &uarr;</a>
  </div>
</footer>

<script src="../../assets/js/main.js"></script>
</body>
</html>
"""

for p in projects:
    older_mice = p.get("older_mice")
    current_mouse = p.get("current_mouse")
    if not older_mice or not current_mouse:
        continue

    all_mice = [current_mouse] + older_mice

    for g in older_mice:
        gallery_imgs = g["images"]
        if len(gallery_imgs) > 1:
            main_file, main_alt = gallery_imgs[0]
            thumbs_html = "\n        ".join(
                f'''<button class="gallery-thumb{' is-active' if j == 0 else ''}" data-src="../../assets/img/projects/{p['slug']}/{fname}" data-alt="{html.escape(alt)}" aria-label="View photo {j+1}">
          <img src="../../assets/img/projects/{p['slug']}/{fname}" alt="{html.escape(alt)}" loading="lazy">
        </button>'''
                for j, (fname, alt) in enumerate(gallery_imgs)
            )
            media_block = f'''<div class="proj-media proj-gallery">
      <img id="galleryMain" src="../../assets/img/projects/{p['slug']}/{main_file}" alt="{html.escape(main_alt)}">
    </div>
    <div class="gallery-thumbs">
        {thumbs_html}
    </div>'''
        else:
            fname, alt = gallery_imgs[0]
            media_block = f'''<div class="proj-media">
      <img src="../../assets/img/projects/{p['slug']}/{fname}" alt="{html.escape(alt)}" loading="lazy">
    </div>'''

        siblings = [m for m in all_mice if m["gid"] != g["gid"]]
        sibling_cards_html = "\n        ".join(
            mouse_card_html(
                label=m["label"], date=m["date"], tagline=m["tagline"], meta=m["meta"],
                img_src=f"../../assets/img/projects/{p['slug']}/{(m['images'][0][0] if 'images' in m else m['thumb'])}",
                href=(f"{m['gid']}.html" if m["gid"] != current_mouse["gid"] else f"../{p['slug']}.html"),
            )
            for m in siblings
        )

        mouse_videos = g.get("videos")
        if mouse_videos:
            def _mvcard(fname, label):
                fpath = os.path.join(SITE, "assets/img/projects", p["slug"], fname)
                missing = not os.path.exists(fpath)
                ratio = video_aspect_ratio(fpath)
                src = f"../../assets/img/projects/{p['slug']}/{fname}"
                return f'''<div class="video-card{'' if not missing else ' is-missing'}" style="aspect-ratio:{ratio}" data-video-src="{src}" data-video-label="{html.escape(label)}">
          <video controls preload="metadata" poster="">
            <source src="{src}" type="video/mp4">
          </video>
          <button type="button" class="video-expand-btn" aria-label="Expand video">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 3H5a2 2 0 0 0-2 2v4M15 3h4a2 2 0 0 1 2 2v4M9 21H5a2 2 0 0 1-2-2v-4M15 21h4a2 2 0 0 0 2-2v-4"/></svg>
          </button>
          <div class="video-placeholder">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor" stroke="none"/></svg>
            <span>Video coming soon</span>
          </div>
          <p class="video-label">{html.escape(label)}</p>
        </div>'''
            mv_cards_html = "\n        ".join(_mvcard(fname, label) for fname, label in mouse_videos)
            mouse_video_block = f'''<h3>Demos</h3>
        <div class="video-grid">
        {mv_cards_html}
        </div>'''
        else:
            mouse_video_block = ""

        out = MOUSE_TEMPLATE.format(
            label=html.escape(g["label"]),
            project_title=html.escape(p["title"]),
            project_slug=p["slug"],
            tagline_attr=html.escape(g["tagline"]),
            date=html.escape(g["date"]),
            meta=html.escape(g["meta"]),
            tagline=html.escape(g["tagline"]),
            role=html.escape(g.get("role", "")),
            blurb=html.escape(g["blurb"]),
            media_block=media_block,
            sibling_cards_html=sibling_cards_html,
            mouse_video_block=mouse_video_block,
        )
        with open(os.path.join(MICE_DIR, f"{g['gid']}.html"), "w") as f:
            f.write(out)

print(f"Generated {n} project pages.")

# also dump a JS-readable mapping for index.html linking (slug per card order)
import json
with open("/home/claude/site/assets/js/_project_slugs.json", "w") as f:
    json.dump([{"title": p["title"], "slug": p["slug"]} for p in projects], f, indent=2)
