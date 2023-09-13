# API class
import json
import requests
from teamDetail import TeamStatistics


class API:
    def __init__(self):
        self.base_url = "https://sports.snoozle.net/search/nfl/searchHandler?"
        self.file_type = "inline"
        self.stat_type = "teamStats"
        self.season = 2020
        self.http_client = requests.Session()

    def get_team_statistics(self):
        team_stats_list = []

        for team_name in range(1, 33):  # iterate over the teams from 1-32
            url = f"{self.base_url}fileType={self.file_type}&statType={self.stat_type}&season={self.season}" \
                  f"&teamName={team_name}"
            response = self.http_client.get(url)
            response_json = response.json()
            print("Request URL:", url)
            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)  # Print the response content
            print("JSON Response:", response_json)
            print()

            # Save the JSON response to a file
            with open(f"team_stats_{team_name}.json", "w") as json_file:
                json.dump(response_json, json_file, indent=4)

            if 'matchUpStats' in response_json:
                match_up_stats = response_json['matchUpStats']

                for match_stats in match_up_stats:
                    vis_stats = match_stats.get('visStats', {})
                    home_stats = match_stats.get('homeStats', {})

                    if 'teamName' in vis_stats:
                        team_stats_list.append(
                            TeamStatistics(
                                vis_stats['teamName'],
                                vis_stats.get('teamNumber', ''),
                                vis_stats.get('teamCode', ''),
                                vis_stats.get('score')
                            )
                        )

                    if 'teamName' in home_stats:
                        team_stats_list.append(
                            TeamStatistics(
                                home_stats['teamName'],
                                home_stats.get('teamNumber', ''),
                                home_stats.get('teamCode', ''),
                                home_stats.get('score')
                            )
                        )

        return team_stats_list
