# Clustering-NH3-1-1-in-High-Mass-Star-Forming-Regions
The aim of this project is to perform clustering on NH3(1,1) data in low hyperfine width regions to see if turbulence is typically low in early stages of star formation.

The RAMPS data was used to perform clustering on the NH3(1,1) hyperfine width maps for all regions across the northern Galactic Plane. K-Means clustering was used for clustering data into various clumps for each region based on the within-cluster-seperation of all datapoints. The number of clumps for each initialization was selected according to the best silhouette score. Performing a silhouette analysis allows the user to get an estimate for the best clustering for each region without visually counting clumps, which would introduce bias.

You can find some of the codes I used for my summer project at Green Bank in the scripts directory. 


