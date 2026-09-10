# Use continuumio/miniconda3 as a base image 
FROM continuumio/miniconda3

# Set /Day6 as a working directory
WORKDIR /Day6

# Copy environment.yml
COPY * .

# create an environment using environment.yml
RUN conda env create -f environment.yml -n ex03

# expose port 8502
EXPOSE 8502

CMD ["conda", "run", "--no-capture-output", "-n", "ex03", "streamlit", "run", "main.py", "--server.address", "0.0.0.0"]