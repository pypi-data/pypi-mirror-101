ENV TERM @(terminal)

# Configure the default timezone for apt package tzdata
RUN ln -fs @(default_timezone) /etc/localtime
RUN apt-get update
# Install this first - will result in only one spurious warning that apt-utils is not installed
RUN DEBIAN__FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils
RUN DEBIAN__FRONTEND=noninteractive apt-get install -y @(system_dependencies)

RUN locale-gen @(language)
ENV LANG @(language)
