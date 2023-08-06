FROM fedora:latest

VOLUME /opt/robotframework/tests

# Basic OS and Phyton dependencies
RUN dnf upgrade -y
RUN dnf install -y python39 pip docker
RUN dnf module install -y nodejs:12
# Database dependencies PostgreSQL
RUN dnf install -y libpq-devel
# FTSA installation for production environment
RUN pip install ftsa-tjpb && ftsa install
# FTSA installation for tests environment
# RUN pip install -i https://test.pypi.org/simple/ ftsa-tjpb==X.Y.Z && ftsa install
# RUN pip install -i https://test.pypi.org/simple/ ftsa-tjpb-core==X.Y.Z

WORKDIR /opt/robotframework/tests