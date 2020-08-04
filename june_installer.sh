echo "Entering HOME..."
cd $HOME
echo "Sourcing the installer - install in HOME/USER/miniconda3 as suggested"
sleep 3
echo "Answer no to conda initialization, we'll source it later"
bash Miniconda3-latest-Linux-x86_64.sh
echo "Initializing conda base environment..."
eval "$(/home/users/$USER/miniconda3/bin/conda shell.bash hook)"
echo "Creating and activating empty virtual environment..."
conda create -y -n june
conda activate june
echo "Installing pip..."
conda install -y pip
echo "Grabbing JUNE..."
git clone https://github.com/IDAS-Durham/JUNE.git
cd JUNE
echo "INstalling dependencies..."
pip install -r requirements.txt
echo "INstalling june..."
pip install -e .
echo "Installing jupyter..."
conda install -y -c conda-forge jupyter
