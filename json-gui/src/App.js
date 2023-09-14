import React, { useState, useEffect } from 'react';

function App() {
    const [teamStats, setTeamStats] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                let response = await fetch("http://127.0.0.1:5000/api/team_statistics");
                if (response.ok) {
                    let data = await response.json();
                    setTeamStats(data);
                } else {
                    let errorText = await response.text();
                    throw new Error(`Unexpected response: ${errorText}`);
                }
            } catch (error) {
                console.error("There was an error fetching the data", error);
                setError(error.toString());
            }
        };

        fetchData()
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error("There was an error fetching data:", error);
            });
;
    }, []);


    return (
        <div className="App">
            <header className="App-header">
                <h2>Team Statistics</h2>
                <ul>
                    {teamStats.map((team, index) => (
                        <li key={index}>
                            <strong>Team Name:</strong> {team[0]},
                            <strong>Team Code:</strong> {team[2]},
                            <strong>Score:</strong> {team[3]}
                        </li>
                    ))}
                </ul>
                {error && <p style={{ color: "red" }}>{error}</p>}
            </header>
        </div>
    );
}

export default App;
