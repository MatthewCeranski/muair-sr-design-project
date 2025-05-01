# Sensor Unit: Assembly Instructions

## 1. 3D Print the Sensor Housing

**Download STL Files**: [Click here to access the 3D models and STL files](sensor-unit/stl/sensor_housing.stl)

These parts are **not designed to be structural or waterproof on their own**, so you can print them with most common filament materials. The MUAIR team recommends **PETG** for its UV resistance and low cost.

If you are new to 3D printing, we suggest searching for tutorials tailored to your specific printer software. The MUAIR team used **Bambu Studio** with the preset profile for **Bambu Labs PETG Basic**.

- You can slice and print the parts at any time during the build process.
- Feel free to modify the model parameters as needed.

>**Note**: In their current state, both the sensor housing and visualization housing **require modification** to fit >internal components.

### Sensor Modification Notice

There is a **known clearance issue** with the sensor module near the screen side of the housing. Specifically, the **inner holding post blocks installation**. Use a Dremel or rotary tool to **remove the post**, leaving approximately **0.25"** remaining to retain stability.

---

## 2. Attach Plexiglass Viewport to Sensor Housing

The sensor housing requires a **2 ¾” x 1” acrylic cover** to be installed over the LCD viewport **before waterproofing**.

### Buying Option:
You can purchase a pre-cut piece of clear acrylic in that size.

### DIY Cutting Option:
1. Use a ruler and fine-tipped Sharpie to mark a rectangle on the plastic cover of a larger acrylic sheet.
2. Cut carefully using a razor blade, acrylic scoring knife, or rotary tool.
3. You can always trim down the piece if it's slightly oversized.
4. **Exercise caution** when cutting.

### Attaching the Cover:
- Mix a **two-part clear epoxy** on cardboard.
- Use toothpicks or Q-tips to apply small dabs of epoxy to the recessed edge of the viewport.
- **Remove the protective plastic film** from the acrylic before applying epoxy.
- Tip: Wear **latex gloves** to avoid mess and for easier cleanup.

 **Cure Time**: Follow the epoxy manufacturer's instructions for drying and curing.

---

## 3. Waterproof the Sensor Housing

To protect internal components, the sensor housing must be waterproofed.

- Use a **sprayable clear rubber coating**.
- **Tape off** the sensor housing as shown in the assembly guide.
- Spray according to the manufacturer’s instructions.

> **DO NOT spray the bottom of the sensor housing.**  
> This area includes vents critical to sensor function — blocking them will reduce accuracy.
> Spray all **other sides** of the housing.

---

## 4. Set Up Sensor Raspberry Pi

Using Raspberry Pi Imager, follow the instructions [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system) to install an operating system and get your raspberry pi up and running. We recommend installing the latest version of Raspberry Pi OS. 

Following setup, you will need to clone this repository to the raspberry pi. In the terminal, copy this code: 
```
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

This will create a copy of the most up to date version of this project. Finally, it is time to set up the raspberry pi to run the MUAIR project automatically. A setup script was created that will download the latest version of python, install the necessary libraries, organize relevant folders, and automate the program. Copy this code into the terminal:
```
bash sensor_setup.sh
```

---

## 5. Assemble the Sensor Circuit

Follow the wire diagram provided below. These connections can be soldered for a more permanent unit, or if flexibility is desired these connections can be made on a breadboard. At this point, test the unit to ensure all connections were made correctly. 

---

## 6. Install the Assembled Sensor Circuit into the Housing

Place each component into the sensor housing. The two air quality sensors will be on the bottom with the fans facing downwards. The LCD screen slides into the slot near the plexiglass viewing window. The breadboard sits on the middle shelf. The raspberry pi fits on the top shelf. Use the wire run cutouts on the back of each shelf to prevent shifting of components. 
