# team stats class
# Import into api.py

class TeamStatistics:
    def __init__(self, team_name, team_number, team_code, score):
        """
        Initialize TeamStatistics instance
        :param team_name: Name of the team
        :param team_number: Identifying team by their number
        :param team_code: The code identifying the team
        :param score: Score of the team
        """

        self.team_name = team_name
        self.team_number = team_number
        self.team_code = team_code
        self.score = score

    def __str__(self):
        # return a formatted string with the team attributes
        return f"Team Name: {self.team_name}, Team Code: {self.team_code}, Score: {self.score}"

    def add_to_tuple(self):
        # return a tuple containing team attributes
        return self.team_name, self.team_number, self.team_code, self.score
