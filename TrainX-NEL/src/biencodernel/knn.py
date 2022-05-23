from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

import faiss
import numpy as np
import torch


class AbstractFaissIndex(ABC):

    @abstractmethod
    def get_knn_ids_for_vector(self, query_vec: torch.Tensor, k=1) -> List[Tuple[str, float]]:
        """
        Returns a sorted list of k neighbors for query_vec
        :param query_vec:
        :param k:
        :return: A list of tuples (id, distance) (yes distance not similarity)
        """


class FaissHNSWIndex:
    def __init__(self, vectors: Dict[str, torch.Tensor], m=32, efConstruction=40, efSearch=16, normalize: bool = True,
                 omp_num_threads: int = 1):
        """
        Initializes the index.
        :param vectors: Dictionary of ids and vectors.
        :param m: HNSW specific parameter
        :param efConstruction: HNSW specific parameter
        :param efSearch: HNSW specific parameter
        :param omp_num_threads:
        """
        try:
            dim = list(vectors.values())[0].shape[0]
        except KeyError:
            raise Exception("Could not create index, it seems that there were no vectors given.")
        faiss.omp_set_num_threads(omp_num_threads)
        self.index = faiss.IndexHNSWFlat(dim, m)
        self.index.metric_type = faiss.METRIC_INNER_PRODUCT
        self.index.hnsw.efConstruction = efConstruction
        self.index.hnsw.efSearch = efSearch
        self.normalize = normalize
        self.idx2id = list()
        ids, vecs = list(zip(*map(lambda d: (d[0], d[1]), vectors.items())))
        vecs = torch.stack(vecs).numpy()
        if self.normalize:
            vecs = vecs / np.linalg.norm(vecs, ord=2, axis=1, keepdims=True)
        self.index.add(vecs)
        self.idx2id = ids

    def get_knn_ids_for_vector(self, query_vec: torch.Tensor, k=1) -> List[Tuple[str, float]]:
        """
        Returns a sorted list of k neighbors for query_vec
        :param query_vec:
        :param k:
        :return: A list of tuples (id, distance) (yes distance not similarity)
        """
        results = list()
        query_vec = query_vec.numpy().reshape(1, -1)
        if self.normalize:
            query_vec = query_vec / np.linalg.norm(query_vec, ord=2, keepdims=True)
        d, i = self.index.search(query_vec, k=k)
        for distance, idx in zip(np.nditer(d), np.nditer(i)):
            idx_item = idx.item()
            if idx_item == -1:  # if k>number of vectors then it will begin returning -1 as idx
                break
            results.append((self.idx2id[idx_item], distance.item()))
        return results

    def __len__(self):
        return len(self.idx2id)


class FaissExactKNNIndex:
    def __init__(self, vectors: Dict[str, torch.Tensor], normalize: bool = True, omp_num_threads: int = 1):
        """
        Initializes a FAISS flat-IP index
        :param vectors: Dictionary of ids and vectors.
        :param m: HNSW specific parameter
        :param efConstruction: HNSW specific parameter
        :param efSearch: HNSW specific parameter
        :param normalize Normalize vectors, this turns a inner-product index into a cos index
        """
        try:
            dim = list(vectors.values())[0].shape[0]
        except KeyError:
            raise Exception("Could not create index, it seems that there were no vectors given.")
        faiss.omp_set_num_threads(omp_num_threads)
        self.index = faiss.IndexFlatIP(dim)
        self.index.metric_type = faiss.METRIC_INNER_PRODUCT
        self.normalize = normalize
        self.idx2id = list()
        ids, vecs = list(zip(*map(lambda d: (d[0], d[1]), vectors.items())))
        vecs = torch.stack(vecs).numpy()
        if self.normalize:
            vecs = vecs / np.linalg.norm(vecs, ord=2, axis=1, keepdims=True)
        self.index.add(vecs)
        self.idx2id = ids

    def get_knn_ids_for_vector(self, query_vec: torch.Tensor, k=1) -> List[Tuple[str, float]]:
        """
        Returns a sorted list of k neighbors for query_vec
        :param query_vec:
        :param k:
        :return: A list of tuples (id, distance) (yes distance not similarity)
        """
        results = list()
        query_vec = query_vec.numpy().reshape(1, -1)
        if self.normalize:
            query_vec = query_vec / np.linalg.norm(query_vec, ord=2, keepdims=True)
        d, i = self.index.search(query_vec, k=k)
        for distance, idx in zip(np.nditer(d), np.nditer(i)):
            idx_item = idx.item()
            if idx_item == -1:  # if k>number of vectors then it will begin returning -1 as idx
                break
            results.append((self.idx2id[idx_item], distance.item()))
        return results

    def __len__(self):
        return len(self.idx2id)
