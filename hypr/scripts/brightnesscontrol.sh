#!/usr/bin/env bash

scrDir=$(dirname "$(realpath "$0")")
iconsDir="~/.config/hypr/icons"
# shellcheck disable=SC1091
#source "$scrDir/globalcontrol.sh"

print_error() {
  local cmd
  cmd=$(basename "$0")
  cat <<EOF
    "${cmd}" <action> [step]
    ...valid actions are...
        i -- <i>ncrease brightness [+5%]
        d -- <d>ecrease brightness [-5%]

    Example:
        "${cmd}" i 10    # Increase brightness by 10%
        "${cmd}" d       # Decrease brightness by default step (5%)
EOF
}

send_notification() {
  brightness=$(brightnessctl info | grep -oP "(?<=\()\d+(?=%)" | cat)
  # brightness=$(ddcutil --bus 15 getvcp 10 | sed 's/.*current value = *\([0-9]*\).*/\1/')
  brightinfo=$(brightnessctl info | awk -F "'" '/Device/ {print $2}')
  angle="$((((brightness + 2) / 5) * 5))"
  # shellcheck disable=SC2154
  echo "angle: ${angle}"
  ico="${iconsDir}/knob-${angle}.svg"
  echo "ico: ${ico}"
  bar=$(seq -s "." $((brightness / 15)) | sed 's/[0-9]//g')
  # [[ "${isNotify}" == true ]] && notify-send -a "HyDE Notify" -r 7 -t 800 -i "${ico}" "${brightness}${bar}"
  #
  notify-send -a "Brightness" -i "${ico}" -r 7 -t 800 "${brightness}"
}

get_brightness() {
  ddcutil --bus 15 getvcp 10 | sed 's/.*current value = *\([0-9]*\).*/\1/'
}

step=${BRIGHTNESS_STEPS:-5}
step="${2:-$step}"

case $1 in
i | -i) # increase the backlight
  if [[ $(get_brightness) -lt 10 ]]; then
    # increase the backlight by 1% if less than 10%
    step=1
  fi

  brightnessctl set +"${step}"%
  # ddcutil --bus 15 setvcp 10 + ${step}
  send_notification
  ;;
d | -d) # decrease the backlight

  if [[ $(get_brightness) -le 10 ]]; then
    # decrease the backlight by 1% if less than 10%
    step=1
  fi

  if [[ $(get_brightness) -le 1 ]]; then
    brightnessctl set "${step}"%
    # ddcutil --bus 15 setvcp 10 - ${step}
    exit 0
  else
    brightnessctl set "${step}"%-
    # ddcutil --bus 15 setvcp 10 - ${step}
  fi
  -
  send_notification
  ;;
s | -s)
  brightnessctl set "${step}"%
  # ddcutil --bus 15 setvcp 10 ${step}
  ;;
*) # print error
  print_error ;;
esac
