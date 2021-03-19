Turkish Text Categorization
---

This is meant to serve as an example of how to structure
and work on your ML projects, and deploy the 
resultant models.

The dataset I have chosen can be found on [Kaggle](https://www.kaggle.com/savasy/ttc4900).

- The python packages can be installed via the requirements.txt file (in a venv), or using [Poetry](https://python-poetry.org/) (preferred way).
- To get the models and data files, you'll also need [DVC](https://dvc.org/). Just run `dvc pull` in this repo to get the data/artifacts.

---
### Docker

- The docker images can be built easily using the `docker-build.sh` file (you can change the tag name if you want).
- Then run the image simply using `docker run -d -p (your host machine port):8080 newscat (or the other name)`
- The port on docker can be configured using the env variable port.

Examples:

    docker run -d -p 8085:8080 newscat

    docker run -it -p 8085:8081 --env PORT=8081 newscat
