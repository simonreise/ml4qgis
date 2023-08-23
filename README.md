# ML4QGIS
---
ML4QGIS is a QGIS plugin that provides a GUI to [Remote Sensing Processor](https://github.com/simonreise/remote-sensing-processor) python library.

ML4QGIS provides several data preprocessing and machine learning algorythms for image segmentation and classification. 

Plugin requires Python, Conda or Docker to run. Nvidia GPU is recommended if you are going to use neural networks.

## Install

Download or clone this repository to QGIS plugins directory. You can open plugins directory by `Settings -> User profiles -> Open active profile folder` and then navigating to `python/plugins`. Then ML4QGIS will appear in processing toolbox.

ML4QGIS does not use QGIS python installation, it requires custom environment with all dependencies installed. You can choose Docker, Conda or Python venv backend. To configure backend you need to run respective tool in Setup category in toolbox. Every tool have user guide where all additional installation steps are described.

Running ML4QGIS tools sometimes require lots of RAM and Docker is not always allocate enough memory, so we recommend to use Conda or Python venv. We also recommend to have a large swap file.

## Usage

Every tool have user guide where all parameters are described. Also you can read [RSP documentation](https://remote-sensing-processor.readthedocs.io/) for additional details.

## License

ML4QGIS is distributed under the same license as Remote Sensing Processor.
