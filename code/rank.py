# leaderboard.py
import json
import os

class Leaderboard:
    def __init__(self, filename='../data/leaderboard.json'):
        self.filename = filename
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.data = json.load(file)
        else:
            self.data = []

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def add_entry(self, name, time, difficulty):
        difficulty_priority = {'normal': 0, 'easy': 1}
        self.data.append({'name': name, 'time': time, 'difficulty': difficulty})
        self.data.sort(key=lambda x: (difficulty_priority[x['difficulty']], x['time']))
        self.data = self.data[:6]  # 只保留前6条记录
        self.save()
        self.load()  # 重新加载数据

    def get_top_entries(self, limit=6):
        self.load() # 获取排行榜时加载最新数据
        return self.data[:limit]