
@[if user_active ]@
USER root
@[end if]@

COPY colcon_setup.bash /usr/local/bin/groot-colcon-setup
RUN chmod 755 /usr/local/bin/groot-colcon-setup && /usr/local/bin/groot-colcon-setup

@[if user_active ]@
USER @(user_name)
RUN vci config https://raw.githubusercontent.com/stonier/repos_index/devel/`awk -F= '$1=="VERSION_CODENAME" { print $2 ;}' /etc/os-release`.yaml
RUN rosdep update
@[end if]@
