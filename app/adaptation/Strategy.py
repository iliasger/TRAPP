# abstract class for an adaptation strategy

class Strategy:

    def monitor(self):
        pass

    def analyze(self, monitor_data):
        pass

    def plan(self, analysis_data):
        pass

    def execute(self, plan_data):
        print "SSSS"
