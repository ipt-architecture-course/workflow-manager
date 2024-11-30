class ProcessorFactory:
    def __init__(self):
        self.processors = {}

    def register_processor(self, process_type, processor_adapter):
        self.processors[process_type] = processor_adapter

    def get_processor(self, process_type):
        if process_type not in self.processors:
            raise ValueError(f"No processor registered for type '{process_type}'.")
        return self.processors[process_type]

processor_factory = ProcessorFactory()