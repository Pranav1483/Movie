import React, {useState} from "react";
import { useNavigate } from "react-router-dom";
import host from "./Host";

function MovieBox(prop) {
    const [liked, setLiked] = useState(prop['movie']['liked']);
    const [watch_list, setWatch_list] = useState(prop['movie']['watch_list']);
    const [watched, setWatched] = useState(prop['movie']['watched']);
    const navigate = useNavigate();
    const handleStatus = (target) => {
        fetch(host + '523a5039c4785c323b530f27de38794b44559b2bbd2c00e3f0e67e4c5438137a/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username: prop['user']['username'], id: prop['movie']['id'], target: target, value: (target === "likes")?liked:(target === "watch_list")?watch_list:watched})
        })
        .then((response) => {
            if (response.status === 204) {
                if (target === "likes") {
                    setLiked((prevLiked) => (prevLiked === "0" ? "1" : "0"));
                  } else if (target === "watch_list") {
                    setWatch_list((prevWatchList) => (prevWatchList === "0" ? "1" : "0"));
                  } else {
                    setWatched((prevWatched) => (prevWatched === "0" ? "1" : "0"));
                  }
            }
        })
        .catch(e => {

        });
    }

    const handleMovie = (event) => {
        event.preventDefault();
        navigate('/watch?movie=' + prop['movie']['id'], {state: {user: prop['user']}});
    }
    return (
        <div key={prop['movie']['id']} className="movie-tile">
            <button className="movie-image-tile" onClick={handleMovie} style={{backgroundImage: 'url(' + prop['movie']['cover'] + ')'}}>
                <span className="movie-tile-play"></span>
            </button>
            <div className="icons-container">
                <button className="movie-tile-like" onClick={() => handleStatus("likes")}>
                    <i className={(liked === '0')?"fa-sharp fa-regular fa-heart":"fa-sharp fa-solid fa-heart"}></i>
                </button>
                <button className="movie-tile-watch_list" onClick={() => handleStatus("watch_list")}>
                    <i className={(watch_list === '0')?"fa-regular fa-bookmark":"fa-solid fa-bookmark"}></i>
                </button>
                <button className="movie-tile-watched" onClick={() => handleStatus("watched")}>
                    <i className={(watched === '0')?"fa-regular fa-eye":"fa-solid fa-eye"}></i>
                </button>
            </div>
        </div>
    )
}

export default MovieBox