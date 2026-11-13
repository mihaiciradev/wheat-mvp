# DJI Mavic 3M

The aircraft described as a Mavic 3 enterprise with a spectral camera is the **DJI Mavic 3 Multispectral (Mavic 3M)**. The EU, C2-certified version is sold as **Mavic 3M EU** (EASA model M3M-EU). “MEU” matches that name. It is not the Mavic 3E, which has no multispectral cameras.

Confirmed from DJI’s Mavic 3M manual:

- One 20 MP RGB camera, 4/3 sensor, mechanical shutter, about 24 mm equivalent, photos up to 5280×3956.
- Four 5 MP multispectral cameras, about 25 mm equivalent: green 560±16 nm, red 650±16 nm, red edge 730±16 nm, near infrared 860±26 nm.
- A sunlight sensor on the aircraft records irradiance so later processing can compensate for light.
- Each capture can be one RGB JPEG plus four single-band TIFFs. RGB-only interval can be 0.7 s. RGB plus multispectral interval is about 2 s.

Fenia does not depend on DJI software. These programs are for capture and map-making. Exported images are what our pipeline should read.

## Programs

| Program | Role |
| --- | --- |
| **DJI Pilot 2** | Required. It is the flight app on the enterprise controller. Plan the grid, fly, and save the photos. It can show live NDVI, GNDVI, and NDRE. It does not build the field map. |
| **DJI Terra Agriculture** | The DJI program that turns a flight into a map. Import the RGB set and the four bands (five files per shot). It makes a 2D orthophoto and a surface model, plus index maps such as NDVI and NDRE. A Windows PC with 32 GB of RAM and an NVIDIA GPU is the published requirement. The agriculture license is the one that includes this. DJI’s store has listed the online agriculture license around 300 USD per year for up to three devices; confirm the current EU price before buying. |
| **Radiometric calibration panel** | Optional, and only useful with Terra’s radiometric correction. Use it when the output must be reflectance, or when flights on different days must be compared. Take panel photos with the Mavic 3M and enter the panel’s known reflectance. Skip it for a first look at one flight. |
| **RTK** | Optional hardware and a correction source, not a separate analysis program. Use it when the same plots must line up across dates. A first flight can be done without it. |
| **DJI FlightHub 2** | Not for this aircraft. DJI’s current supported-device list includes the Mavic 3 Enterprise series and excludes the Mavic 3 Multispectral. Do not buy it to fly or map the Mavic 3M. |
| **DJI Modify** | Optional editor for 3D models. Not used for plot measurements. |
| **PIX4Dfields or another photogrammetry tool** | Optional substitute for Terra if someone already has a license. Pix4D publishes a Mavic 3M workflow. Our own code does not stitch a flight into a map. |

## What public photos can and cannot tell us

These are real Mavic 3M files. They are not our microplots, and they are not a wheat or sunflower establishment set.

- Pix4D winter-barley example, flown at 90 m with RTK: [pix4d.com/dji-mavic-3-multispectral-dataset](https://www.pix4d.com/dji-mavic-3-multispectral-dataset). 309 RGB images and 1,236 multispectral images, plus calibration-target photos. Useful as a processing example.
- Raw olive flights, CC BY 4.0: [doi.org/10.5281/zenodo.12943015](https://doi.org/10.5281/zenodo.12943015). Each shot is `*_D.JPG` plus `*_MS_G.TIF`, `*_MS_R.TIF`, `*_MS_RE.TIF`, and `*_MS_NIR.TIF`. One flight is several gigabytes.
- Raw vineyard flights, CC BY 4.0: [doi.org/10.5281/zenodo.14604638](https://doi.org/10.5281/zenodo.14604638). About 22 GB. The deposit reports about 1.4 cm RGB and 4.8 cm multispectral on that day.

The full archives were not downloaded. A 2 m plot is a poor fit to a 90 m survey photo. From the published sensor size and field of view, a rough scale is about 2.5 cm per RGB pixel at 90 m, and about 4 cm per multispectral pixel. The same 2 m plot is then only about 80 RGB pixels across. That can support a coarse cover estimate. It is a weak basis for seedling gaps or plant counts. A lower pass, on the order of 30 m, is the flight to try when the weather allows, with the whole plot in frame and the plot edges visible.

Do not commit those downloaded flights. Keep them outside Git if someone processes them locally.
