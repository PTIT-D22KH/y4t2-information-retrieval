from sklearn.datasets import fetch_rcv1

rcv1 = fetch_rcv1(data_home="./")
print(rcv1.data.shape)
