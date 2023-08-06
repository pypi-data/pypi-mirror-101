#!/bin/bash

# Installs:
#  - Basic system debians for development (cmake etc)
#  - Ros2 Apt Repo / Snorriheim PPA
#  - Colcon and a few Ros2 development packages

##############################################################################
# Colours
##############################################################################

BOLD="\e[1m"

CYAN="\e[36m"
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"

RESET="\e[0m"

padded_message ()
{
  line="........................................"
  printf "%s %s${2}\n" ${1} "${line:${#1}}"
}

pretty_header ()
{
  echo -e "${BOLD}${1}${RESET}"
}

pretty_print ()
{
  echo -e "${GREEN}${1}${RESET}"
}

pretty_warning ()
{
  echo -e "${YELLOW}${1}${RESET}"
}

pretty_error ()
{
  echo -e "${RED}${1}${RESET}"
}

##############################################################################
# Methods
##############################################################################

function add_ros_apt_repo ()
{
    if [ ! -f '/etc/apt/sources.list.d/ros2.list' ]; then 
        curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2.list
    fi
}

function add_snorriheim_ppa ()
{
    apt-add-repository -y -n ppa:d-stonier/snorriheim
}

function install_debs()
{
  args=$1[@]
  DEBS=("${!args}")  # pull the array out ... magic
  DEBS_STRING="${DEBS[@]}"
  DEBIAN_FRONTEND=noninteractive apt-get install -y ${DEBS[@]}
  if [ $? -ne 0 ]; then
    pretty_error "Failed to install debs [${DEBS_STRING}]"
    return 1
  fi
  return 0
}

##############################################################################
# Variables
##############################################################################

pretty_header "Variables"

UBUNTU_DISTRO=`awk -F= '$1=="VERSION_CODENAME" { print $2 ;}' /etc/os-release`
declare -A ros_distro_map=( ['bionic']='dashing' ['focal']='foxy' )
ROS_DISTRO=${ros_distro_map[${UBUNTU_DISTRO}]}

BOOTSTRAP_DEBS=(curl gnupg2 lsb-release software-properties-common)
SYSTEM_DEBS=(build-essential cmake git python3-flake8 python3-pip python3-pytest-cov python3-setuptools wget)
COLCON_DEBS=( \
    python3-colcon-core python3-colcon-common-extensions python3-colcon-coveragepy-result python3-colcon-ed python3-colcon-lcov-result \
    python3-rosdep python3-vcstool \
)
SNORRIHEIM_DEBS=(python3-groot-rocker-extensions python3-vci)
ROS2_DEBS=(ros-${ROS_DISTRO}-ros-environment)

echo -e "  ${CYAN}UBUNTU_DISTRO${RESET}: ${YELLOW}${UBUNTU_DISTRO}${RESET}"
echo -e "  ${CYAN}ROS_DISTRO${RESET}: ${YELLOW}${ROS_DISTRO}${RESET}"

##############################################################################
# Do Stuff
##############################################################################

pretty_header "Installing Repos and Debs"

apt-get update
install_debs BOOTSTRAP_DEBS || exit 1
add_ros_apt_repo
add_snorriheim_ppa
apt-get update
install_debs SYSTEM_DEBS || exit 1
install_debs COLCON_DEBS || exit 1
install_debs SNORRIHEIM_DEBS || exit 1
install_debs ROS2_DEBS || exit 1
rosdep init || exit 1
