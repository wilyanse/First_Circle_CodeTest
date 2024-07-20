# First_Circle_CodeTest

1. Create python venv with `python -m venv venv`
2. Run the python venv with `venv/scripts/activate`
3. Run the docker container for PostgreSQL with `docker-compose up`

Running the latest code in the process, in this case it would be `dataloading.py` (since Data Governance only covers logging which does not run a python file) will run the previous code as well since the python files are imported into each other, ensuring no redundancy. Do note that most of the Python notebooks in the subdirectories may not work as intended because of path issues, importing issues, and so forth. The notebooks only serve to document my thought process in developing the modules and as your guide.