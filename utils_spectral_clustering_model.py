# importing libraries 
import pandas as pd
from scipy.spatial import distance
from sklearn.cluster import SpectralClustering
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.neighbors import NearestCentroid
from sklearn.metrics import accuracy_score

def get_distance_matrix(dataset, metric="braycurtis"):
    distance_matrix=distance.squareform(distance.pdist(dataset, metric=metric))
    # avoiding NaN values
    distance_matrix=pd.DataFrame(distance_matrix).fillna(0).values
    return distance_matrix

def get_accuracy(cluster_labels: np.ndarray, y_train: pd.core.series.Series)->int:
  mapping_class_to_clusters=pd.DataFrame({'cluster':list(cluster_labels), 'class':list(y_train)})
  # given this dataset we need to determine what is the majority class for each cluster
  group_by_class_to_clusters=mapping_class_to_clusters.groupby(by=["cluster", "class"]).size().reset_index(name="count")
  max_counts_idx = group_by_class_to_clusters.groupby('cluster')['count'].idxmax()
  # Display the corresponding rows
  result = group_by_class_to_clusters.loc[max_counts_idx]
  total_number_of_samples=group_by_class_to_clusters['count'].sum()
  correctly_predicted=result['count'].sum()
  accuracy=correctly_predicted/total_number_of_samples
  accuracy=accuracy.round(3)
  return accuracy,result

def get_accuracy_test(X_train_graph_similarity, X_test_graph_similarity,cluster_labels, y_test, result_classes_per_cluster):
  clf=fit_nearest_centroid(X_train_graph_similarity,cluster_labels)
  y_test_predicted_cluster=clf.predict(X_test_graph_similarity)
  clusters_list=result_classes_per_cluster['cluster'].to_list()
  classes_list=result_classes_per_cluster['class'].to_list()
  mapping_cluster_to_class_dict={clusters_list[i]:classes_list[i] for i in range(len(clusters_list))}
  y_test_predicted_class=[mapping_cluster_to_class_dict[p] for p in y_test_predicted_cluster]
  # get the accuracy
  accuracy_test=accuracy_score(y_test,y_test_predicted_class)
  accuracy_test=accuracy_test.round(3)
  return accuracy_test

def fit_nearest_centroid(X_train_graph_similarity, cluster_labels):
  clf = NearestCentroid()
  clf.fit(X_train_graph_similarity,cluster_labels)
  return clf

def get_test_set_distances(X_test,X_train):
  X_train_array = X_train.values
  X_test_array = X_test.values
  # Calculate Bray-Curtis distance using cdist
  result_matrix = distance.cdist(X_test_array, X_train_array, metric='braycurtis')
  #avoiding NaN values
  distance_matrix=pd.DataFrame(result_matrix).fillna(0).values
  return distance_matrix

def iterated_hold_out_clustering(X:pd.core.frame.DataFrame,y:pd.core.series.Series,iterations:int,thresh:float)->list:
  results={'training_accuracy':[], 'test_accuracy':[]}
  for i in range(iterations):
    # splitting dataset in training and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=i)
    X_train_graph=get_distance_matrix(X_train)
    X_train_graph[X_train_graph>=thresh]=1
    X_train_graph_similarity=1-X_train_graph
    clusterer = SpectralClustering(n_clusters=2, random_state=i, affinity="precomputed", n_jobs=-1)
    # distance matrix is computed using braycurtis distance!
    cluster_labels = clusterer.fit_predict(X_train_graph_similarity)
    accuracy_training,result_classes_per_cluster=get_accuracy(cluster_labels,y_train)
    results['training_accuracy'].append(accuracy_training)
    # testing the model
    X_test_graph=get_test_set_distances(X_test,X_train) 
    # use the threshold
    X_test_graph[X_test_graph>=thresh]=1
    # convert distance to similarity
    X_test_graph_similarity=1-X_test_graph
    # get test accuracy
    test_accuracy=get_accuracy_test(X_train_graph_similarity, X_test_graph_similarity, cluster_labels, y_test, result_classes_per_cluster)
    results['test_accuracy'].append(test_accuracy)

  return results

def grid_search_threshold(X:pd.core.frame.DataFrame, y:pd.core.series.Series, thresholds:list, hold_out_it:int)->dict:
  results_gridsearch={'thresh':[], 'training_accuracy':[], 'test_accuracy':[]}
  
  for t in thresholds:
    results_gridsearch['thresh'].append(t)
    results_hold_out=iterated_hold_out_clustering(X,y,hold_out_it,t)
    mean_training=np.mean(np.asarray(results_hold_out['training_accuracy']))
    mean_test=np.mean(np.asarray(results_hold_out['test_accuracy']))
    results_gridsearch['training_accuracy'].append(mean_training)
    results_gridsearch['test_accuracy'].append(mean_test)
    
  return results_gridsearch