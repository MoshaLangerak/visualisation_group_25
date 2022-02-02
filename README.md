# JBI100-Visualisation-Group-25

## About this app

Our project code for the JBI100 visualization project.

## Requirements

* Python 3 (add it to your path (system variables) to make sure you can access it from the command prompt)
* Git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* Data folder (since this cannot be saved on GitHub) (https://drive.google.com/drive/folders/144wEfkkN4OJ6icSgAEAxIxfLvg8Kk1cY?usp=sharing)

## How to run this app
We suggest you to create a virtual environment for running this app with Python 3. Clone this repository 
and open your terminal/command prompt in the root folder.

Open the command prompt cd into the folder where you want to save the files and run the following commands. To get the HTTPS link, press the clone button in the right top corner and then copy the link under "Clone with HTTPS". 

```
> git clone <HTTPS link>
> cd <folder name on your computer>
> python -m venv venv
```
If python is not recognized use python3 instead

In Windows: 

```
> venv\Scripts\activate

```
In Unix (macOS or Linux) system:

```
> source venv/bin/activate

```

Move the data downloaded to the data folder with path ~/visualisation_group_25/Data

Install all required packages by running:
```
> pip install -r requirements.txt
```

Run this app locally with:
```
> python app.py
```
You will get a http link, open this in your browser to see the results. Now you can view the dashboard.

## Resources

* [Dash](https://dash.plot.ly/)
* [Road Safety Data](https://data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data)
* [Population Data](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland)