# DBT Cloud Setup
  * Create an account on [DBT cloud](https://cloud.getdbt.com/).
  * Set up project
  * Follow the instructions [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md) to setup project. you can use the keys that was setup for the instructions.
  * The project directory has to be changed to `/dbt`. Go to settings. click on the project folder. Then edit the Project subdirectory to `/dbt`.
   ![show](../images/project_directory.png)
  * Lets create a production environment. go to deploy, then environment. create a new environment with the name, production.
  * You can name the dataset for the deployment credentials `production`.
  * Lets create a job for our transformation. Name the Job, the production environment will be selected automatically.
  * Enable generate docs on run and source refreshness.
  * Edit the command to `dbt build --select +gh_data`.
  * We will trigger the run with prefect, so no need to add triggers. To use DBT access keys, you have to have a paid version. But we will be using the trial version which gives us access to the api.
  * Copy the web address of the dbt job link.
  ![show](../images/dbt_id.png)
  * The digits after deploy in the link is the user_id, while the link after the jobs is the job_id. we will need it in setting triggers with prefect.
  

Continue the setup [here]([../README.md](https://github.com/GbotemiB/gharchive_de_project/blob/main/README.md#dbt-cloud))
