<p align="center">
  <img src="https://www.flowfusic.com/brandmark-design_transparent_for_web.png" width="350">
</p>


# flowfusic-cli

Flowfusic's command line tool for project visualization. The CLI connects your Flowfusic projects with your local Paraview postprocessing software.

Quick Start
-----------

1.  Create a free Flowfusic account at [flowfusic.com](https://www.flowfusic.com)

2. Install the cli:

   ```
   $ pip install flowfusic-cli
   ```

3. Login with the cli by typing:

   ```
   $ flowfusic login
   ```

This step will open a web browser and ask for your login credentials.

4. You can now visualize your Flowfusic projects using Paraview by running

   ``` 
   $ flowfusic paraview --paraview PATH/TO/PARAVIEW 
   ```

   Note that if paraview is already accessible in your path, it is sufficient to run

   ``` 
   $ flowfusic paraview
   ```



## Acknowledgements

We would like to acknowledge excellent Open Source CLI tools created by FloydHub.
