Running JUNE
============
- Use `june_installer.sh` to create an anaconda env and install `june`
  and its dependencies there.
- the quickstart notebook from `master` doesn't work out-the-box so I prepared
  a Python script that runs the flow and outputs results and plots (`quickstart.py`)
- run it in the `refactor/interaction` branch from the main JUNE directory:

```
cd $HOME/JUNE
cp june/groups/leisure/cinema.py $HOME
git checkout refactor/interaction
cp $HOME/cinema.py june/groups/leisure/cinema.py
python quickstart.py
```
