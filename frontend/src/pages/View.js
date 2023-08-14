import React, {useState, useEffect} from "react";
import {useNavigate, useLocation, useSearchParams} from "react-router-dom";
import host from "../components/Host";
import PageHeader from "../components/Header";
import MovieBox from "../components/MovieTile";
import Plyr from "plyr-react";
import "plyr/dist/plyr.css";
import './styles.css';

function ViewPage() {
    const location = useLocation();
    const [{user}, setUser] = useState(location.state?location.state:{user: null});
    const [searchParams] = useSearchParams();
    const movie_id = searchParams.get('movie');
    const [movie, setMovie] = useState(null);
    const [movies, setMovies] = useState(null);
    const [videoURL, setVideoURL] = useState('a');
    const [subURL, setSubURL] = useState('a');
    const navigate = useNavigate();

    useEffect(() => {
        if (!user) {
            const isActive = localStorage.getItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
            if (!isActive) {
                navigate('/login');
            }
            else {
                fetch(host + 'bf1e2a1a0e5ed9da4b836e8d75d490d13e3ae8d46ae048bc961f7bfb358416b3/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: isActive, password: '', status: "no" })
                })
                .then((response) => {
                    if (response.status === 404) {
                        localStorage.removeItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
                        navigate('/login');
                    }
                    else if (response.status === 200) {
                        return response.json();
                    }
                })
                .then((data) => {
                    setUser(data);
                    fetch(host + 'e4160e2ceae9b331c2208cd92e29c67fe8177795eb337338b93ac7ee0cadd99b/' + movie_id)
                    .then(response => {
                        if (response.status === 200) {
                            return {data1: response.json(), user_id: data['id']};
                        }
                    })
                    .then(result => {
                        const { data1, user_id } = result;
                        setMovie(data1);
                        fetch('http://localhost:8000/api/98eb11b4c48e22645a9fa336a2bb9989aa53ddea634bc80b6e732a3b8d84a0bd/' + data1['id'])
                        .then(response => {
                            setSubURL('http://localhost:8000/api/257f0036b086851f30acc4850ac4ea1ab4904a126cd9710d5177d4dbe16ba226/' + data1['id']);
                            return response.blob();
                        })
                        .then(blob => {
                            setVideoURL(URL.createObjectURL(blob));
                        })
                        .catch(error => {
                            
                        });
                        fetch(host + 'aaa121090b1fd7761e5408638ed7f186f751f93b4a60c6ff197fc568bcd18766/', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({id: data1['id'], username: user_id})
                        })
                        .then(response => {
                            if (response.status === 200) {
                                return response.json()
                            }
                        })
                        .then((data2) => {
                            setMovies(data2);
                        })
                        .catch(e => {
                            setMovies([]);
                        })
                    })
                    .catch(e => {
                        setMovie([])
                    });
                })
                .catch((e) => {
                    localStorage.removeItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
                    navigate('/login');
                });
            }
        }
        else {
            fetch(host + 'e4160e2ceae9b331c2208cd92e29c67fe8177795eb337338b93ac7ee0cadd99b/' + movie_id)
            .then(response => {
                if (response.status === 200) {
                    return response.json();
                }
            })
            .then((data1) => {
                setMovie(data1);
                fetch('http://localhost:8000/api/98eb11b4c48e22645a9fa336a2bb9989aa53ddea634bc80b6e732a3b8d84a0bd/' + data1['id'])
                .then(response => {
                    setSubURL('http://localhost:8000/api/257f0036b086851f30acc4850ac4ea1ab4904a126cd9710d5177d4dbe16ba226/' + data1['id']);
                    return response.blob();
                })
                .then(blob => {
                    setVideoURL(URL.createObjectURL(blob));
                })
                .catch(error => {
                    
                });
                fetch(host + 'aaa121090b1fd7761e5408638ed7f186f751f93b4a60c6ff197fc568bcd18766/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id: data1['id'], username: user['username']})
                })
                .then(response => {
                    if (response.status === 200) {
                        return response.json();
                    }
                })
                .then((data2) => {
                    setMovies(data2);
                })
                .catch(e => {
                    setMovies([]);
                })
            })
            .catch(e => {
                setMovie([])
            });
        }
    }, [navigate, user, movie_id]);

    const handleRightClick = (event) => {
        event.preventDefault();
    }
    if ((user) && (movie)) {
        return (
            <div className="view-full-container">
                <PageHeader user={user}/>
                <div className="movie-view-container">
                    <Plyr source={{type: "video", title: movie['title'], sources:[{src: videoURL, type: "video/mp4", size: 720}], tracks: [{kind: "captions", label: "English", srcLang: "en", src: subURL, default: true}]}} crossOrigin="anonymous"/>
                </div>
                <div className="movie-info-container">
                    <p className="movie-details">Title : {movie['title']}</p>
                    <p className="movie-details">Cast : {movie['cast'].slice(0, 16).join(', ')}</p>
                    <p className="movie-details">Genres : {movie['genres'].join(', ')}</p>
                    <p className="movie-details">Runtime : {movie['runtime']} min &nbsp;&nbsp;&nbsp; Rating : {movie['rating']} &nbsp;&nbsp;&nbsp; Votes : {movie['votes']}</p>
                    <p className="movie-details">Production : {movie['production'].join(', ')}</p>
                </div>
                { movies && <h1 className="dashboard-title">Similar Movies</h1>}
                { movies && <div className="movie-container">
                    {Object.entries(movies).map(([index, film]) => (
                        <MovieBox key={index} movie={film} user={user}/>
                    ))}
                </div>}
            </div>
        )
    }
}

export default ViewPage;