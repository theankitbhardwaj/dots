#!/bin/zsh

# Create config directories if they don't exist
mkdir -p ~/.config/ghostty
mkdir -p ~/.config/hypr
mkdir -p ~/.config/kitty
mkdir -p ~/.config/swaync
mkdir -p ~/.config/waybar
mkdir -p ~/.config/wlogout
mkdir -p ~/.config/wofi

# Symlink config files and directories
ln -sf $(pwd)/ghostty ~/.config/ghostty
ln -sf $(pwd)/hypr ~/.config/hypr
ln -sf $(pwd)/kitty ~/.config/kitty
ln -sf $(pwd)/starship/starship.toml ~/.config/starship.toml
ln -sf $(pwd)/swaync ~/.config/swaync
ln -sf $(pwd)/waybar ~/.config/waybar
ln -sf $(pwd)/wlogout ~/.config/wlogout
ln -sf $(pwd)/wofi/style.css ~/.config/wofi/style.css

echo "Dotfiles installed successfully!"
