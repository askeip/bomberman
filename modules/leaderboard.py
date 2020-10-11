class Leaderboard():

    def __init__(self, max_size, file_name="leaderboard.txt"):
        self.file_name = file_name
        self.max_size = max_size
        self.results = FileLeaderboard.read_leaderboard(file_name)
        self.str_format = ""
        self.refresh_str_format()

    def refresh_str_format(self):
        self.str_format = ''
        for i in range(len(self.results)):
            self.str_format += str(i + 1) + ". " + str(self.results[i]) + '\n'

    def refresh(self, value):
        added = False
        for i in range(len(self.results)):
            if value > self.results[i]:
                self.results.insert(i, value)
                if len(self.results) > self.max_size:
                    self.results.pop()
                added = True
                break
        if len(self.results) < self.max_size and not added:
            self.results.append(value)
        self.refresh_str_format()
        FileLeaderboard.write_leaderboard(self, self.file_name)


class FileLeaderboard():

    @staticmethod
    def write_leaderboard(leaderboard, file_name="leaderboard.txt"):
        with open(file_name, mode='w', encoding='UTF-8') as f:
            f.write(leaderboard.str_format)

    @staticmethod
    def read_leaderboard(file_name="leaderboard.txt"):
        leaderboard = []
        try:
            with open(file_name, encoding='UTF-8') as f:
                str_board = f.read().split('\n')
                for line in str_board:
                    line = line.split('. ')
                    leaderboard.append(int(line[1]))
            leaderboard.sort()
        finally:
            return leaderboard
