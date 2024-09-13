# Distribution Plotting Tool, DHH 2024

A plotting tool for the argument class dataset created during the [Digital Humanities Hackathon 2024](https://www.helsinki.fi/en/digital-humanities/helsinki-digital-humanities-hackathon-2024-dhh24) by the Parliament group.

### Echoes of the Chambers: Studying Democracy through Parliamentary Speeches

The hackathon team built a model to classify parliamentary speeches based on how democracy is used as an argument. The four categories, developed by humanities experts, are: democracy under threat, democracy as a value, democracy as leverage, and other. More information about the model and the code used to build it can be found [here](https://github.com/kferraga/ParliamentHackathon2024).

For more information about the hackathon and pictures from the event, visit the [Hackathon website](https://www.helsinki.fi/en/digital-humanities/helsinki-digital-humanities-hackathon-2024-dhh24) and follow the event on [Instagram](https://www.instagram.com/dhhackathon/).

## Distribution Tool

The terminal-based distribution tool is used to visualize some of the results from the argument class dataset.

### Installation and Packages

To use the tool, clone the repository to your computer. The required packages are listed below:

* [Python 3](https://www.python.org/downloads/)
* [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
* [NumPy](https://numpy.org/install/)
* [Matplotlib](https://matplotlib.org/stable/install/index.html)


### User guide

The program has multiple options for visualization. 

Start the program with the command:  

```
python3 init.py
```


The commands can be listed with the option "c".  

![options](documentation/commands.png)

The programs stops with the "quit" command.  

### Example figures

![gb](figures/gb_lc.png)
![gender](figures/gender_dist.png)
![pie](figures/gb_pie_chart.png)