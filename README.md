# Homeowners and Neighborhoods

## Exercise
Pearl Certification benefits homeowners along many different vectors. For purposes of this exercise, we'll call those energy efficiency **E**, water **W**, and resilience **R**. Various home builders are currently building new neighborhoods. Each neighborhood **(N)** scores differently across the different Pearl vectors **(E,W,R)**. For example, Belmont Acres **(N1)** has lots of solar, and great air sealing meaning it's **"E"** score is **10**, but the faucets are just up to code giving it a **"W"** score of **1**. It's resilience is typical for a new Pearl Certified home, so it's **"R"** score is **5**.

Discerning home buyers **(H)** are moving to Charlottesville. Home buyers have fixed goals for each of Energy, Water and Resilience. A home buyer's fit for a neighborhood is calculated by the dot product of the home buyer's goals and the neighborhood scores. Home buyers have a sense of Charlottesville, so have expressed preferences for which neighborhoods they may want to live in.

Your task is to write code to place home buyers in neighborhoods such that once they have moved to Charlottesville, no home buyer could subsequently move to a neighborhood they prefer more and be a better fit for it than any home buyer already in that neighborhood. Further so that no builder is overwhelmed, the number of home buyers should be evenly distributed among the available neighborhoods. (You may assume that the number of home buyers modulo the number of neighborhoods is zero(0).)

You will read your input from a file, and write your output to a file. The input file will have one item (home buyer or neighborhood) per line.

Neighborhood lines start with **'N'**. Neighborhood lines contain the scores of the characteristics of the neighborhood in **'Key:Value'** form. So, Belmont Acres might show up in the input file as:

```N N1 E:10 W:1 R:5```

Home buyer lines start with **'H'**. Home buyer lines contain the goals of the home buyer coded the same as for neighborhood. Home buyer lines also contain neighborhood preferences separated by a 'greater than' symbol indicating that the neighborhood to the left is more preferred than the one to the right. So "AC Capehart" is a high-goal home buyer that prefers Belmont Acres and might show up like this:

```H H9 E:10 W:6 R:8 N1>N2>N3```

The output for your code will be a file with each neighborhood filled with home buyers and the score for that home buyer in that neighborhood. So code in which AC Capehart **(H9)** was placed with other home buyers **(H2 and H4)** in Belmont Acres **(N1)** would show up like this: 

```N1: H9(146) H2(128) H4(122)```

Below is sample input and the expected output from that input:

### Input:
```
N N0 E:7 W:7 R:10
N N1 E:2 W:1 R:1
N N2 E:7 W:6 R:4

H H0 E:3 W:9 R:2 N2>N0>N1
H H1 E:4 W:3 R:7 N0>N2>N1
H H2 E:4 W:0 R:10 N0>N2>N1
H H3 E:10 W:3 R:8 N2>N0>N1
H H4 E:6 W:10 R:1 N0>N2>N1
H H5 E:6 W:7 R:7 N0>N2>N1
H H6 E:8 W:6 R:9 N2>N1>N0
H H7 E:7 W:1 R:5 N2>N1>N0
H H8 E:8 W:2 R:3 N1>N0>N2
H H9 E:10 W:2 R:1 N1>N2>N0
H H10 E:6 W:4 R:5 N0>N2>N1
H H11 E:8 W:4 R:7 N0>N1>N2
```
### Valid Output:
```
N0: H5(161) H11(154) H2(128) H4(122)
N1: H9(23) H8(21) H7(20) H1(18)
N2: H6(128) H3(120) H10(86) H0(83)
```

## Requirements

Current project is running on python v3.10.12, is using the standard library so it doesn't require any external library, anyways here are the steps to isolate a virtual environment using **pyenv** tool:
1. Install `Pyenv` following these [steps](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
2. Once install in the CLI run `pyenv install 3.10.12`
3. Clone this repo and in the CLI `cd` inside the repo path
3. Create a virtual environment by running in the same CLI session: `pyenv virtualenv 3.10.12 home_owners_and_neighborhoods`
4. Activate the environment running in the same CLI session: `pyenv activate home_owners_and_neighborhoods`
5. Run the code with `python main.py`

## How To Use
Is simple:
1. Set a txt file inside inside `data` folder
2. Open `main.py` file and set the path to the input file.
3. Run `python main.py` and compare outputs