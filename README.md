# Homeowners and Neighborhoods

## Exercise

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