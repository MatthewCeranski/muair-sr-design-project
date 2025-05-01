# Visual Unit: Assembly Instructions

## 1. 3D Print the Visualization Housing

Download the STL files and 3D models [here](muair-sr-design-project/visualization-unit/stl).

These parts are not designed to be structural or waterproof on their own. Therefore, any common filament material can be used. The MUAIR team recommends PETG due to its UV resistance and relatively low cost.

If you are new to 3D printing, search for a tutorial based on your specific printer and slicing software. The MUAIR team used Bambu Studio with the preset profile for Bambu Labs PETG Basic.

- Slice and print these models at any point in your build process.
- Because the parts are not structural, you can experiment with slicing parameters to suit your needs.

### Visualization Housing Modification

There is a known clearance issue with the SD card slot on the Raspberry Pi. To resolve this, use a Dremel or other rotary tool to hollow out a **0.5 inch by 0.5 inch** square that is at least **0.15 inches deep** in the corresponding wall of the housing.

Refer to the reference image below for proper placement and dimensions.

*(Insert or link to reference image here)*

---

## 2. Attach Smokestacks to the Visualization Housing

The visualization housing includes decorative smokestacks that need to be attached to the top of the unit.

To secure the smokestacks:

1. Mix a two-part clear epoxy on a sheet of cardboard.
2. Apply small dabs of the mixture to the ends of the smokestacks using toothpicks or Q-Tips.
3. Carefully insert the smokestacks into position, centered around the pre-cut holes on the top of the assembly.

Tip: Wear latex gloves to avoid getting epoxy on your hands. This also makes it easier to wipe off any excess.

Allow the epoxy to cure according to the manufacturer's instructions.

---

## 3. Paint the Visualization Housing (Optional)

Painting is optional but recommended for a more engaging visual experience.

The MUAIR team painted the visualization unit to reflect a realistic factory aesthetic. The more visually compelling the unit is, the more likely it is to spark curiosity and prompt reflection about air quality.

Feel free to be creative—make the visualization stand out and invite interpretation.

---

## 4. Set Up the Visualization Raspberry Pi

Using Raspberry Pi Imager, follow the instructions [here](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system) to install an operating system and get your raspberry pi up and running. We recommend installing the latest version of Raspberry Pi OS. 

Following setup, you will need to clone this repository to the raspberry pi. In the terminal, copy this code: 
```
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

This will create a copy of the most up to date version of this project. Finally, it is time to set up the raspberry pi to run the MUAIR project automatically. A setup script was created that will download the latest version of python, install the necessary libraries, organize relevant folders, and automate the program. Copy this code into the terminal:
```
bash visual_setup.sh
```

---

## 5. Assemble the Visualization Circuit

Follow the wire diagram provided below. These connections can be soldered for a more permanent unit, or if flexibility is desired these connections can be made on a breadboard. At this point, test the unit to ensure all connections were made correctly. 

---

## 6. Install the Visualization Circuit

Install the assembled components into the visualization housing. The screen is secured with two screws at the bottom of the rear cutout. The fans are tucked into mounts below each smokestack opening. The raspberry pi is set in place on the standouts provided. Attach streamers to the protrusions in each smokestack to give the effect of smoke while the fans are turned on.
