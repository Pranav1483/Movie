import React, {useState, useEffect} from "react";
import { useNavigate, useLocation } from "react-router-dom";
import './styles.css'
import PageHeader from "../components/Header";
import MovieBox from "../components/MovieTile";
import host from "../components/Host";

function LikesPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const [{user}, setUser] = useState(location.state?location.state:{user: null});
    const [movie, setMovie] = useState([]);
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
                    fetch(host + '61e98b8eeb5ad0d3ad9338ddfe0ee35b7535929e9a6084fac92742858e1bba84/', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username: data['username'], target: "likes"})
                    })
                    .then(response => {
                        if (response.status === 200) {
                            return response.json();
                        }
                    })
                    .then(data1 => {
                        setMovie(data1);
                    })
                    .catch(e => {
                        setMovie([]);
                    })
                })
                .catch((e) => {
                    localStorage.removeItem('9442331fe398b259a1a1dd4ddc062049fca67f4e6d6c783dd838394cb547cb05');
                    navigate('/login');
                });
            }
        }
        else {
            fetch(host + '61e98b8eeb5ad0d3ad9338ddfe0ee35b7535929e9a6084fac92742858e1bba84/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: user['username'], target: "likes"})
            })
            .then(response => {
                if (response.status === 200) {
                    return response.json();
                }
            })
            .then(data1 => {
                setMovie(data1);
            })
            .catch(e => {
                setMovie([]);
            })
        }
    }, [navigate, user]);
    if (user){
        return (
            <div className="full-container-dashboard">
                <PageHeader user={user}/>
                <h1 className="dashboard-title">Liked By {user.fname}</h1>
                <div className="movie-container">
                    {Object.entries(movie).map(([index, film]) => (
                        <MovieBox key={index} movie={film} user={user}/>
                    ))}
                </div>
            </div>
        )
    }
    else {
        return (
            <></>
        )
    }
}

export default LikesPage;