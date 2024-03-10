# Site Archiver
## Running the Application


1. Create Docker Image:

    ```docker build -t malvandi/site-archiver:1.0.0 .```


2. Run:
   #### Windows:
   ```docker run -v ${pwd}:/app malvandi/site-archiver:1.0.0 yahoo.com```

   And for metadata use:

   ```docker run -v ${pwd}:/app malvandi/site-archiver:1.0.0 --metadata yahoo.com```
   
   #### Linux:
   ```docker run -v $(pwd):/app malvandi/site-archiver:1.0.0 yahoo.com```

   And for metadata use:

   ```docker run -v $(pwd):/app malvandi/site-archiver:1.0.0 --metadata yahoo.com```


3. See the results in `./Downloads` directory