from sklearn_extra.cluster import KMedoids
from sklearn.datasets import make_blobs

# Generate synthetic data for clustering
X, _ = make_blobs(n_samples=100, centers=3, random_state=42)

# Apply KMedoids clustering
kmedoids = KMedoids(n_clusters=3, random_state=0).fit(X)

# Output results
print("Cluster centers:", kmedoids.cluster_centers_)
print("Labels:", kmedoids.labels_)
print("Testing scikit-learn-extra completed successfully!")