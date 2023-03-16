* DBT Cloud Setup
  * create an account on [DBT cloud](https://cloud.getdbt.com/).
  
  * set up project
  * go back to [Gharchive](https://github.com/GbotemiB/gharchive_DE_project) to fork the repository.
  * follow the instructions [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md) to setup project.
  * the project directory has to be changed to `/dbt`. Go to settings. click on the project folder. Then edit the Project subdirectory to `/dbt`.
  * ![show](project_directory.png)
  * lets create a production environment. go to deploy, then environment. create a new environment with the name, production.
  * you can name the dataset for the deployment credentials `production`.
  * ![show](images/dbt_environment.png)
  * Lets create a job for our transformation. Name the Job, the production environment will be selected automatically.
  * enable generate docs on run and source refreshness.
  * edit the command to `dbt build`.
  * we will trigger the run with prefect, so no need to add triggers.
  * copy the web address of the dbt job link.
  ![show](images/dbt_id.png)
  * the digits after deploy in the link is the user_id, while the link after the jobs is the job_id. we will need it in setting triggers with prefect.

