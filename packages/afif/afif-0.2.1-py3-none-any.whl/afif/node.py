class AfifNode:

    def __init__(self, value):
        self.data_value = value
        self.next = None

    def description(self):
        print(f"value : {self.data_value}, next : {self.next}")

    def next_node(self):
        return self.next
