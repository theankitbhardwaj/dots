#!/bin/zsh

# Symlink config files and directories
ln -sf $(pwd)/ghostty ~/.config/ghostty
ln -sf $(pwd)/hypr ~/.config/hypr
ln -sf $(pwd)/kitty ~/.config/kitty
ln -sf $(pwd)/starship/starship.toml ~/.config/starship.toml
ln -sf $(pwd)/swaync ~/.config/swaync
ln -sf $(pwd)/waybar ~/.config/waybar
ln -sf $(pwd)/wlogout ~/.config/wlogout
ln -sf $(pwd)/wofi ~/.config/wofi
ln -sf $(pwd)/swayosd ~/.config/swayosd

echo "Dotfiles installed successfully!"
