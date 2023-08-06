RUN echo "export PS1='\[\033[01;36m\](docker)\[\033[00m\] \[\033[01;32m\]\u@@@(container_name)\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '" >> @(home_dir)/.bashrc
