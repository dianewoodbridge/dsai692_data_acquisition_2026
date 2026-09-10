# Use continuumio/miniconda3 as a base image 
FROM continuumio/miniconda3

# Set /Day6 as a working directory
WORKDIR /Day6

# Copy environment.yml
COPY * .

# create an environment using environment.yml
RUN conda env create -f environment.yml -n ex01

# install fastapi[standard] for fastapi's cli on the environment
RUN conda install -n ex01  fastapi[standard] 

# expose port 8000
EXPOSE 8000

# run the ex01.py as fastapi server.
CMD ["conda", "run", "--no-capture-output", "-n", "ex01", "fastapi", "dev", "ex01.py", "--port=8000", "--host=0.0.0.0"]