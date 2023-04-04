### Prefect
If you are familar with prefect, you can decide to use prefect locally. But Prefect Cloud will be used.
* create a [prefect cloud account](https://app.prefect.cloud)
* create a workspace
  ![show](images/prefect.png)
* to set api keys, go to [my profile](https://app.prefect.cloud/my/profile), click on `API Keys`, create api key, name the api key `login`, copy the key securely.

* go back to terminal on the vm, run the next command to install the requirement to run prefect.
  run `sudo apt install python3-pip` to install pip package manager. Then change directory into the cloned repo, then run the following.

    ```
    pip install -r requirements.txt
    ```
    then run `sudo reboot now` to reboot vm instance or `source ~/.bashrc` to effect installation.

    To authenticate with prefect cloud, run
    ```
    prefect cloud login
    ```
    choose `Paste an API key`
* blocks are available on prefect cloud. if you are running prefect locally, you might need to add the blocks by running the following commands in terminal.
  ```
  prefect block register -m prefect_gcp
  prefect block register -m prefect_github
  prefect block register -m prefect_dbt
  prefect block register -m prefect_docker
  ```
* configuring prefect blocks. blocks can be configured with scripts or through the Prefect UI. The blocks will be configured via the UI.
  #### GCP bucket block
    ![show](images/prefect_block.png)
     * click the + to configure a block
     * go to GCS Bucket
     * name the block `gharchive`
     * get your gcp bucket name that was created in terraform setup. use it for the name of the bucket `gharchive_dataset_gcs`
     * scroll down to Gcp Credentials to add credentials. Click `Add +` to add gcp credentials.
     * let the name of the block name be `gcp-creds`
     * the api key that was downloaded when setting up GCP. copy the contents to `Service Account Info (Optional)` and save it.
     * the credential will be added to the gcp block automatically. click save
     ![show](images/prefect_gcp.png)
  #### Github block
    * search github in blocks and add it. 
    * name the block `gharchive-github`
    * Enter the repository as the forked repo.
    * Enter reference as main.
      ![show](images/prefect_github.png)