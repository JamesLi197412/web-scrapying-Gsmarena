import time

class TokenBucket:
    def __init__(self, tokens_per_second):
        self.tokens_per_second = tokens_per_second
        self.tokens = 0
        self.last_token_time = time.time()

    def get_token(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_token_time

        self.tokens += elapsed_time * self.tokens_per_second
        self.tokens = min(self.tokens, self.tokens_per_second)  # Limit tokens to the maximum rate

        if self.tokens < 1:
            time_to_sleep = (1 - self.tokens) / self.tokens_per_second
            time.sleep(time_to_sleep)
            self.tokens += 1

        self.tokens -= 1
        self.last_token_time = time.time()

        return True

