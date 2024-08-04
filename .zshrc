# Source the .zshrc file from the home directory
source ~/.zshrc

# Set the PYTHONPATH to include the scripts and support directories
export PYTHONPATH=$(pwd)/scripts:$PYTHONPATH
export PYTHONPATH=$(pwd)/support:$PYTHONPATH

export PATH=$(pwd)/scripts:$PATH
