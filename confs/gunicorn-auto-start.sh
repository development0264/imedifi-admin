#!/bin/bash

NAME="CareMedicsBackend"                                  							              # Name of the application
DJANGODIR=/home/imedifi/imedify/backend/             				        # Django project directory
DJANGOENVDIR=/home/imedifi/envmed            			    # Django project env
SOCKFILE=/home/imedifi/imedify/backend/gunicorn.sock  		  # we will communicte using this unix socket
USER=imedifi                                        					              # the user to run as
GROUP=imedifi                                     							            # the group to run as
NUM_WORKERS=1                                    							            # how many worker processes should Gunicorn spawn (2 * CPUs + 1)
DJANGO_SETTINGS_MODULE=CareMedicsBackend.settings             						            # which settings file should Django use
DJANGO_WSGI_MODULE=CareMedicsBackend.wsgi                     						            # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source /home/imedifi/envmed/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ${DJANGOENVDIR}/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
