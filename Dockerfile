FROM python:3.11-slim

# Tell apt-get we're never going to be able to give manual feedback (on build)
ARG DEBIAN_FRONTEND=noninteractive

# Try to setup proper user IDs
ARG USER_UID=${USER_UID:-999}

# set ipdb as default debugger
# tell python not to buffer stdout
# tell python not to write bytecode to disk
ENV PYTHONBREAKPOINT=ipdb.set_trace \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

## os dependencies
RUN apt-get update -y && \
    apt-get -y install --no-install-recommends postgresql-client  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# user
RUN adduser --system --uid=${USER_UID} --group --home=/school_schedule-api/  --shell=/sbin/nologin --gecos "Docker image user" school_schedule

# copy additional configs
COPY --chown=school_schedule:school_schedule pyproject.toml /app/pyproject.toml
COPY --chown=school_schedule:school_schedule pytest.ini /app/pytest.ini

# copy scripts
COPY --chown=school_schedule:school_schedule scripts /app/scripts
RUN chmod ug+x /app/scripts/*

# install requirements
COPY --chown=school_schedule:school_schedule requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt


# copy code
COPY --chown=school_schedule:school_schedule school_schedule_api /app/school_schedule_api

USER school_schedule

WORKDIR /app/school_schedule_api
