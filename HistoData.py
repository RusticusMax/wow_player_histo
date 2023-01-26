

class HistoData:
    def __init__(self, num_buckets: int):
        self.m_count = 0
        self.m_buckets = [0] * num_buckets
        self.m_num_buckets: int = num_buckets

    def num(self):
        return self.m_num_buckets

    def chk_idx(self, idx: int):
        if idx >= self.m_num_buckets:
            raise ValueError(f"Histo_data: Bucket index {idx} out of range {self.m_num_buckets-1}")
        return True

    def bucket(self, idx: int):
        self.chk_idx(idx)
        return self.m_buckets[idx]

    def inc_bucket(self, idx: int):
        self.chk_idx(idx)
        self.m_buckets[idx] += 1

    def cnt(self):
        return self.m_count

    def inc_cnt(self):
        self.m_count += 1
