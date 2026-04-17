#!/bin/bash

# 1. Get the absolute path of the current directory
WD=$(pwd)
echo "Setting up Kap kernel in: $WD"

# 2. Update the Python script
# Replaces the wd = '...' line with the current absolute path
sed -i "s|wd = '.*'|wd = '$WD'|g" kap_kernel.py

# 3. Update the kernel.json
# Replaces the python path and the script path
# Note: This assumes your kernel.json is in the current folder before installation
sed -i "s|\"/home/.*/kap_kernel.py\"|\"$WD/kap_kernel.py\"|g" kernel.json

# 4. Install the kernelspec to Jupyter
# --user installs it to ~/.local/share/jupyter/kernels
echo "Registering kernelspec..."
jupyter kernelspec install "$WD" --user --name=kap --replace

# 5. Copy the logo
# (jupyter kernelspec install usually copies all files in the dir, 
# but we'll force the logo move to be sure)
KERNEL_DEST="$HOME/.local/share/jupyter/kernels/kap"
if [ -f "$WD/logo-64x64.png" ]; then
    cp "$WD/logo-64x64.png" "$KERNEL_DEST/"
    echo "Logo installed to $KERNEL_DEST"
fi

echo "Done! Restart Jupyter Lab to see the changes."
