# Applying Spectral Clustering to Gut Microbiome Data: A Classification Approach


## Introduction
In this study, I explore the adaptation of the spectral clustering algorithm to serve as a classifier, investigating its effectiveness in classifying gut microbiome data by employing different thresholds to compute the affinity matrix. 
## Microbiome Data 
### Introduction
The human microbiome is the collection of microorganisms, that reside on or within human tissues and biofluids along with the corresponding anatomical sites.

<img src="img/Microbiome.png" alt="Microbiome Image" width="350" height="200">

Microbiome can be analyzed at many levels,
the higher the level the more specific the
classification of the microorganisms.

<img src="img/taxonomy.png" alt="Microbiome Levels" width="350" height="200">

### Curated Metagenomic Data of the Human Microbiome
#### Overview of the curatedMetagenomicData package

The `curatedMetagenomicData` package offers standardized and curated human microbiome data for conducting novel analyses. It encompasses various datasets including gene families, marker abundance, marker presence, pathway abundance, pathway coverage, and relative abundance. The data originates from samples collected across different body sites. Taxonomic abundances for bacteria, fungi, and archaea are calculated using MetaPhlAn3, while metabolic functional potential is computed using HUMAnN3. The package provides both manually curated sample metadata and standardized metagenomic data, which are available as (Tree)SummarizedExperiment objects.

**Authors and Contributors:**
- **Authors:** Lucas Schiffer, Levi Waldron
- **Contributors:** Edoardo Pasolli, Jennifer Wokaty, Sean Davis, Audrey Renson, Chloe Mirzayi, Paolo Manghi, Samuel Gamboa-Tuz, Marcel Ramos, Valerie Obenchain, Kelly Eckenrode, Nicola Segata

[Package Link](https://bioconductor.org/packages/release/data/experiment/html/curatedMetagenomicData.html)

#### Gut Microbiome Data For IBD (Inflamatory Bowel Disease) and CRC (Colorectal Cancer) Patients
The CuratedMetagenomicData package offers datasets from two distinct cohorts: one comprising healthy individuals and the other consisting of subjects with various health conditions. Among the diseased subjects, categories include type 2 diabetes, colorectal cancer, adenoma, impaired glucose tolerance, atherosclerotic cardiovascular disease, and inflammatory bowel disease. For this specific project, individuals with inflammatory bowel disease (IBD) and colorectal cancer (CRC) were selected as subjects of interest. Furthermore, the analysis was conducted by selecting the family level. 


## A Classification Approach

### Dataset 
The dataset consists of 555 samples for both the inflammatory bowel disease (IBD) and colorectal cancer (CRC) classes. Each sample is characterized by 99 columns, representing various microbial families and their relative abundances. These relative abundance values indicate the prevalence of specific microbial families within each sample's gut microbiome. For further details, refer to the 'microbiome_family_level.csv' file located in the data folder.

Note:for more details on this section and how the dataset was generated please have a look at _dataset_preprocessing.ipynb_ and _utils_preprocessing.py_
### Splitting the Dataset
The dataset was split, allocating 67% for the training set and 33% for validation.
### Iterated Hold-Out Procedure (Model Selection)
To select the optimal threshold for computing the affinity matrix and determine the best parameters for the MLPClassifier, an iterated hold-out procedure was performed. The training set was divided into 67% for training and 33% for testing, and this process was repeated 1000 times.

Note: for more details on this section and the following ones please have a look at _project_francesco_canonaco.ipynb_, _utils_classification_model.py_, _utils_spectral_clustering.py_

### Spectral Clustering as a Classifier
To create a classification approach by adapting the unsupervised procedure of spectral clustering, different thresholds were applied to compute the affinity matrix. Here's how the new spectral clustering works:

- The affinity matrix was computed using the Bray-Curtis distance.
- The graph was thresholded to optimize the accuracy score, and distance matrix was transformed to similarity. 
- Upon learning the clusters, each cluster was assigned a class based on the majority class within it.
- A two-cluster model was tested by transforming new samples to align with the computed affinity matrix.
- The transformed samples were assigned to the nearest cluster.

### Optimization of the Spectral Clustering by Thresholding the Affinity Matrix
To optimize the Spectral Clustering procedure, multiple thresholds were tested. The accuracy values for different thresholds are presented in the chart below. Each threshold underwent an iterated hold-out procedure with 1000 iterations.

<img src="img/optimal_threshold_spectral_clustering.png" alt="Microbiome Levels" width="600" height="200">

### Optimization of the MLPClassifier
The MLPClassifier underwent optimization with respect to various parameters, including hidden layers, alpha, and max iterations. Each parameter was optimized individually through an iterated hold-out process consisting of 1000 iterations. The resulting optimal parameters are as follows:

- **Hidden Layers**: (99,50)
- **Alpha**: 1e-5
- **Max Iterations**: 3

The activation function used was ReLU, and the solver employed was Adam.

### Comparing MLP Classifier and Spectral Clustering Accuracy
The image below illustrates a comparison between the two best-performing models with their respective optimal parameters. Both models exhibit similar performance on both the training and test sets, indicating effective handling of overfitting despite the dataset's complexity. Moreover, both models demonstrate comparable performance for this particular problem instance. 

<img src="img/iterated_holdout_comparison.png" alt="" width="600" height="200">

The optimal models were trained using the entire training set and validated on 33% of the initial split. The performance of both models on the validation set is illustrated in the image below.

<img src="img/final_comparison.png" alt="" width="600" height="200">

## Conclusion
Both models demonstrated similar performance on this particular problem instance, with their performances being notably comparable. While the models outperformed random guessing, their performances were not particularly remarkable, possibly due to the large number of variables and the insufficient sample size. Additionally, sparsity may have influenced the results significantly. Despite these challenges, the Spectral Clustering classifier performed admirably considering the adaptation of an unsupervised algorithm and the limited amount of data available.

#### Description of the folders:
- **charts** contains an interactive version of the charts
- **img** contains the images used in the report
- **experiments_results** contains the result of the best threshold selection procedure
